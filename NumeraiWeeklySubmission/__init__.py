#################################################################
#                                                               #
#   Numerai Weekly Submission (Time-triggered Azure function)   #
#                                                               #
#################################################################

# Load libraries
import azure.functions as func
from azure.storage.blob import BlobClient, ContainerClient

import os
import gc
import logging
import datetime
import pickle
import pandas as pd

from NumeraiWeeklySubmission.helpers import (get_numerai_tournament_current_round_number,
                                            download_numerai_live_data, get_feature_names, create_ensemble_predictions,
                                            prepare_predictions, submit_predictions, send_email_notification)


# // Main frunction //
def main(mytimer: func.TimerRequest) -> None:

    # Logs
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    if mytimer.past_due:
        logging.info('The timer is past due!')
    logging.info(f'Python timer trigger function ran at {utc_timestamp}')

    # Load environment variables (settings)
    AzureWebJobsStorage_var = os.environ['AzureWebJobsStorage']
    settings = {element.split("=",1)[0]:element.split("=",1)[1] for element in AzureWebJobsStorage_var.split(";")}

    # 1. Get current tournament round
    logging.info('1. Get current tournament round')
    current_round = get_numerai_tournament_current_round_number()
    logging.info(f"Current round: {current_round}")

    # 2. Download numerai_live_data and save it as a parquet file in a temporary folder
    
    # Warning: The current directory in Azure Functions is read-only. 
    # Use ./data when running locally and /tmp when deploying to Azure Functions.
    logging.info('2. Download numerai_live_data and save it as a parquet file in a local path')
    download_numerai_live_data(local_path= "/tmp", current_round=current_round)

    # 3. Load numerai_live_data (from ephemeral storage, not from Azure storage)
    logging.info('3. Load numerai_live_data (from ephemeral storage, not from Azure storage')
    numerai_live_data = pd.read_parquet(f"/tmp/numerai_live_data_{current_round}.parquet")
    logging.info(f"numerai_live_data shape: {numerai_live_data.shape}")

    # 4. (Optional) Upload numerai_live_data for the current round to Azure Blob Storage
    logging.info('4. Upload numerai_live_data for the current round to Azure Blob Storage')
    blob_client = BlobClient(account_url=settings["DefaultEndpointsProtocol"] + "://" + settings["AccountName"] + ".blob.core.windows.net",
                             credential=settings["AccountKey"],
                             max_single_put_size=4*1024*1024,
                             container_name="live-data",
                             blob_name=f"numerai_live_data_{current_round}.csv")
    
    blob_client.upload_blob(data=numerai_live_data.to_csv(index=True, index_label="id", encoding = "utf-8"),
                            blob_type="BlockBlob",
                            connection_timeout=600)

    # 5. Load trained ML models from Azure Storage
    logging.info('5. Load trained ML models from Azure Storage')

    ## Check all available pre-trained ML models
    container_client = ContainerClient(account_url=settings["DefaultEndpointsProtocol"] + "://" + settings["AccountName"] + ".blob.core.windows.net",
                                       credential=settings["AccountKey"],
                                       container_name="production-models")

    model_names = [blob.name for blob in container_client.list_blobs()]
    model_names = sorted(model_names)
    logging.info(f"There are {len(model_names)} blobs in this container")
    logging.info(f"{model_names}")

    ## Load each model, predict and store predictions
    for MODEL_NAME in model_names:

        logging.info(f"MODEL_NAME: {MODEL_NAME}")

        # Define model BlobClient
        blob_client = BlobClient(account_url=settings["DefaultEndpointsProtocol"] + "://" + settings["AccountName"] + ".blob.core.windows.net",
                                 credential=settings["AccountKey"],
                                 container_name="production-models",
                                 blob_name=MODEL_NAME)

        # Load trained model
        downloader = blob_client.download_blob()
        model = pickle.loads(downloader.readall())

        training_features = get_feature_names(model)
        # logging.info(f"total features: {len(training_features)}")

        # Predict and store predictions
        numerai_live_data.loc[:, MODEL_NAME] = model.predict(numerai_live_data[training_features])


    ## Keep only the predictions for the current round
    numerai_predictions = numerai_live_data[model_names].copy(deep=True)
    
    ## Delete numerai_live_data
    numerai_live_data = None
    del numerai_live_data
    gc.collect()

    logging.info(f"There are {numerai_predictions.shape[1]} total models predictions")


    # 6. Create Ensemble predictions
    logging.info('6. Create Ensemble predictions')
    numerai_predictions = create_ensemble_predictions(numerai_predictions)
    logging.info(f"There are {numerai_predictions.shape[1]} total models predictions with ensemble predictions")


    # 7. Prepare predictions
    logging.info('7. Prepare predictions')
    numerai_predictions = prepare_predictions(numerai_predictions)


    # 8. (Optional) Upload predictions to Azure Blob Storage
    logging.info('8. Upload predictions to Azure Blob Storage')
    blob_client = BlobClient(account_url=settings["DefaultEndpointsProtocol"] + "://" + settings["AccountName"] + ".blob.core.windows.net",
                             credential=settings["AccountKey"],
                             max_single_put_size= 4*1024*1024,
                             container_name="predictions-files",
                             blob_name=f"numerai_predictions_{current_round}.csv")

    blob_client.upload_blob(numerai_predictions.to_csv(index=True, index_label="id", encoding = "utf-8"),
                            blob_type="BlockBlob",
                            connection_timeout=600)


    # 9. Submit predictions using NumerAPI
    logging.info('9. Submit predictions using NumerAPI')
    submit_predictions(numerai_predictions)
    
    
    # 10. (Optional) Send email to notify me that the job is done
    logging.info('10. Send email to notify me that the job is done')
    send_email_notification(current_round)
#########################
#                       #
#   Helper functions    #
#                       #
#########################

# 1. get_numerai_tournament_current_round_number()
# 2. download_numerai_live_data(local_path="./data")
# 3. get_feature_names(model)
# 4. create_ensemble_predictions(numerai_predictions: pd.DataFrame)
# 5. prepare_predictions(numerai_predictions)
# 6. submit_predictions(numerai_predictions: pd.DataFrame)
# 7. send_email_notification(current_round: int)
# 8. generate_random_quote()


# Load libraries
import os
import pathlib
import numpy as np
import pandas as pd
from numerapi import NumerAPI
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Suppress warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


## NumerAPI
def get_numerai_tournament_current_round_number()->int:
    napi = NumerAPI()
    return napi.get_current_round()


def download_numerai_live_data(local_path:str="/tmp", current_round:int=None):
    
    # Create local path to store downloaded data
    pathlib.Path(local_path).mkdir(parents=True, exist_ok=True) 

    # Download live data
    napi = NumerAPI()
    napi.download_dataset(filename="v4/live.parquet",
                          dest_path=f"{local_path}/numerai_live_data_{current_round}.parquet")
    return None



## ML Helpers
def get_feature_names(model):
    """Extract feature names from trained ML model"""
    
    if hasattr(model, 'feature_names_in_'):
        # Sklearn models
        training_features = model.feature_names_in_
    elif hasattr(model, 'feature_name_'):
        # Lightgbm
        training_features = model.feature_name_
    elif hasattr(model, 'get_booster'):
        # XGBoost
        training_features = model.get_booster().feature_names
            
    return training_features


def create_ensemble_predictions(numerai_predictions: pd.DataFrame):
    """Create Ensemble predictions"""

    # PLACEHOLDER FOR ENSEMBLE MODELING CODE

    # Add random predictions
    numerai_predictions["RANDOM33"] = np.random.choice(a = [0.00, 0.25, 0.50, 0.75, 1.00],
                                                            size=numerai_predictions.shape[0],
                                                            replace=True,
                                                            p=[0.05, 0.20, 0.50, 0.20, 0.05])


    return numerai_predictions



def prepare_predictions(numerai_predictions: pd.DataFrame):
    """Prepare predictions for submission"""

    # PLACEHOLDER FOR PREPARE PREDICTIONS FILE CODE 
    rename_columns_dict = {}

    numerai_predictions = numerai_predictions.rename(columns=rename_columns_dict)
    return numerai_predictions


def submit_predictions(numerai_predictions: pd.DataFrame):
    """Submit predictions to Numerai"""

    # Get NumerAPI Keys
    NumerAPIKeys_var = os.environ['NumerAPIKeys']
    NumerAPIKeys_dict = {element.split("=",1)[0]:element.split("=",1)[1] for element in NumerAPIKeys_var.split(";")}
    napi = NumerAPI(secret_key=NumerAPIKeys_dict['secret_key'],
                    public_id=NumerAPIKeys_dict['public_id'])

    # Every columns in numerai_predictions dataset is a prediction for a different model
    for model_name in numerai_predictions.columns:
        
        # Submit predictions for this model
        print("model_name:", model_name)
        
        # Get model UUID
        model_id = napi.get_models()[model_name.lower()]
        print("model_id:",model_id)
        
        # Submit predictions via Numerai API
        napi.upload_predictions(tournament = 8, 
                                model_id = model_id,
                                df = (numerai_predictions[[model_name]]
                                    .rename(columns={f"{model_name}":"prediction"})
                                    .reset_index()))
        
        print("-"*50)

    return None


## Utils
def send_email_notification(current_round: int):
    """Send email notification"""

    sg = sendgrid.SendGridAPIClient(api_key=os.environ['SendGridKeys'])
    from_email = Email("from.example@example.com")                               # Change to your verified sender
    to_email = To("to.example@example.com")                                      # Change to your recipient
    subject = f"Numerai Submission was successful | Round {current_round}"

    content = Content("text/html", generate_random_quote())
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
    return None


def generate_random_quote():
    """Generate a random quote from the list of quotes"""
    
    from random_words import RandomWords
    from quote import quote
    rw = RandomWords().random_word()
    quote_json = quote(rw, limit=1)
    
    # Create html content for the email
    html_content = f"""
    <h1> Good job! <h1>
    <h3> Another week that you save yourself 1h &#8987; </h3>
    <p> Automated weekly Numerai Submission was successful. </p>
    <hr>
    <strong><p> Here is your quote: </p></strong>
    <blockquote>
        {quote_json[0]['quote']}
    </blockquote>
    <figcaption> &#9997; {quote_json[0]['author']}</figcaption>
    """
    return html_content

    	
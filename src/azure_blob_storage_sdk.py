#############################
#                           #
#   Azure Blob Storge SDK   # 
#                           #
#############################

# The following components make up the Azure Blob Service:

# 1. The storage account itself (BlobServiceClient)
# 2. A container within the storage account (ContainerClient)
# 3. A blob (file) within a container (BlobClient)


## Load modules
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient


## Create client objects

blob_service_client = BlobServiceClient(account_url="****", 
                                        credential="****")

container_client = ContainerClient(account_url="****",
                                   credential="****",
                                   container_name="production-models")


blob_client = BlobClient(account_url="****",
                        credential="****",
                        container_name="production-models",
                        blob_name="ml_model.pkl")


## 1. BlobServiceClient: Connect to Azure Storage Account
blob_service_client.get_account_information()

# Check containers inside the Azure Blob Storage account
containers_list = blob_service_client.list_containers()
for container in containers_list:
    print(container.name)

## 2. ContainerClient: Connect to a container
blobs_list = [blob.name for blob in container_client.list_blobs()]
print(f"There are {len(blobs_list)} blobs in this container")
print(blobs_list)


## 3. BlobClient: Connect to a blob
blob_client.exists()
blob_client.url

downloader = blob_client.download_blob()

import pickle
model = pickle.loads(downloader.readall())
model
type(model)
model.get_params()

import numpy as np
model.predict(np.random.choice(a=[0,0.25, 0.50, 0.75,1], size=len(model.feature_name_), replace=True).reshape(1,-1))


## Download Numerai Live data and save it as a CSV file in Azure Blob Storage

# Download Numerai Live Data
from numerapi import NumerAPI
napi = NumerAPI()
current_round = napi.get_current_round()

file_name = f"numerai_live_data_{current_round}.parquet"
napi.download_dataset(filename="v4/live.parquet", dest_path=f"../data/{file_name}")


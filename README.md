# Azure functions with Python

## About this repository

A complete guide on developing and deploying Azure functions with Python, using VSCode and Azure extension.

🧰 **Prerequisites:**

1. Azure Account <https://portal.azure.com>
2. VSCode <https://code.visualstudio.com/> and Azure Extension <https://code.visualstudio.com/docs/azure/extensions>
3. Python 3.8 <https://www.python.org/>
4. Azure Functions Core Tools <https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Clinux%2Ccsharp%2Cportal%2Cbash#v2>
5. Azure Storage Explorer <https://azure.microsoft.com/en-us/features/storage-explorer/>
6. Numerai API Keys <https://numer.ai/account> (Optional for NumeraiWeeklySubmission)
7. Trained ML/DL models and inference python code (Optional for NumeraiWeeklySubmission)

---

## Numerai Weekly Submission

🕵️ Looking for the code for my Medium Article, [How I automated my Numerai weekly submissions pipeline for free, using Azure functions and python](https://medium.com/@papaemman.pan/how-i-automated-my-numerai-weekly-submissions-pipeline-for-free-using-azure-functions-and-python-9bcf8382af1c) ?

Go to [NumeraiWeeklySubmission](./NumeraiWeeklySubmission) directory

---

## Documentation 📚

1. [Azure Functions](./docs/1_Azure_functions.md)
2. [Azure Functions with Python](./docs/2_Azure_functions_with_python.md)
3. [Azure Blob Storage Python SDK](./docs/3_Azure_Blob_storage_python_sdk_notes.md)
4. [Azure Functions http requessts](./docs/4_Azure_Functions_http_request.md)
5. [Azure Functions time trigger](./docs/5_Azure_Functions_time_trigger.md)

## Contents

1. [HttpExample](./HttpExample/) directory contains an example of an http-triggered (input) Azure function, writting in messages in an Azure queue (output binding).

2. [NumeraiWeeklySubmission](./NumeraiWeeklySubmission/) directory contains an example of a time-triggered Azure function with Azure Blob storage integration.

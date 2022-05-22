# Azure functions

## Resources

* [Azure Functions Docs](https://docs.microsoft.com/en-us/azure/azure-functions/)
* [Azure Functions developer guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference?tabs=blob)
* [Browse code samples](https://docs.microsoft.com/en-us/samples/browse/?products=azure-functions&languages=python)
* [Azure Functions triggers and bindings concepts](https://docs.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings?tabs=csharp)
* [Azure serverless community library](https://www.serverlesslibrary.net/?technology=Blob%20Storage&language=Python)

---

## Function code

A function is the primary concept in Azure Functions.
A function contains two important pieces - your **code**, which can be written in a variety of languages, and some config, the `function.json` file.
For compiled languages, this config file is generated automatically from annotations in your code. For scripting languages, you must provide the config file yourself.

## Function app

A function app provides an execution context in Azure in which your functions run.
As such, it is the unit of deployment and management for your functions.

## Folder structure

The code for all the functions in a specific function app is located in a root project folder that contains a host configuration file.
The `host.json` file contains runtime-specific configurations and is in the root folder of the function app.
A `bin` folder contains packages and other library files that the function app require.

## How to edit functions in the Azure portal

The Functions editor built into the Azure portal lets you update your code and your function.json file directly inline.
This is recommended only for **small changes** or proofs of concept - best practice is to use a local development tool like VS Code.

## Create a local Functions project

A Functions project directory contains the following files and folders, regardless of language:

| File name                 | Description |
| -----------               | ----------- |
| `host.json`               | Host configuration file |
| `function.json`           | Function configuration file |
| `local.settings.json`     | Settings used by Core Tools when running locally, including app settings. To learn more, see local settings. |
| `.gitignore`              | Prevents the local.settings.json file from being accidentally published to a Git repository. To learn more, see local settings |
| `.vscode\extensions.json` | Settings file used when opening the project folder in Visual Studio Code. |

## Triggers and Bindings

**Triggers** are what cause a function to run.
A trigger defines how a function is invoked and a function must have exactly one trigger.
Triggers have associated data, which is often provided as the payload of the function.

**Binding** to a function is a way of declaratively connecting another resource to the function; bindings may be connected as input bindings, output bindings, or both.
Data from bindings is provided to the function as parameters.

You can mix and match different bindings to suit your needs.
Bindings are optional and a function might have one or multiple input and/or output bindings.

* For triggers, the direction is always in
* Input and output bindings use in and out
* Some bindings support a special direction inout. If you use inout, only the Advanced editor is available via the Integrate tab in the portal.

## Example Scenario

A **scheduled job** (Timer) reads **Blob Storage** contents and creates a new **Cosmos DB document**.

## Create a new Binding step-by-step

1. Add new binding

2. Select binding direction
    * out
    * in

3. Select binding type

    * Azure Blob Storage
    * Azure Cosmos DB
    * Azure Event Hubs
    * Azure Queue Storage
    * Azure Service Bus
    * Azure Table Storage
    * HTTP
    * Kafka Output
    * SendGrid
    * SignalR
    * Twilio SMS

4. Select the name used to identify this binding in your code

5. More settings
    * The queue to which the message will be sent. If the queue doesn't exists yet,
one will be vreated for you in the specified storage account.
    * The path within your storage account to which the blob will be written.

6. Select settings from "local.settings.json"

---

## Helpers

### Azure function triggers

1. Time trigger
2. Azure Blob Storage trigger
3. Azure Cosmos DB trigger
4. Durable Functions activity
5. Durable Functions HTTP starter
6. Durable Functions orchestrator
7. Azure Event Grid trigger
8. Azure Event Hub trigger
9. Azure Queue storage trigger
10. Azure Service Bus Queue trigger
11. Azure Service Bus Topic trigger
12. HTTP trigger
13. HTTP trigger(s) from OpenAPI V2/V3 Specification (Preview)

### Authorization level

1. Function
2. Anonymoys
3. Admin

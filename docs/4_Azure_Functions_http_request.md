# Azure Functions | Python DEMO

Azure Functions are a powerful way to build stateless services that can be deployed to Azure.

Documentation: [Azure Functions Python Developer Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level)

## Guides

1. [Quickstart: Create a function in Azure with Python using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)

2. [Connect Azure Functions to Azure Storage using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/functions-add-output-binding-storage-queue-vs-code?pivots=programming-language-python&tabs=in-process)

---

## Goal

Create an HTTP triggered Azure function, which will write a message in an Azure Queue storage.

## Requirements

1. An Azure account with an active subscription
2. The Azure Functions Core Tools
3. Python versions that are supported by Azure Functions.
4. Visual Studio Code
5. The Python extension for Visual Studio Code.
6. The Azure Functions extension for Visual Studio Code.
7. Install the Azure Storage extension for Visual Studio Code.
8. Install Azure Storage Explorer.

> In a terminal or command window, run ```func --version``` to check that the **Azure Functions Core Tools** version.

---

## 1. Create your local project

**Important Note:** These steps were designed to be completed outside of a workspace. In this case, do not select a project folder that is part of a workspace.

1. Choose the **Azure icon** in the Activity bar, then in the Azure: Functions area, select the Create new project... icon.
2. Choose a directory location for your project workspace and choose Select. It is recommended that you create a new folder or choose an empty folder as the project workspace.
3. Provide the following information at the prompts:
    * Select a language for your function project: Choose `Python`.
    * Select a Python alias to create a virtual environment: Choose the location of your `Python interpreter`. If the location isn't shown, type in the full path to your Python binary.
    * Select a template for your project's first function: Choose `HTTP trigger`.
    * Provide a function name: Type `HttpExample`.
    * Authorization level: Choose `Anonymous`, which enables anyone to call your function endpoint. To learn about authorization level, see Authorization keys.
    * Select how you would like to open your project: Choose `Add to workspace`.
4. Using this information, Visual Studio Code generates an Azure Functions project with an HTTP trigger. You can view the local project files in the Explorer

## 2. Run the function locally

Visual Studio Code integrates with [Azure Functions Core tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local) to let you run this project on your local development computer before you publish to Azure.

1. To call your function, **press F5 to start the function app project**.
Output from Core Tools is displayed in the Terminal panel. Your app starts in the Terminal panel.
You can see the URL endpoint of your HTTP-triggered function running locally.

2. With Core Tools running, go to the Azure: Functions area. Under Functions, expand `Local Project > Functions`. Right-click (Windows) the HttpExample function and choose **Execute Function Now....**

3. In Enter request body you see the request message body value of `{ "name": "Azure" }`. Press Enter to send this request message to your function.

4. When the **function executes locally and returns a response, a notification is raised in Visual Studio Code**. Information about the function execution is shown in Terminal panel.

5. With the Terminal panel focused, press `Ctrl + C` to **stop Core Tools** and disconnect the debugger.

After you've verified that the function runs correctly on your local computer, it's time to use Visual Studio Code to publish the project directly to Azure.

## 3. Publish the project to Azure

Important Note: Publishing to an existing function app overwrites the content of that app in Azure.

1. Sign in to Azure from VS Code

2. Choose the Azure icon in the Activity bar, then in the `Azure: Functions area`, choose the **Deploy to function app**... button.

3. Provide the following information at the prompts:

    * **Select folder**: Choose a folder from your workspace or browse to one that contains your function app. You won't see this if you already have a valid function app opened.

    * **Select subscription**: Choose the subscription to use. You won't see this if you only have one subscription.

    * **Select Function App in Azure**: Choose + Create new Function App. (Don't choose the Advanced option, which isn't covered in this article.)

    * **Enter a globally unique name for the function app**: Type a name that is valid in a URL path. The name you type is validated to make sure that it's unique in Azure Functions.

    * **Select a runtime**: Choose the version of Python you've been running on locally. You can use the python --version command to check your version.

    * **Select a location for new resources**: For better performance, choose a region near you.

    * After that, the extension shows the status of individual resources as they are being created in Azure in the notification area.

4. When completed, the following Azure resources are created in your subscription, using names based on your function app name:

    * A **resource group**, which is a logical container for related resources.
    * A **standard Azure Storage account**, which maintains state and other information about your projects.
    * A **consumption plan**, which defines the underlying host for your serverless function app.
    * A **function app**, which provides the environment for executing your function code. A function app lets you group functions as a logical unit for easier management, deployment, and sharing of resources within the same hosting plan.
    * An **Application Insights** instance connected to the function app, which tracks usage of your serverless function.
    * A notification is displayed after your function app is created and the deployment package is applied.

## 4. Run the function in Azure

1. Back in the `Azure: Functions` area in the side bar, expand your **subscription, your new function app, and Functions**. Right-click the `HttpExample` function and choose Execute Function Now....

2. In Enter request body you see the request message body value of `{ "name": "Azure" }`. Press Enter to send this request message to your function.

3. When the function executes in Azure and returns a response, a notification is raised in Visual Studio Code.

## 5. Download the function app settings

1. Press the **F1 key to open the command palette**, then search for and run the command `Azure Functions: Download Remote Settings.....`

2. Choose the function app you created in the previous article. Select Yes to all to overwrite the existing local settings. Because it contains **secrets**, the `local.settings.json` file never gets published, and is excluded from source control

3. Copy the value `AzureWebJobsStorage`, which is the **key for the Storage account** connection string value. You use this connection to verify that the output binding works as expected.

## 6. Register binding extensions

Because you're using a **Queue storage output binding,** you must have the Storage bindings extension installed before you run the project.

Your project has been configured to use **extension bundles**, which automatically installs a predefined set of extension packages.

Extension bundles usage is enabled in the `host.json` file at the root of the project.

In Functions, each type of binding requires

1. direction
2. type,
3. a unique name
to be defined in the `function.json` file. The way you define these attributes depends on the language of your function app.

**Binding attributes are defined directly** in the `function.json` file. Depending on the binding type, additional properties may be required.
The queue output configuration describes the fields required for an Azure Storage queue binding. The extension makes it easy to add bindings to the `function.json` file.

**To create a binding, right-click the `function.json` file** in your HttpTrigger folder and choose `Add binding....` Follow the prompts to define the following binding properties for the new binding:

| Prompt    | Value  | Description |
| ----------| -------| ----------- |
| Select binding direction| `out` | The binding is an output binding.
| Select binding with direction... | `Azure Queue Storage` | The binding is an Azure Storage queue binding.|
|  The name used to identify this binding in your code | `msg` | Name that identifies the binding parameter referenced in your code. |
| The queue to which the message will be sent | `outqueue` | The name of the queue that the binding writes to. When the queueName doesn't exist, the binding creates it on first use. |
|  Select setting from "local.setting.json" |  `AzureWebJobsStorage` | The name of an application setting that contains the connection string for the Storage account. The AzureWebJobsStorage setting contains the connection string for the Storage account you created with the function app. |

## 7. Add code that uses the output binding

After the binding is defined, you can **use the name of the binding to access it as an attribute in the function signature.**
By using an output binding, you don't have to use the Azure Storage SDK code for authentication, getting a queue reference, or writing data.
The Functions runtime and queue output binding do those tasks for you.

Update `HttpExample\__init__.py` to match the following code, adding the `msg` parameter to the function definition and `msg.set(name)` under the `if name:` statement.

The `msg` parameter is an instance of the `azure.functions.Out` class.
Its set method writes a string message to the queue, in this case the name passed to the function in the URL query string.

## 8. Run the function locally

1. Press **F5** to start the function app project and Core Tools.

2. With **Core Tools** running, go to the Azure: Functions area. Under Functions, expand Local Project > Functions. Right-click the HttpExample function and choose Execute Function Now....

3. In Enter request body you see the request message body value of `{ "name": "Azure" }`. Press Enter to send this request message to your function.

    * **Note: You can trigger the function sending a request using the browser**

        * Without parameters: <https://azure-function-python-demo.azurewebsites.net/api/httpexample>

        * Passing parameters: <https://azure-function-python-demo.azurewebsites.net/api/httpexample?name=panagiotis>

4. After a response is returned, press **Ctrl + C to stop Core Tools**.

Because you are using the storage connection string, your function connects to the Azure storage account when running locally.
A new queue named **outqueue** is created in your storage account by the Functions runtime when the output binding is first used.
You'll use **Storage Explorer** to verify that the queue was created along with the new message.

## 9. Connect Storage Explorer to your account

1. Run the **Azure Storage Explorer tool**, select the connect icon on the left, and select Add an account.
2. In the Connect dialog, choose Add an Azure account, choose your Azure environment, and select Sign in....
3. After you successfully sign in to your account, you see all of the Azure subscriptions associated with your account.

## 10. Examine the output queue

1. Open the **Azure Storage Explorer tool.**
2. Expand the Queues node, and then select the queue named **outqueue**.
3. Run the function again, send another request, and you'll see a new message appear in the queue.

## 11. Redeploy and verify the updated app

1. In Visual Studio Code, press F1 to open the command palette. In the command palette, search for and select `Azure Functions: Deploy to function app....`

2. Choose the function app that you created. Because you're redeploying your project to the same app, select Deploy to dismiss the warning about **overwriting files**.

3. After deployment completes, you can again use the `Execute Function Now...` feature to trigger the function in Azure.

4. Again view the message in the storage queue to verify that the output binding again generates a new message in the queue.

## Clean up resources

Use the following steps to delete the function app and its related resources to avoid incurring any further costs.

1. In Visual Studio Code, press F1 to open the command palette. In the command palette, search for and select Azure Functions: Open in portal.

2. Choose your function app, and press Enter. The function app page opens in the Azure portal.

3. In the Overview tab, select the named link next to Resource group.

4. In the Resource group page, review the list of included resources, and verify that they are the ones you want to delete.

5. Select Delete resource group, and follow the instructions. Deletion may take a couple of minutes. When it's done, a notification appears for a few seconds. You can also select the bell icon at the top of the page to view the notification.

---

## Common Errors

1. App can't run
"connect ECONNREFUSED 127.0.0.1:9091"
"value cannot be null. (parameter 'provider') azure functions python"

Modify `host.json` file with the correct verions

```json
"extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[2.*, 4.0.0)"
  }
```

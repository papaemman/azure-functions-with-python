# Azure functions

## Resources

* [Azure Functions Python code samples](https://docs.microsoft.com/en-us/samples/browse/?products=azure-functions&languages=python)

* [Azure Functions Python developer guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level)

Table of Contents

1. Programming model
2. Alternate Entry point
3. Folder structure
4. Import behacior
5. Triggers and Inputs
6. Outputs
7. Logging
8. Log custom telemetry
9. HTTP Trigger and bindings
10. Web frameworks
11. Scaling and Performance
12. Context
13. Global variables
14. Environment variables
15. Python version
16. Package management
17. Publishing to Azure
18. Unit Testing
19. Temporary files
20. Preinstalled libraries
21. Python worker extensions
22. Cross-origin resource sharing
23. Async


---

## Programming model

Azure Functions expects a function to be a **stateless method** in your Python script that **processes input** and **produces output.**
By default, the runtime expects the method to be implemented as a **global method** called `main()` in the `__init__.py` file.

Data from **triggers** and **bindings** is bound to the function via **method attributes** using the `name` property defined in the `function.json` file.

For example, the `function.json` below describes a **simple function triggered by an HTTP** request named `req`:

```{json}
{
    "scriptFile": "__init__.py",
    "bindings": [
        {
            "authLevel": "function",
            "type": "httpTrigger",
            "direction": "in",
            "name": "req",
            "methods": [
                "get",
                "post"
            ]
        },
        {
            "type": "http",
            "direction": "out",
            "name": "$return"
        }
    ]
}
```

Based on this definition, the `__init__.py` file that contains the function code might look like the following example:

```{python}
def main(req):
    user = req.params.get('user')
    return f'Hello, {user}!'
```

You can also **explicitly declare the attribute types** and return type in the function using Python type annotations. This helps you use the intellisense and autocomplete features provided by many Python code editors.

```{python}
import azure.functions

def main(req: azure.functions.HttpRequest) -> str:
    user = req.params.get('user')
    return f'Hello, {user}!'
```
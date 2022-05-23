# Azure function project file structure

```{bash}
.
├── .venv                     # Python Virtual environment
├── .vscode                   # Configuration options for VSCode
├── host.json                 # Configuration options that affect all functions in a function app instance
├── local.settings.json       # Maintains settings used when running functions locally.These settings aren't used when running in Azure
|
├── AzureFunction_1
│ ├── function.json           # Azure Function Settings
│ ├── __init__.py             # Python Code
│ └── readme.md               # Documentation
|
├── AzureFunction_2
│ ├── function.json           
│ ├── __init__.py             
│ └── readme.md               
|
└── requirements.txt          # Package dependencies
```

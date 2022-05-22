# Azure Functions notes

* Azure functions are designed to run as a separate workspace in VSCode.
In order to combine the code of Azure Functions to my main codebase, I have to create a new `compute` directory in my original codebase and open this directory in VSCode. It is essential not to have any workspace open when I initialize the local Azure Function for the first time.

## Resources

1. [Timer trigger for Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=in-process&pivots=programming-language-python#example)

2. [Azure Blob storage input binding for Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-blob-input?tabs=in-process%2Cextensionv5&pivots=programming-language-python)

3. [Azure Functions SendGrid bindings](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-sendgrid?tabs=in-process%2Cfunctionsv2&pivots=programming-language-python)

---

## Time Trigger examples

```{json}
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "name": "mytimer",
      "type": "timerTrigger",
      "direction": "in",
      "schedule": "10 * * * * *"
    }
  ]
} 
```

### Operators

| Type                           | Example | When triggered |
| ----                           | -------      | ------------   |
| A specific value               | ```0 5 * * * *``` | Once every hour of the day at minute 5 of each hour
| All values (*)                 | ```0 * 5 * * *```| At every minute in the hour, beginning at hour 5
| A range (- operator)           | ```5-7 * * * * *```| Three times a minute - at seconds 5 through 7 during every minute of every hour of each day
| A set of values (, operator)   | ```5,8,10 * * * * *```| Three times a minute - at seconds 5, 8, and 10 during every minute of every hour of each day
| An interval value (/ operator) | ```0 */5 * * * *```| 12 times an hour - at second 0 of every 5th minute of every hour of each day

To specify months or days you can use numeric values, names, or abbreviations of names:

* For days, the numeric values are 0 to 6 where 0 starts with Sunday.
* Names are in English. For example: Monday, January.
* Names are case-insensitive.
* Names can be abbreviated. Three letters is the recommended abbreviation length. For example: Mon, Jan. 
* Keep in mind that **UTC time** is -3 hours from Greece Time.

### Example schedules

| Example | When triggered |
| ------- | ------------   |
| ```0 */5 * * * *```      | once every five minutes |
| ```0 0 * * * *```        | once at the top of every hour |
| ```0 0 */2 * * *```      | once every two hours |
| ```0 0 9-17 * * *```     | once every hour from 9 AM to 5 PM |
| ```0 30 9 * * *```       | at 9:30 AM every day |
| ```0 30 9 * * 1-5```     | at 9:30 AM every weekday |
| ```0 30 9 * Jan Mon```   | at 9:30 AM every Monday in January |
| ```10 * * * * *```       | at the 10th second  every minute |
| ```*/10 * * * * *"```    | once every 10 seconds |

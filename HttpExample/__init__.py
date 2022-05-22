#################################################################
#                                                               #
#   Http-triggered Azure function with output bidning in queue  #
#                                                               #
#################################################################

# Load libraries
import logging
import azure.functions as func

# Main function
def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> str:
    logging.info(f"PAPAEMMAN | Function triggered by HTTP request.")
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        msg.set(name)
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )
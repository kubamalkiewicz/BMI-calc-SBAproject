import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="CalculateBMI")
def CalculateBMI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        weight = req_body.get('weight')
        height = req_body.get('height')

        if not weight or not height:
            return func.HttpResponse(
                 "Please pass weight and height in the request body",
                 status_code=400
            )

        # Calculate BMI
        height_m = height / 100
        bmi = round(weight / (height_m * height_m), 1)

        # Determine health category
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        response_data = {
            "bmi": bmi,
            "category": category
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            mimetype="application/json",
            status_code=200
        )
        
    except ValueError:
        return func.HttpResponse(
             "Invalid input format.",
             status_code=400
        )
import joblib
import pandas as pd
import os
from app.logger_setup import setup_logging

logger = setup_logging()

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "model.pkl")


def predict_churn(features: list) -> int:
    try:
        model = joblib.load(MODEL_PATH)

        # These names MUST match the "Feature names seen at fit time" in your error log
        columns = [
            "standardscaler__CreditScore",
            "standardscaler__Age",
            "standardscaler__Tenure",
            "standardscaler__Balance",
            "standardscaler__NumOfProducts",
            "standardscaler__HasCrCard",
            "standardscaler__IsActiveMember",
            "standardscaler__EstimatedSalary",
            "onehotencoder__Geography_Germany",
            "onehotencoder__Geography_Spain",
            "onehotencoder__Gender_Male",
        ]

        input_df = pd.DataFrame([features], columns=columns)
        prediction = model.predict(input_df)
        return int(prediction[0])

    except Exception as e:
        logger.error(f"Prediction Error: {e}")
        raise e

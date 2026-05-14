from litestar import Litestar, get, post
from pydantic import BaseModel
from app.model_utils import predict_churn
from app.logger_setup import setup_logging

logger = setup_logging()


class ChurnRequest(BaseModel):
    CreditScore: float
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: float
    IsActiveMember: float
    EstimatedSalary: float
    Geography_Germany: int
    Geography_Spain: int
    Gender_Male: int


@get("/", sync_to_thread=False)
def home() -> dict[str, str]:
    return {"message": "Welcome to the Churn Prediction Service"}


@get("/health", sync_to_thread=False)
def health() -> dict[str, str]:
    return {"status": "healthy"}


@post("/predict", sync_to_thread=False)
def predict(data: ChurnRequest) -> dict[str, int]:
    features = [
        data.CreditScore,
        data.Age,
        data.Tenure,
        data.Balance,
        data.NumOfProducts,
        data.HasCrCard,
        data.IsActiveMember,
        data.EstimatedSalary,
        data.Geography_Germany,
        data.Geography_Spain,
        data.Gender_Male,
    ]

    prediction = predict_churn(features)
    return {"prediction": prediction}


app = Litestar(route_handlers=[home, health, predict])

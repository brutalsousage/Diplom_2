BASE_URL = "https://stellarburgers.education-services.ru/"
LOGIN_ENDPOINT = f"{BASE_URL}api/auth/login"
REGISTER_ENDPOINT = f"{BASE_URL}api/auth/register"
TOKEN_ENDPOINT = f"{BASE_URL}api/auth/token"
INGREDIENTS_ENDPOINT = f"{BASE_URL}api/ingredients"
ORDERS_ENDPOINT = f"{BASE_URL}api/orders"



REQUIRED_FIELDS_MESSAGE = "Email, password and name are required fields"
USER_EXISTS_MESSAGE = "User already exists"
AUTH_REQUIRED_MESSAGE = "You should be authorised"
INGREDIENTS_REQUIRED_MESSAGE = "Ingredient ids must be provided"
INVALID_CREDENTIALS_MESSAGE = "email or password are incorrect"

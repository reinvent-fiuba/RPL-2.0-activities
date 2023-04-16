from fastapi.security import OAuth2PasswordBearer

get_token = OAuth2PasswordBearer(tokenUrl="token")

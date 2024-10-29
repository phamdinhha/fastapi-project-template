import jwt
from fastapi import Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient
from app.core.settings import settings
from app.core.logger import ServiceLogger


logger = ServiceLogger.get_logger()

url = settings.PUBLIC_AUTH_JWKS_URL
kid = settings.PUBLIC_AUTH_KID
jwks_client = PyJWKClient(uri=url, lifespan=3600)

bearer = HTTPBearer(auto_error=False)


def get_token_claims(bearer_token: HTTPAuthorizationCredentials):
    token = str(bearer_token.credentials)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    data = jwt.decode(
        bearer_token,
        signing_key.key,
        algorithms=["RS256"],
        options={
            "verify_signature": True,
            "verify_exp": True,
            "verify_nbf": False,
            "verify_iat": True,
            "verify_aud": False,
            "verify_iss": False,
            "require": [],
        },
    )
    return data


async def verify_token(
    request: Request,
    bearer_token: HTTPAuthorizationCredentials = Security(bearer)
):
    if not bearer_token:
        err_msg = "Must provide an access token."
        logger.error(err_msg)
        err_code = status.HTTP_401_UNAUTHORIZED
        err = {
            'err_msg': err_msg,
            'err_code': err_code
        }
        return None, err
    
    try:
        token_claims = get_token_claims(bearer_token)
        request.state.user = token_claims
    except Exception as e:
        logger.error(f"Could not get token claims:\n{e}", exc_info=True)
        err_msg = f"Could not verify, parse, and/or validate scope from provided access token: {str(e)}"
        err_code = status.HTTP_401_UNAUTHORIZED
        err = {
            'err_msg': err_msg,
            'err_code': err_code
        }
        return None, err

    return token_claims, None


def get_current_user(request: Request):
    return request.state.user

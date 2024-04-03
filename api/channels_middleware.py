from django.db import close_old_connections
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import UntypedToken
from .utils import LOGGER, get_user


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        try:
            query_string_param = dict(k_v.split('=') for k_v in scope['query_string'].decode("utf-8").split("&"))
            if query_string_param.get('token'):
                token = query_string_param.get('token')
            else:
                raise Exception("Invalid token type")
            untyped_token = UntypedToken(token).payload
            scope['user'] = await get_user(untyped_token.get('user_id'))

        except Exception as e:
            LOGGER.error(e)
            return None

        return await super().__call__(scope, receive, send)


from channels.auth import AuthMiddlewareStack

def JWTAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
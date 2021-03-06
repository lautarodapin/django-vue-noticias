from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from users.models import User
from channels.db import database_sync_to_async


# @database_sync_to_async
# def get_user(scope):
#     if scope["subprotocols"].__len__() > 0:
#         token = Token.objects.get(key=scope["subprotocols"][0])
#         if token:
#             return token.user
#     return AnonymousUser()

# class TokenAuthMiddleware:
#     """
#     Token authorization middleware for Django Channels 3
#     """

#     def __init__(self, inner):
#         self.inner = inner

#     async def __call__(self, scope, receive, send):
#         scope["user"] = await get_user(scope)
#         return await self.inner(scope, receive, send)

@database_sync_to_async
def get_user(scope):
    ''' Utiliza el query string para ver el token
    '''
    if scope["query_string"].__len__() > 0:
        _, token = scope["query_string"].decode().split("=")
        if token:
            token = Token.objects.get(key=token)
            if token:
                return token.user
    return AnonymousUser()

class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 3
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        scope["user"] = await get_user(scope)
        return await self.inner(scope, receive, send)
# channels_middleware.py
from channels.middleware import BaseMiddleware
from rest_framework.exceptions import AuthenticationFailed
from django.db import close_old_connections
from accounts.tokenauthentication import JWTAuthentication

class JWTWebSocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()  # Close database connections before processing

        # Extract the token from the query string
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_parameters = dict(qp.split("=") for qp in query_string.split("&"))
        token = query_parameters.get("token", None)

        if token is None:
            # Token not provided, reject the connection
            await send({
                "type": "websocket.close",
                "code": 4000,
            })
            return

        # Authenticate the user using your JWTAuthentication class
        authentication = JWTAuthentication()
        try:
            user = await authentication.authenticate_websocket(scope, token)
            if user is not None:
                # Attach the authenticated user to the scope
                scope["user"] = user
            else:
                # Token is invalid, reject the connection
                await send({
                    "type": "websocket.close",
                    "code": 4001,
                })
                return

            # Continue processing the WebSocket
            return await super().__call__(scope, receive, send)

        except AuthenticationFailed:
            # Token authentication failed, reject the connection
            await send({
                "type": "websocket.close",
                "code": 4002,
            })


import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

import notifications.routing
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter(
#     {
#         "http" : django_asgi_app, 
#         "websocket" : URLRouter(
#                 chat.routing.websocket_urlpatterns
#             )    
        
#     }
# )

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    notifications.routing.websocket_urlpatterns
                    + chat.routing.websocket_urlpatterns
                )
            )
        ),
    }
)
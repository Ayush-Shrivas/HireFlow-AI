import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django_application = get_asgi_application()

try:
    from channels.routing import ProtocolTypeRouter, URLRouter
    from config.routing import websocket_urlpatterns

    application = ProtocolTypeRouter({"http": django_application, "websocket": URLRouter(websocket_urlpatterns)})
except ModuleNotFoundError:
    application = django_application

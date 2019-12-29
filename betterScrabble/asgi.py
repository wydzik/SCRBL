from channels.routing import get_default_application
import django
django.setup()

application = get_default_application()
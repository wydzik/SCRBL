import os
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "betterScrabble.settings")

application = get_default_application()
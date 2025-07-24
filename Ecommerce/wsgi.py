import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')

# Initialize Django
django.setup()

# Run migrations automatically on startup (Render workaround)
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as e:
    print("Migration error:", e)

application = get_wsgi_application()

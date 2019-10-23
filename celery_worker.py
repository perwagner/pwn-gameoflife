import os
from app import celery, create_app
 
app = create_app(os.getenv('ENV') or 'local')
app.app_context().push()
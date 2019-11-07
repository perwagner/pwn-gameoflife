#!/usr/bin/env python
import os
from application import celery, create_app
 
app = create_app(os.getenv('ENV') or 'local')
app.app_context().push()
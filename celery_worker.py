#!/usr/bin/env python
import logging
import os

from application import celery, create_app
 

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

ENV = os.getenv('ENV')
logger.info(f"Env in worker: {ENV}")
app = create_app(ENV or 'local')
app.app_context().push()
from descope import DescopeClient

from settings import env_settings
from utils.logger import logger

try:
    descope_client = DescopeClient(project_id=env_settings.descope_id)
    logger.info(f'Descope client initialized - {descope_client}')
except Exception as error:
    logger.error(f"Failed to initialize descope. Error: {error}")

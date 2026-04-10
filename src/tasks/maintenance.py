from celery_app import celery_app, get_setup_utils
from helpers.config import get_settings
import asyncio
from utils.idempotency_manager import IdempotencyManager

import logging

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    name="tasks.maintenance.clean_celery_executions_table",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 60},
)
def clean_celery_executions_table(self):
    return asyncio.run(_clean_celery_executions_table(self))


async def _clean_celery_executions_table(self):
    db_engine, vectordb_client = None, None

    try:

        (
            db_engine,
            db_client,
            llm_provider_factory,
            vectordb_provider_factory,
            generation_client,
            embedding_client,
            vectordb_client,
            template_parser,
        ) = await get_setup_utils()

        # Create idempotency manager
        idempotency_manager = IdempotencyManager(db_client, db_engine)

        settings = get_settings()

        # Clean old task records
        deleted_count = await idempotency_manager.cleanup_old_tasks(
            time_retention=settings.CELERY_TASK_TIME_LIMIT
        )

        logger.info(f"Deleted {deleted_count} old task records")

    except Exception as e:
        logger.error(f"Error cleaning up old task records: {str(e)}")
        raise
    finally:
        try:
            if db_engine:
                await db_engine.dispose()
            if vectordb_client:
                await vectordb_client.disconnect()
        except Exception as e:
            logger.error(f"Task failed while cleaning: {str(e)}")

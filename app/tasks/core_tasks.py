import asyncio

from app.core import logger
from app.worker import task_broker

"""
======== DEMO ONLY ========


from datetime import datetime

@task_broker.task(
    schedule=[
        {"cron": "*/1 * * * *", "args": [1]}
    ]
)
async def task_test_log_schedule(value: int) -> int:
    cur_date = datetime.now().isoformat()
    logger.info(f"Task test_log_schedule({value}) at {cur_date}")
    return value + 1
"""


@task_broker.task(task_name="tasks:task_speak")
async def task_speak(
    word: str,
) -> str:
    await asyncio.sleep(5)
    return f"I say, {word}!"


@task_broker.task(task_name="tasks:task_request_to_delete_user")
def task_request_to_delete_user(user_id: str) -> None:
    # TODO: Send email to user to confirm deletion
    # TODO: flag user as pending delete.
    logger.info(
        f"User({user_id}) requested to delete their account."
    )  # pragma: no cover


@task_broker.task(task_name="tasks:task_request_to_delete_client")
def task_request_to_delete_client(user_id: str, client_id: str) -> None:
    # TODO: Send email to client admin emails to confirm deletion
    # TODO: flag client as pending delete.
    logger.info(
        f"User({user_id}) requested to delete the Client({client_id})."
    )  # pragma: no cover

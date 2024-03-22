from app.broker import broker
from app.core.logger import logger


@broker.task(task_name="tasks:task_speak")
def task_speak(
    word: str,
) -> str:
    return f"I say, {word}!"


@broker.task(task_name="tasks:task_request_to_delete_user")
def task_request_to_delete_user(user_id: str) -> None:
    # TODO: Send email to user to confirm deletion
    # TODO: flag user as pending delete.
    logger.info(
        f"User({user_id}) requested to delete their account."
    )  # pragma: no cover


@broker.task(task_name="tasks:task_request_to_delete_client")
def task_request_to_delete_client(user_id: str, client_id: str) -> None:
    # TODO: Send email to user to confirm deletion
    # TODO: flag client as pending delete.
    logger.info(
        f"User({user_id}) requested to delete the Client({client_id})."
    )  # pragma: no cover

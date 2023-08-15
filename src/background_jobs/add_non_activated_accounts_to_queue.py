from src.user.user_repo import UserRepo, IUserRepo
from datetime import datetime, timedelta
from pika import BlockingConnection, ConnectionParameters
import json


async def add_non_activated_accounts_to_queue(user_repo: IUserRepo = UserRepo()):
    expiration = datetime.utcnow() - timedelta(hours=24)
    expired_users = user_repo.find_non_activated_accounts(expiration=expiration)
    connection = BlockingConnection(ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="non-activated")
    channel.basic_publish(
        exchange="", routing_key="non-activated", body=json.dumps(expired_users)
    )
    connection.close()

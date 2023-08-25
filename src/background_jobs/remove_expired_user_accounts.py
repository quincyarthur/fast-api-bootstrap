import sys

sys.path.append("/app")

from db.config import async_session
from src.user.user_repo import UserRepo, IUserRepo
from datetime import datetime, timedelta
import asyncio


async def remove_expired_accounts():
    async with async_session() as session:
        user_repo: IUserRepo = UserRepo(db=session)
        expiration = datetime.utcnow() - timedelta(hours=24)
        await user_repo.remove_expired_user_accounts(expiration=expiration)


def sync_remove_expired_accounts():
    asyncio.run(remove_expired_accounts())


if __name__ == "__main__":
    sync_remove_expired_accounts()

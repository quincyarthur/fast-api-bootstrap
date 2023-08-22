import sys
sys.path.append('/app')

from db.config import async_session
from src.user.user_repo import UserRepo, IUserRepo
from datetime import datetime, timedelta
import asyncio

if __name__ == '__main__':
    async def async_main():
        async with async_session() as session:
            user_repo: IUserRepo = UserRepo(db=session)
            expiration = datetime.utcnow() - timedelta(hours=24)
            await user_repo.remove_expired_user_accounts(expiration=expiration)
    asyncio.run(async_main())

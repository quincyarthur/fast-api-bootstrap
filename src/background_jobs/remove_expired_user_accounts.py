from src.user.user_repo import UserRepo, IUserRepo
from datetime import datetime, timedelta


async def remove_expired_user_accounts(user_repo: IUserRepo = UserRepo()):
    expiration = datetime.utcnow() - timedelta(hours=24)
    return await user_repo.remove_expired_user_accounts(expiration=expiration)

from src.user.user_repo import UserRepo, IUserRepo
from datetime import datetime, timedelta

user_repo: UserRepo = UserRepo()
expiration = datetime.utcnow() - timedelta(hours=24)
user_repo.remove_expired_user_accounts(expiration=expiration)

from ..repository.user_repository import User_repository

class User_service:

    def __init__(self):
        self.repo = User_repository()

    def create_user(self, login: str, pwd: str, name: str):
        return self.repo.create_user(login, pwd, name)

    def get_users(self):
        return self.repo.get_users()

    def update_user(self, login: str, new_login: str, pwd: str, name: str):
        return self.repo.update_user(login, new_login, pwd, name)

    def del_user(self, login: str):
        return self.repo.delete_user(login)

    def get_analytics(self, login: str, begin_date: str, end_date: str):
        return self.repo.get_analytics(login, begin_date, end_date)
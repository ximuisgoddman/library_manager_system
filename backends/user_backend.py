from django.contrib.auth.backends import BaseBackend
from users.models import MyUser


class UserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            myuser = MyUser.objects.get(username=username)
            print("@@password:", password)
            if myuser.check_password(password):
                return myuser
            else:
                print("error user password")
        except Exception as e:
            print("user no exist", e)
            return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except Exception as e:
            return None

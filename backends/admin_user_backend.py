from django.contrib.auth.backends import BaseBackend
from admin_users.models import AdminUser


class AdminUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            myuser = AdminUser.objects.get(username=username)
            if myuser.check_password(password):
                return myuser
        except AdminUser.DoesNotExist as e:
            print("admin user no exist", e)
            return None

    def get_user(self, user_id):
        try:
            return AdminUser.objects.get(pk=user_id)
        except AdminUser.DoesNotExist:
            return None

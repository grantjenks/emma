import getpass

from django.contrib.auth import login
from django.contrib.auth.models import User


def login_user(get_response):
    def middleware(request):
        if not request.user.is_authenticated:
            username = getpass.getuser()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_superuser(username)
            login(request, user)
        response = get_response(request)
        return response
    return middleware

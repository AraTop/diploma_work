from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from users.forms import UserForm, UserProfileForm
from users.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/users_register.html'
    success_url = '/users/login/'


@method_decorator(login_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        channel = user.channel
        user.delete()

        if channel:
            channel.delete()
        return user


@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

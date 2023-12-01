from django.shortcuts import render


class AuthorSubPermissionsMixin:
    def has_permissions(self):
        obj = self.get_object()
        return obj.channel == self.request.user.channel

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return render(request, 'main/access_denied.html')
        return super().dispatch(request, *args, **kwargs)

from django.shortcuts import render


class AuthorPermissionsMixin:
    def has_permissions(self):
        obj = self.get_object()
        return obj == self.request.user.channel
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return render(request, 'main/access_denied.html')
        return super().dispatch(request, *args, **kwargs)


class AuthorSubPermissionsMixin:
    def has_permissions(self):
        obj = self.get_object()
        return obj.channel == self.request.user.channel
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return render(request, 'main/access_denied.html')
        return super().dispatch(request, *args, **kwargs)


class AuthorPostPermissionsMixin:
    def has_permissions(self):
        obj = self.get_object()
        return obj.channel == self.request.user.channel
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return render(request, 'main/access_denied.html')
        return super().dispatch(request, *args, **kwargs)


class AuthorCommentPermissionsMixin:
    def has_permissions(self):
        obj = self.get_object()
        return obj.user == self.request.user.nickname
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return render(request, 'main/access_denied.html')
        return super().dispatch(request, *args, **kwargs)
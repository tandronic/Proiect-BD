from django.shortcuts import redirect


class LogInMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        elif request.user.is_superuser:
            return redirect('admin:index')
        return super(LogInMixin, self).dispatch(request, *args, **kwargs)

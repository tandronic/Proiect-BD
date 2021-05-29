import datetime
import debug_toolbar


from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path, reverse_lazy
from django.views.i18n import JavaScriptCatalog
from django.views.decorators.http import last_modified
from django.contrib.auth.models import Group
from django.contrib.auth import views as auth_views

from administration.views import HomePageView, LoginPageView, RegisterView, \
    EditProfileView

last_modified_date = datetime.datetime.now()

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit-profile/<int:pk>', EditProfileView.as_view(), name='edit-profile'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='administration/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='administration/password_reset.html',
        email_template_name='administration/password_reset_email.html',
        subject_template_name='administration/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='administration/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
                template_name='administration/password_reset_complete.html'),
        name='password_reset_complete'),
    path('admin/', admin.site.urls, name='admin'),
    path('', include(('appointments.urls', 'appointments'), namespace='appointments')),
]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', last_modified(lambda req, **kw: last_modified_date)(
        JavaScriptCatalog.as_view()), name='javascript-catalog'),
]

admin.site.site_header = "Administrare Pacienti"
admin.site.site_title = "Administrare Pacienti"
admin.site.index_title = "Bine ai venit!"

admin.site.unregister(Group)

admin.site.site_url = '/'

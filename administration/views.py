from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import Http404
from django.db import connection

from administration.mixins import LogInMixin
from administration.forms import RegisterForm, EditProfileForm
from appointments.models import Appointments
from appointments.query import AppointmentsQuery
from users.models import User
from users.query import UserQuery


class HomePageView(LogInMixin, ListView):
    def get_template_names(self):
        if self.request.user.is_patient:
            return 'administration/home-patient.html'
        return 'administration/home-medic.html'

    def get_queryset(self):
        if self.request.user.is_patient:
            return Appointments.objects.raw(
                AppointmentsQuery.GET_PATIENT_APPOINTMENTS.format(patient_id=self.request.user.pk))
        return Appointments.objects.raw(
            AppointmentsQuery.GET_MEDIC_APPOINTMENTS.format(medic=self.request.user.pk))

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        with connection.cursor() as cursor:
            if self.request.user.is_patient:
                cursor.execute(
                    AppointmentsQuery.GET_PATIENT_APPOINTMENTS_NUMBER.format(patient_id=self.request.user.pk)
                )
            else:
                cursor.execute(
                    AppointmentsQuery.GET_MEDIC_APPOINTMENTS_NUMBER.format(medic=self.request.user.pk)
                )
            nr_appointments = cursor.fetchone()
            nr_appointments = nr_appointments[0]
        context['nr_appointments'] = nr_appointments
        return context


class LoginPageView(LoginView):
    template_name = 'administration/login.html'
    redirect_authenticated_user = 'home'


class RegisterView(CreateView):
    template_name = 'administration/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.is_patient = True
        obj.set_password(form.cleaned_data['password'])
        obj.is_active = True
        mail_subject = "Date cont Administare pacienti"
        context_data = {
            'user': obj,
        }
        html_message = render_to_string(
            'administration/register_email.html', context_data)

        plain_message = strip_tags(html_message)
        send_mail(
            mail_subject, plain_message, settings.EMAIL_HOST_USER,
            [obj.email], html_message=html_message)
        obj.save()
        return super().form_valid(form)


class EditProfileView(LogInMixin, UpdateView):
    template_name = 'administration/edit-profile.html'
    form_class = EditProfileForm
    success_url = '/'

    def get_object(self, *args, **kwargs):
        user = User.objects.raw(UserQuery.GET_USER.format(pk=self.kwargs['pk']))
        if len(user) == 0:
            raise Http404('No matches the given query.')
        return user[0]


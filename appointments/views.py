import datetime

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import Http404, HttpResponseRedirect
from django.db import connection

from administration.mixins import LogInMixin
from appointments.models import Appointments
from appointments.forms import AppointmentsForm, MedicAppointmentsForm
from appointments.query import AppointmentsQuery
from users.models import User
from users.query import UserQuery


class CreateAppointmentView(LogInMixin, CreateView):
    template_name = 'appointments/create-appointment.html'
    form_class = AppointmentsForm
    success_url = '/'

    def form_valid(self, form):
        scheduled = form.cleaned_data['scheduled_datetime']
        with connection.cursor() as cursor:
            cursor.execute(
                    AppointmentsQuery.CHECK_APPOINTMENTS_SCHEDULE.format(
                        medic_id=form.cleaned_data['medic'].pk,
                        patient_id=self.request.user.pk,
                        day=scheduled.day
                    )
                )
            data = cursor.fetchone()
        if data and data[0] == 1:
            form.add_error("scheduled_datetime", "Exista deja o programare creata in aceasta zi")
            return super().form_invalid(form)
        obj = form.save(commit=False)
        obj.patient = self.request.user
        mail_subject = "Consultatie creata"
        html_message_patient = render_to_string('appointments/appointment_create_email.html',
                                        {'appointment': obj})
        html_message_medic = render_to_string('appointments/appointment_create_medic_email.html',
                                                {'appointment': obj})
        plain_message_patient = strip_tags(html_message_patient)
        plain_message_medic = strip_tags(html_message_medic)
        send_mail(
            mail_subject, plain_message_patient, settings.EMAIL_HOST_USER,
            [obj.patient.email], html_message=html_message_patient)
        send_mail(
            mail_subject, plain_message_medic, settings.EMAIL_HOST_USER,
            [obj.medic.email], html_message=html_message_medic)
        obj.save()
        return super().form_valid(form)


class EditAppointmentView(LogInMixin, UpdateView):
    template_name = 'appointments/create-appointment.html'
    form_class = AppointmentsForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        appointment = self.get_object()
        if appointment.status != Appointments.IN_PROGRESS:
            return redirect('appointments:patient-appointment-view', pk=appointment.pk)
        return super(EditAppointmentView, self).dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        appointments = Appointments.objects.raw(AppointmentsQuery.GET_APPOINTMENT.format(pk=self.kwargs['pk']))
        if len(appointments) == 0:
            raise Http404('No matches the given query.')
        return appointments[0]

    def form_valid(self, form):
        old_object = self.get_object()
        obj = form.save(commit=False)
        with connection.cursor() as cursor:
            cursor.execute(
                    AppointmentsQuery.UPDATE_APPOINTMENT.format(
                        medic_id=obj.medic.pk,
                        patient_id=self.request.user.pk,
                        scheduled=obj.scheduled_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        description=obj.description,
                        disease_id=obj.disease_id,
                        status=obj.status,
                        treatment=obj.treatment,
                        pk=obj.pk
                    )
                )
            old_symptoms = old_object.symptoms.values_list('pk', flat=True)
            new_symptoms = [symptom.pk for symptom in form.cleaned_data['symptoms']]
            symptoms_to_delete = list(set(old_symptoms) - set(new_symptoms))
            symptoms_to_add = list(set(new_symptoms) - set(old_symptoms))
            if symptoms_to_delete:
                for pk in symptoms_to_delete:
                    cursor.execute(
                        AppointmentsQuery.DELETE_APPOINTMENTS_SYMPTOMS_BY_SYMPTOMS.format(
                            appointment_pk=obj.pk,
                            symptom_pk=pk
                        )
                    )
            if symptoms_to_add:
                for pk in symptoms_to_add:
                    cursor.execute(
                        AppointmentsQuery.INSERT_SYMPTOMS.format(
                            appointment_pk=obj.pk,
                            symptom_pk=pk
                        )
                    )
        return HttpResponseRedirect(self.get_success_url())


class DeleteAppointmentView(LogInMixin, DeleteView):
    model = Appointments
    success_url = '/'

    def get_object(self, *args, **kwargs):
        appointments = Appointments.objects.raw(AppointmentsQuery.GET_APPOINTMENT.format(pk=self.kwargs['pk']))
        if len(appointments) == 0:
            raise Http404('No matches the given query.')
        return appointments[0]

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        mail_subject = "Consultatie anulata"
        html_message = render_to_string('appointments/appointment_delete_email.html',
                                        {'appointment': appointment})
        plain_message = strip_tags(html_message)
        send_mail(
            mail_subject, plain_message, settings.EMAIL_HOST_USER,
            [appointment.patient.email, appointment.medic.email], html_message=html_message)
        with connection.cursor() as cursor:
            cursor.execute(
                AppointmentsQuery.DELETE_APPOINTMENTS_SYMPTOMS.format(pk=appointment.pk)
            )
            cursor.execute(
                AppointmentsQuery.DELETE_APPOINTMENTS.format(pk=appointment.pk)
            )
        return HttpResponseRedirect(self.success_url)


class MedicDailyAppointmentView(LogInMixin, ListView):
    template_name = 'appointments/medic-daily-appointment.html'

    def get_queryset(self):
        date = self.kwargs['date']
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        return Appointments.objects.filter(scheduled_datetime__day=date.day) \
            .order_by('scheduled_datetime')


class MedicEditAppointmentView(LogInMixin, UpdateView):
    template_name = 'appointments/medic-edit-appointment.html'
    form_class = MedicAppointmentsForm
    success_url = '/'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Appointments, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(MedicEditAppointmentView, self).get_context_data(**kwargs)
        patient = self.get_object().patient
        context['appointments'] = patient.appointmentspatient \
            .filter(status=Appointments.RESOLVED).exclude(pk=self.kwargs['pk'])
        context['appointment'] = self.get_object()
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.status = Appointments.RESOLVED
        mail_subject = "Rezultat consultatie"
        html_message = render_to_string('appointments/appointment_email.html',
                                        {'appointment': obj})
        plain_message = strip_tags(html_message)
        send_mail(
            mail_subject, plain_message, settings.EMAIL_HOST_USER,
            [obj.patient.email], html_message=html_message)
        obj.save()
        return super().form_valid(form)


class PatientsView(LogInMixin, ListView):
    template_name = 'appointments/view-patients.html'

    def get_queryset(self):
        return Appointments.objects.raw(AppointmentsQuery.GET_MEDIC_APPOINTMENTS.format(medic=self.request.user.pk))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PatientsView, self).get_context_data(**kwargs)
        patients = []
        for appointment in self.get_queryset():
            if appointment.patient not in patients:
                patients.append(appointment.patient.pk)
        search = self.request.GET.get('q')
        filters = {'pk': ','.join([str(p) for p in patients])}
        if search:
            filters['filters'] = f"AND cnp='{search}'"
        else:
            filters['filters'] = ""
        context['patients'] = User.objects.raw(AppointmentsQuery.GET_PATIENTS.format(**filters))
        return context


class PatientsHistoryAppointsView(LogInMixin, ListView):
    template_name = 'appointments/patient-appointments-history.html'

    def get_queryset(self):
        user = User.objects.raw(UserQuery.GET_USER.format(pk=self.kwargs['pk']))
        if len(user) == 0:
            raise Http404('No matches the given query.')
        return user[0]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PatientsHistoryAppointsView, self).get_context_data(**kwargs)
        patient = self.get_queryset()
        context['appointments'] = Appointments.objects.raw(
            AppointmentsQuery.GET_PATIENT_APPOINTMENTS_WITH_STATUS.format(
                patient_id=patient.pk, status=Appointments.RESOLVED))
        return context


class PatientsAppointsViewOnly(LogInMixin, DetailView):
    template_name = 'appointments/patient-view-appointment.html'

    def get_object(self, *args, **kwargs):
        appointments = Appointments.objects.raw(AppointmentsQuery.GET_APPOINTMENT.format(pk=self.kwargs['pk']))
        if len(appointments) == 0:
            raise Http404('No matches the given query.')
        return appointments[0]

    def get_context_data(self, **kwargs):
        context = super(PatientsAppointsViewOnly, self).get_context_data(**kwargs)
        context['appointment'] = self.get_object()
        return context

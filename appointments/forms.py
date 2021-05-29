import datetime
import pytz

from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from django.db.models import Q

from appointments.models import Appointments


class AppointmentsForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ('medic', 'scheduled_datetime', 'description', 'disease', 'symptoms')
        widgets = {
            'scheduled_datetime': DateTimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentsForm, self).__init__(*args, **kwargs)
        self.fields['medic'].queryset = self.fields['medic'].queryset.exclude(Q(is_patient=True) | Q(is_superuser=True))

    def clean_scheduled_datetime(self):
        scheduled_datetime = self.cleaned_data.get('scheduled_datetime')
        scheduled_datetime_start = scheduled_datetime - datetime.timedelta(minutes=30)
        medic = self.cleaned_data.get('medic')
        now = datetime.datetime.now(pytz.timezone('Europe/Bucharest'))
        start_program = scheduled_datetime.replace(hour=10, minute=0, second=0, microsecond=0)
        end_program = scheduled_datetime.replace(hour=16, minute=0, second=0, microsecond=0)
        if scheduled_datetime <= now:
            raise forms.ValidationError("Nu se poate selecta o data din trecut")
        if scheduled_datetime < start_program or scheduled_datetime > end_program:
            raise forms.ValidationError("Intervalul orar pentru programari este 10:00-16:00")
        if scheduled_datetime.isoweekday() not in range(1, 5):
            raise forms.ValidationError("Programarile se pot realiza de Luni pana Vineri")
        if self.instance.pk:
            appointment = Appointments.objects \
                .filter(medic=medic, scheduled_datetime__range=[scheduled_datetime_start, scheduled_datetime]) \
                .exclude(pk=self.instance.pk).exists()
        else:
            appointment = Appointments.objects \
                .filter(medic=medic, scheduled_datetime__range=[scheduled_datetime_start, scheduled_datetime]) \
                .exists()
        if appointment:
            raise forms.ValidationError("Data si ora programarii nu sunt disponibile")
        return scheduled_datetime


class MedicAppointmentsForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ('treatment',)

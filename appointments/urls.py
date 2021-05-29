import datetime

from django.urls import path

from appointments.views import CreateAppointmentView, EditAppointmentView, \
    MedicDailyAppointmentView, MedicEditAppointmentView, PatientsView, DeleteAppointmentView, \
    PatientsHistoryAppointsView, PatientsAppointsViewOnly

last_modified_date = datetime.datetime.now()

urlpatterns = [
    path('appointment/create/', CreateAppointmentView.as_view(), name='create-appointment'),
    path('appointment/edit/<int:pk>', EditAppointmentView.as_view(), name='edit-appointment'),
    path('appointment/delete/<int:pk>', DeleteAppointmentView.as_view(), name='delete-appointment'),
    path('medic-appointment/edit/<int:pk>', MedicEditAppointmentView.as_view(), name='medic-edit-appointment'),
    path('patient-appointments/<int:pk>', PatientsHistoryAppointsView.as_view(), name='patient-appointments'),
    path('patient-appointment-view/<int:pk>', PatientsAppointsViewOnly.as_view(), name='patient-appointment-view'),
    path('medic-appointments/<slug:date>', MedicDailyAppointmentView.as_view(), name='medic-appointments'),
    path('patients/', PatientsView.as_view(), name='patients'),
]



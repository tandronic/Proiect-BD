from django.contrib import admin

from appointments.models import Appointments, Diseases, Symptoms


@admin.register(Appointments)
class Appointments(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'get_cnp', 'get_email',
                    'get_phone', 'scheduled_datetime', 'status')
    search_fields = ('patient__first_name', 'patient__last_name',
                     'medic__first__name', 'medic__last__name',
                     'patient__cnp')
    list_filter = ('disease', 'status')
    autocomplete_fields = ('patient', 'medic')

    def get_first_name(self, obj):
        return obj.patient.first_name

    get_first_name.short_description = 'first name'
    get_first_name.admin_order_field = 'patient__first_name'

    def get_last_name(self, obj):
        return obj.patient.last_name

    get_last_name.short_description = 'last name'
    get_last_name.admin_order_field = 'patient__last_name'

    def get_cnp(self, obj):
        return obj.patient.cnp

    get_cnp.short_description = 'cnp'
    get_cnp.admin_order_field = 'patient__cnp'

    def get_email(self, obj):
        return obj.patient.email

    get_email.short_description = 'email'
    get_email.admin_order_field = 'patient__email'

    def get_phone(self, obj):
        return obj.patient.phone

    get_phone.short_description = 'phone'
    get_phone.admin_order_field = 'patient__phone'


@admin.register(Diseases)
class DiseasesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Symptoms)
class SymptomsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

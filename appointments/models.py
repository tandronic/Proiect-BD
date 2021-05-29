import datetime
import pytz

from django.db import models

from users.models import User


class Diseases(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = "diseases"
        verbose_name_plural = "diseases"

    def __str__(self):
        return self.name


class Symptoms(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "symptoms"
        verbose_name_plural = "symptoms"

    def __str__(self):
        return self.name


class Appointments(models.Model):
    IN_PROGRESS = 1
    RESOLVED = 2
    CANCELED = 3

    STATUS_CHOICES = (
        (IN_PROGRESS, "In desfasurare"),
        (RESOLVED, "Incheiat"),
        (CANCELED, "Anulat")
    )

    patient = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='appointmentspatient', verbose_name='Pacient')
    medic = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='appointmentsmedic', verbose_name='Medic')
    scheduled_datetime = models.DateTimeField(verbose_name='Data programarii')
    description = models.TextField(
        help_text="Scurta prezentare de ce doriti aceasta programare ...", verbose_name='Descriere')

    created_date = models.DateTimeField(auto_now_add=True)
    disease = models.ForeignKey(
        Diseases, on_delete=models.SET_NULL, null=True, verbose_name='Boala')
    symptoms = models.ManyToManyField(Symptoms, blank=True, verbose_name='Simptome')
    status = models.IntegerField(choices=STATUS_CHOICES, default=IN_PROGRESS)
    treatment = models.TextField(
        help_text="Tratament", verbose_name='Tratament', null=True, blank=True)

    class Meta:
        db_table = "appointments"
        verbose_name_plural = "appointments"

    def __str__(self):
        return self.patient.cnp

    @property
    def can_be_cancelled(self):
        now = datetime.datetime.now(pytz.timezone('Europe/Bucharest'))
        return self.scheduled_datetime <= now or self.status != self.IN_PROGRESS

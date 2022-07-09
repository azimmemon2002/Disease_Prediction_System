from django.contrib import admin
from .models import patient, doctor, diseaseinfo, consultation, ratingreview
# Register your models here.


def patient_name(patient):
    try:
        return patient.patient.name
    except Exception as e:
        print(e)
        return patient.patient

    #   foregine key >> patient >> name


def doctor_name(doctor):
    return doctor.doctor.name


def diseasename(diseaseinfo):
    return diseaseinfo.diseaseinfo.diseasename


class patientdisplay(admin.ModelAdmin):
    list_display = ("user", "name", "dob", "gender",)


class doctordisplay(admin.ModelAdmin):
    list_display = ("user", "name", "specialization", "gender", "rating")


class diseasedisplay(admin.ModelAdmin):

    list_display = (patient_name, "diseasename", "symptomsname", "confidence_score", "consultdoctor")


class consultdisplay(admin.ModelAdmin):
    list_display = (patient_name, doctor_name, diseasename, "consultation_date", "status")


class ratingdisplay(admin.ModelAdmin):
    list_display = (patient_name, doctor_name, "rating", "review")


admin.site.register(patient, patientdisplay)
admin.site.register(doctor, doctordisplay)
admin.site.register(diseaseinfo, diseasedisplay)
admin.site.register(consultation, consultdisplay)
admin.site.register(ratingreview, ratingdisplay)

from django.urls import include, path, re_path
from . import views
from django.contrib import admin




urlpatterns = [

    # ======= Testing urls ==========
    path("basic/", views.basic, name="basic"), #Test
    path("about", views.about, name="about"), #Test


    # ======= HoMe InDeX ==========
    path("", views.index, name="home"),   


    # ======= Admin urls ==========
    path("admin_ui", views.admin_ui, name="admin_ui"),
    
    
    # ======= Doctors urls ==========
    path('doctor_ui', views.doctor_ui , name='doctor_ui'),
    path('dviewprofile/<str:doctorusername>', views.dviewprofile , name='dviewprofile'),


    # ======= patients urls ==========
    path('patient_ui', views.patient_ui , name='patient_ui'),
    path('pviewprofile/<str:patientusername>', views.pviewprofile , name='pviewprofile'),


    # ======= Disease_predict ========
    path('predict_disease', views.predict_disease, name='predict_disease'),


    # ======= Consultations ========
    path('consult_doctor', views.consultdoctor, name='consultdoctor'),
    path('Consultations/<str:doctorusername>', views.create_Consultation, name='create_Consultation'),
    path('viewconsultation/<int:consultation_id>', views.viewconsultation , name='viewconsultation'),
    path('close_consultation/<int:consultation_id>', views.close_consultation , name='close_consultation'),


    # ======= Consultations Histroy ========
    path('pconsultation_history/<str:patientusername>', views.pconsultation_history , name='pconsultation_history'),
    path('dconsultation_history/<str:doctorusername>', views.dconsultation_history , name='dconsultation_history'),


    # ======= rate review ========
    path('rating_review/<int:consultation_id>', views.rating_review , name='rating_review'),


    # ======= chat links ========
    path('post', views.post, name='post'),
    path('chat_messages', views.chat_messages, name='chat_messages'),





]

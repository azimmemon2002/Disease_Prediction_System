from django.urls import path, re_path
from . import views

urlpatterns = [
    # |=============================== Logout urls ==================================|

    path('',views.logout, name="logout"),
    

    # |=============================== Sign in urls =================================|

    path("sign_in_admin", views.sign_in_Admin, name="sign_in_admin"),
    path("sign_in_patient", views.sign_in_Patient, name="sign_in_patient"),
    path("sign_in_doctor", views.sign_in_Doctor, name="sign_in_doctor"),

 
    # |=============================== Sign up urls =================================|
   
    path("sign_up_patient", views.sign_up_Patient, name="sign_up_patient"),
    path("sign_up_doctor", views.sign_up_Doctor, name="sign_up_doctor"),

    # |=========================== Save Data to Database ============================|

    path('savePdata', views.savePdata , name='savePdata'),
    path('saveDdata', views.saveDdata , name='saveDdata'),
    
]


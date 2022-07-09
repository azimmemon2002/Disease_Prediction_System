# from datetime import datetime
# from django.contrib import messages
import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse

from django.contrib.auth.models import User, auth
from app.models import doctor,diseaseinfo,consultation,ratingreview
from chat_system.models import Chat

from pandas import read_csv
import joblib as jb
import datetime as dt


model_path = './app/trained_model/mnb.joblib'
model = jb.load(model_path)



def basic(request):
    return render(request, "basic.html")  # test


def index(request):
    if request.method == "GET":
        try:
            hour = int(dt.datetime.now().hour)
            if 0 <= hour < 12:
                message = "Good morning"

            elif 12 <= hour < 18:
                message = "Good afternoon"

            else:
                message = "Good evening"
        except Exception as e:
            print(e)
        return render(request, "homepage/index.html",{"gretings":message})
    else:
        return HttpResponse("Something Went Wrong!")


def about(request):
    if request.method == "GET":
        return render(request, "aboutpage/about.html")
    else:
        return HttpResponse("Something Went Wrong!")



def admin_ui(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                hour = int(dt.datetime.now().hour)
                if 0 <= hour < 12:
                    message = "Good morning"

                elif 12 <= hour < 18:
                    message = "Good afternoon"

                else:
                    message = "Good evening"
            except Exception as e:
                print(e)
            
            return render(request, 'admin/admin_ui/admin_ui.html',{"gretings":message})
        else:
            return redirect('home')

                


def doctor_ui(request):
    if request.method == 'GET':

        if request.user.is_authenticated:

            doctorid = request.session['doctorusername']
            duser = User.objects.get(username=doctorid)

            return render(request, 'doctor/doctor_ui/profile.html', {"duser": duser})

        else:
            return redirect('home')

    if request.method == 'POST':

        return render(request, 'doctor/doctor_ui/profile.html')


def dviewprofile(request, doctorusername):
    if request.method == 'GET':
        status = False
        duser = User.objects.get(username=doctorusername)
        print(duser)
        print(request.user)


        if request.user == duser:
            status = True
            print(status)
            return render(request, 'doctor/view_profile/profile.html', {"duser": duser,"statue":status})
        else:
            print(status)
            return render(request, 'doctor/view_profile/profile.html', {"duser": duser,"status":status})


def patient_ui(request):
    if request.method == 'GET':

        if request.user.is_authenticated:

            patientusername = request.session['patientusername']
            puser = User.objects.get(username=patientusername)

            return render(request, 'patient/patient_ui/profile.html', {"puser": puser})

        else:
            return redirect('home')

    if request.method == 'POST':

        return render(request, 'patient/patient_ui/profile.html')


def pviewprofile(request, patientusername):
    
    if request.method == 'GET':
        status = False
        puser = User.objects.get(username=patientusername)

        if request.user == puser:
            status = True
            print(status)
            return render(request, 'patient/view_profile/profile.html', {"puser": puser,"statue":status})
        else:
            print(status)
            return render(request, 'patient/view_profile/profile.html', {"puser": puser,"status":status})


def predict_disease(request):

    disease_file = './app/data/disease.csv'
    
    data = read_csv(disease_file)
    symptomslist = data["Disease List"].tolist()
    
    if request.method == 'GET':
    
        return render(request, "patient\predictdisease\predict_disease.html", {"Symptoms": symptomslist})
    
    if request.method == 'POST':

        default_disease_values = './app/data/defaults.csv'
        dict_names = './app/data/dict_names.csv'


        symptom_no = int(request.POST["noofsym"])
        print(symptom_no)
        if (symptom_no == 0 ) :
            return JsonResponse({'predicteddisease': "none",'confidencescore': 0 })
    
        else :
            psymptoms = []
            psymptoms = request.POST.getlist("symptoms[]")

            names = {}
            df = read_csv(default_disease_values)
            

            with open(dict_names, mode='r') as inp:
                reader = csv.reader(inp)
                names = {rows[0]:rows[1] for rows in reader}

            for symptom in psymptoms:df[names[symptom]] = 1

            predict = model.predict(df)
            y_pred = model.predict_proba(df)
            confidencescore=y_pred.max() * 100
            print(" confidence score of : = {0} ".format(confidencescore))

            confidencescore = format(confidencescore, '.0f')
            predicted_disease = predict[0]
            print(predicted_disease)

            # get doctor info acoording to disease

            Rheumatologist = ['Osteoarthristis','Arthritis']
       
            Cardiologist = ['Heart attack','Bronchial Asthma','Hypertension ']
        
            ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]

            Orthopedist = []

            Neurologist = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

            Allergist_Immunologist = ['Allergy','Pneumonia',
            'AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']

            Urologist = [ 'Urinary tract infection',
            'Dimorphic hemmorhoids(piles)']

            Dermatologist = [  'Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']

            Gastroenterologist = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
            'Alcoholic hepatitis','Jaundice','hepatitis A',
            'Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']
            
            if predicted_disease in Rheumatologist :
                consultdoctor = "Rheumatologist"
            
            elif predicted_disease in Cardiologist :
                consultdoctor = "Cardiologist"

            elif predicted_disease in ENT_specialist :
                consultdoctor = "ENT specialist"
        
            elif predicted_disease in Orthopedist :
                consultdoctor = "Orthopedist"
        
            elif predicted_disease in Neurologist :
                consultdoctor = "Neurologist"
        
            elif predicted_disease in Allergist_Immunologist :
                consultdoctor = "Allergist/Immunologist"
        
            elif predicted_disease in Urologist :
                consultdoctor = "Urologist"
        
            elif predicted_disease in Dermatologist :
                consultdoctor = "Dermatologist"
        
            elif predicted_disease in Gastroenterologist :
                consultdoctor = "Gastroenterologist"
        
            else :
                consultdoctor = "other"


            request.session['doctortype'] = consultdoctor 

            try:
                patientusername = request.session['patientusername']
                puser = User.objects.get(username=patientusername)
            except Exception as e:
                print(e)
            
            
            try:
                patient = puser.patient
            except Exception as e:
                patient = None
                print(e)
            
            diseasename = predicted_disease
            no_of_sym = symptom_no
            symptomsname = psymptoms
            confidence = confidencescore

            diseaseinfo_new = diseaseinfo( 
                patient=patient,
                diseasename=diseasename,
                no_of_symptoms=no_of_sym,
                symptomsname=symptomsname,confidence_score=confidence,consultdoctor=consultdoctor)
            diseaseinfo_new.save() 

            request.session['diseaseinfo_id'] = diseaseinfo_new.id

            
            return JsonResponse({'predicteddisease': predicted_disease ,'confidencescore':confidencescore, 'consultdoctor': consultdoctor})

       
def consultdoctor(request):

    if request.method == 'GET':
        
        doctortype = request.session['doctortype']
        print(doctortype)
        dinfo = doctor.objects.all()

        return render(request,'patient\consultation\consulting_a_doctor.html',{"dinfo":dinfo})
 
       
def create_Consultation(request,doctorusername):

    if request.method == 'POST':
       

        patientusername = request.session['patientusername']
        
        puser = User.objects.get(username=patientusername)
        patient_info = puser.patient
        
        duser = User.objects.get(username=doctorusername)
        doctor_info = duser.doctor
        request.session['doctorusername'] = doctorusername


        diseaseinfo_id = request.session['diseaseinfo_id']
        diseaseinfo_info = diseaseinfo.objects.get(id=diseaseinfo_id)

        consultation_date = dt.date.today()
        status = "active"
        
        consultation_new = consultation(patient=patient_info, doctor=doctor_info, diseaseinfo=diseaseinfo_info, consultation_date=consultation_date,status=status)
        consultation_new.save()

        request.session['consultation_id'] = consultation_new.id
        
        
        print("consultation record is saved sucessfully")
         
        return redirect('viewconsultation',consultation_new.id)


def viewconsultation(request,consultation_id):
   
    if request.method == 'GET':
      request.session['consultation_id'] = consultation_id
      consultation_info = consultation.objects.get(id=consultation_id)

      return render(request,'consultation/consultation.html', {"consultation":consultation_info })


def rating_review(request,consultation_id):
   if request.method == "POST":
         
         consultation_info = consultation.objects.get(id=consultation_id)
         patient = consultation_info.patient
         doctor_info = consultation_info.doctor
         rating = request.POST.get('rating')
         review = request.POST.get('review')

         rating_info = ratingreview(patient=patient,doctor=doctor_info,rating=rating,review=review)
         rating_info.save()

         rate = int(rating_info.rating_is)
         doctor.objects.filter(pk=doctor_info).update(rating=rate)
         

         return redirect('viewconsultation',consultation_id)
         

def close_consultation(request,consultation_id):
   if request.method == "POST":
         
         consultation.objects.filter(pk=consultation_id).update(status="closed")
         
         return redirect('home')


def pconsultation_history(request,patientusername):
    if request.method == 'GET':

      patientusername = request.session['patientusername']
      puser = User.objects.get(username=patientusername)
      patient_info = puser.patient
        
      consultationnew = consultation.objects.filter(patient = patient_info)
      
    
      return render(request,'patient/consultation/consultation_history.html',{"consultation":consultationnew})


def dconsultation_history(request,doctorusername):
    if request.method == 'GET':

      doctorusername = request.session['doctorusername']
      duser = User.objects.get(username=doctorusername)
      doctor_info = duser.doctor
        
      consultationnew = consultation.objects.filter(doctor = doctor_info)
      
    
      return render(request,'doctor/consultation/consultation_history.html',{"consultation":consultationnew})


def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox')

        consultation_id = request.session['consultation_id'] 
        consultation_info = consultation.objects.get(id=consultation_id)

        chat = Chat(consultation_id=consultation_info,sender=request.user, message=msg)

        if msg != '':            
            chat.save()
            print("Message Saved "+ msg )
            return JsonResponse({ 'msg': msg })
        else:
            return HttpResponse('Request must be POST.')


    else:
        return HttpResponse('Request must be POST.')
    

    
def chat_messages(request):    
   if request.method == "GET":

         consultation_id = request.session['consultation_id'] 
         chats = Chat.objects.filter(consultation_id=consultation_id)
         return render(request, 'consultation/chatbox.html', {'chat': chats})


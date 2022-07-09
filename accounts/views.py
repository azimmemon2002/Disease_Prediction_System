from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from app.models import patient, doctor

from datetime import datetime


# Create your views here.

def logout(request):
    auth.logout(request)
    request.session.pop('patientid', None)
    request.session.pop('doctorid', None)
    request.session.pop('adminid', None)
    return render(request, 'homepage\index.html')


# |=========================================== Sign IN Functions ====================================|


def sign_in_Admin(request):
    try:
        if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = auth.authenticate(username=username, password=password)

            try:

                if user is not None:

                    try:
                        if user.is_superuser == True:
                            auth.login(request, user)

                            return redirect('home')

                    except:
                        messages.info(
                            request, 'Please enter the correct username and password for a admin account.')
                        return redirect('sign_in_admin')

            except:
                messages.info(
                    request, 'Please enter the correct username and password for a admin account.')
                return redirect('sign_in_admin')

        elif request.method == "get" or request.method == "GET":
            return render(request, 'admin\signin\signin_admin.html')

    except:
        return render(request, 'admin\signin\signin_admin.html')


# |================================================= Sign In-UP Doctor ===============================================================|


def sign_in_Doctor(request):

    if request.method == 'GET':
        return render(request, 'doctor\signin\signin_doctor.html')

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                if (user.doctor.is_doctor == True):

                    auth.login(request, user)
                    request.session['doctorusername'] = user.username

                    return redirect('doctor_ui')

            except:
                messages.info(request, 'invalid credentials')
                return redirect('sign_in_doctor')

        else:
            messages.info(request, 'invalid credentials')
            return redirect('sign_in_doctor')
    else:
        messages.info(request, "try again")
        return redirect('sign_in_doctor')


def sign_up_Doctor(request):

    if request.method == 'GET':
        return render(request, 'doctor\signup\signup_doctor.html')

    if request.method == "POST":

        if request.POST['username'] and request.POST['name'] and request.POST['email'] and request.POST['dob'] and request.POST['age'] and request.POST['gender'] and request.POST['address'] and request.POST['mobile'] and request.POST['registration_no'] and request.POST['year_of_registration'] and request.POST['qualification'] and request.POST['state_medical_council'] and request.POST['specialization'] and request.POST['password'] and request.POST['re_password']:

            username = request.POST['username']
            name = request.POST['name']
            email = request.POST['email']
            dob = request.POST['dob']
            age = request.POST['age']
            gender = request.POST['gender']
            address = request.POST['address']
            mobile_no = request.POST['mobile']
            registration_no = request.POST['registration_no']
            year_of_registration = request.POST['year_of_registration']
            qualification = request.POST['qualification']
            state_medical_council = request.POST['state_medical_council']
            specialization = request.POST['specialization']

            password = request.POST['password']
            re_password = request.POST['re_password']
            
            if password == re_password:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'username already taken')
                    return redirect('sign_up_doctor')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email already taken')
                    return redirect('sign_up_doctor')

                else:
                    user = User.objects.create_user(
                        username=username, password=password, email=email)
                    user.save()

                    doctornew = doctor(user=user, name=name, dob=dob, gender=gender, age_one=age, address=address, mobile_no=mobile_no, registration_no=registration_no,
                                       year_of_registration=year_of_registration, qualification=qualification, state_medical_council=state_medical_council, specialization=specialization)
                    doctornew.save()
                    messages.info(request, 'user created sucessfully')

                return redirect('sign_in_doctor')
            else:
                messages.info(
                    request, 'password not matching, please try again')
                return redirect('sign_up_doctor')
        else:
            messages.info(
                request, 'Please make sure all required fields are filled out correctly')
            return redirect('sign_up_doctor')


def saveDdata(request):
    if request.method == 'POST':

        name = request.POST['name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        mobile_no = request.POST['mobile_no']
        address = request.POST['address']
        registration_no = request.POST['registration_no']
        year_of_registration = request.POST['year_of_registration']
        qualification = request.POST['qualification']
        state_medical_council = request.POST['state_medical_council']
        specialization = request.POST['specialization']

        dobdate = datetime.strptime(dob, '%Y-%m-%d')
        yor = datetime.strptime(year_of_registration, '%Y-%m-%d')

        doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)

        doctor.objects.filter(pk=duser.doctor).update(name=name, dob=dobdate, gender=gender, address=address, mobile_no=mobile_no, registration_no=registration_no,
                                                      year_of_registration=yor, qualification=qualification, state_medical_council=state_medical_council, specialization=specialization)
        messages.success(request, 'Profile details updated.')

        return redirect('dviewprofile', doctorusername)


# |===================================================== Sign In-UP Patient ======================================================================|


def sign_in_Patient(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if "@" in username:
            user = auth.authenticate(username=User.objects.get(
                email=username).username, password=password)

        if user is not None:
            try:
                if (user.patient.is_patient == True):
                    auth.login(request, user)
                    request.session['patientusername'] = user.username
                    return redirect('patient_ui')

            except:
                messages.info(request, 'invalid credentials')
                return redirect('sign_in_patient')

        else:
            messages.info(request, 'invalid credentials')
            return redirect('sign_in_patient')

    else:
        return render(request, "patient\signin\signin_patient.html")


def sign_up_Patient(request):
    if request.method == 'GET':
        return render(request, "patient\signup\signup_patient.html")

    if request.method == "POST":
        if request.POST['username'] and request.POST['name'] and request.POST['email'] and request.POST['dob'] and \
            request.POST['age'] and request.POST['gender'] and request.POST['address'] and request.POST[
                'mobile'] and request.POST['password'] and request.POST['re_password']:

            username = request.POST['username']
            name = request.POST['name']
            email = request.POST['email']
            dob = request.POST['dob']
            age = request.POST['age']
            gender = request.POST['gender']
            address = request.POST['address']
            mobile_no = request.POST['mobile']
            password = request.POST['password']
            re_password = request.POST['re_password']

            if password == re_password:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "username already taken")
                    return redirect('sign_up_patient')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email already taken')
                    return redirect('sign_up_patient')

                else:
                    user = User.objects.create_user(
                        username=username, password=password, email=email)
                    user.save()

                    patientnew = patient(
                        user=user, name=name, dob=dob, gender=gender, address=address, mobile_no=mobile_no, age_one=age)
                    patientnew.save()
                    messages.info(request, 'user created sucessfully')

                return redirect('sign_in_patient')

            else:
                messages.info(
                    request, 'password not matching, please try again')
                return redirect('sign_up_patient')
        else:
            messages.info(
                request, 'Please make sure all required fields are filled out correctly')
            return redirect('sign_up_patient')


def savePdata(request):
    if request.method == 'POST':

        name = request.POST['name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        address = request.POST['address']
        mobile_no = request.POST['mobile_no']

        dobdate = datetime.strptime(dob, '%Y-%m-%d')

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)

        patient.objects.filter(pk=puser.patient).update(
            name=name, dob=dobdate, gender=gender, address=address, mobile_no=mobile_no)
        messages.success(request, 'Profile details updated.')

        return redirect('pviewprofile', patientusername)

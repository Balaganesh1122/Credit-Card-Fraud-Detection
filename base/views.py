from django.shortcuts import render
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pickle
from playsound import playsound



def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Your password and confirm password do not match!")  # Alert message
        else:
            if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already taken! Please choose another.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered! Please use another email.")
            else:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login')

    return render(request, 'signup.html')
        


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Username or Password is incorrect!")  # Displaying an alert message

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')
@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


def getPredictions(cc_num,category,amt,gender,age,trans_month,trans_year,lat_dis,long_dis):
    model = pickle.load(open('Hybrid.pkl', 'rb'))
    new_data = {'cc_num':cc_num,
            'amt': amt,
            'category':category,
            'gender': gender,
            'age': age,
            'trans_month':trans_month ,
            'trans_year':trans_year,
            'lat_dis': lat_dis,
            'long_dis':long_dis}
    new_df = pd.DataFrame([new_data])
    prediction = model.predict(new_df)
    return prediction
def result(request):
    cc_num = float(request.GET['cc_num'])
    amt = float(request.GET[ 'amt'])
    gender = int(request.GET[ 'gender'])
    age = int(request.GET[ 'age'])
    trans_month = int(request.GET[ 'trans_month'])
    trans_year = int(request.GET[ 'trans_year'])
    lat_dis = float(request.GET[ 'lat_dis'])
    long_dis = float(request.GET[ 'long_dis'])
    category = str(request.GET[ 'category'])
    result = getPredictions(cc_num,category,amt,gender,age,trans_month,trans_year,lat_dis,long_dis)
    if result==0:
        result = "Fraud"
        playsound('2.wav')
    else:
        result= "No Fraud"
    return render(request, 'result.html', {'result': result})
    


from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
import dbConnectionFunctions as db
from userProfile import views
from dashboard import views as dashViews
from sponsor import views as sponViews

def login(request):
    return render(request, 'index.html')

#need to move this to index @app.route('/index/', methods=['GET', 'POST'])
def loginpg(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        correctPassword = db.login(email, password)

        if correctPassword == True:
            request.session['loggedin'] = True
            request.session['id'] = db.getUserID(email)
            request.session['email'] = email
            request.session['role'] = db.getUserType(email)
            request.session['isViewing'] = False

            if request.POST.get('remember') == 'true':
                request.session.set_expiry(0)
            
            return moveout(request)
        else:
            messages.success(request, 'Incorrect Email or Password')
            return render(request, 'index.html')

def logoutpg(request):
    if request.session['isViewing']:
        if request.session['isSponsor']:
            db.removeTempDriver(request.session['tempId'])
            del request.session['tempEmail']
            del request.session['tempId']
        else:
            userType = db.getUserType(request.session['tempId'])

            if userType == 'Driver':
                db.removeTempDriver(request.session['tempId'])
            else:
                db.removeTempSponsor(request.session['tempId'])
            
            del request.session['tempEmail']
            del request.session['tempId']

    del request.session['loggedin']
    del request.session['id']
    del request.session['email']
    del request.session['role']
    del request.session['isSponsor']
    del request.session['isAdmin']
    del request.session['isViewing']
    
    return render(request, 'index.html')

#need to check vs role 
def moveout(request):
    if 'loggedin' in request.session:
        print(request.session.get('role'))
        if request.session.get('role') == 'Driver':
            request.session['isSponsor'] = False
            request.session['isAdmin'] = False

            
            result = db.getDriverOrgs(request.session['id'])
            request.session['orgID'] = result[0][0]
            return dashViews.driverDash(request)

        if request.session.get('role') == 'Sponsor':
            request.session['isSponsor'] = True
            request.session['isAdmin'] = False
            response = redirect('/sponsor_dash/')
            return response

        if request.session.get('role') == 'Admin':
            request.session['isSponsor'] = False
            request.session['isAdmin'] = True

            result = db.getOrgs()
            request.session['adminOrgChoice'] = result[0][0]
            return dashViews.adminDash(request)
    else:
        print('not logged in...displaying login')
        return render(request, 'index.html')

def changepass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if(email != None and email != ''):
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            if(password == cpassword):
                response = db.changePassword(email, password)
            else:
                messages.success(request, 'Passwords do not match')
                return render(request, 'index.html')
        else:
            messages.success(request, 'Incorrect Email')
            return render(request, 'index.html')           

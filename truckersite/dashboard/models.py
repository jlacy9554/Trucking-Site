from django.db import models
import dbConnectionFunctions as db
from dashboard import views
from sponsor import views as spon
from orgPage import views as org

# Create your models here.

def setDriverOrg(request, orgID):
    request.session['orgID'] = orgID
    return views.driverDash(request)

def editAdmin(request):
    admin = request.POST.get('admin')

    if admin != 'none':
        if 'remove' in request.POST:
            db.removeAdmin(admin)
        
        elif 'edit' in request.POST:
            return org.adminEditUser(request, admin)

    return views.adminDash(request)

def addNewAdmin(request):
    email = request.POST.get('email')
    name = request.POST.get('name')

    newPassword = db.getRandomPassword()

    db.createAdmin(name, email, newPassword)

    db.emailNewAdmin(email, newPassword)

    return views.adminDash(request)

def addOrg(request):
    newOrgName = request.POST.get('name')

    db.createOrg(newOrgName)

    return views.adminDash(request)

def removeOrg (request):
    orgNo = request.POST.get('orgID')

    db.removeOrg(orgNo)

    return views.adminDash(request)

def setDriverView(request):
    tempUserName = 'temp'
    email = '@email.com'
    tempEmail = tempUserName + email

    num = 0
    while (db.checkEmail(tempEmail)):
        num += 1
        tempEmail = tempUserName + str(num) + email
    
    request.session['tempEmail'] = tempEmail
    request.session['isViewing'] = True

    request.session['tempId'] = db.createTempDriver(tempEmail, 1)
    
    return views.driverDash(request)

def setSponsorView(request):
    tempUserName = 'temp'
    email = '@email.com'
    tempEmail = tempUserName + email

    num = 0
    while (db.checkEmail(tempEmail)):
        num += 1
        tempEmail = tempUserName + str(num) + email
    
    request.session['tempEmail'] = tempEmail
    request.session['isViewing'] = True

    request.session['tempId'] = db.createTempSponsor(tempEmail, 1)
    
    return spon.sponsorDashDisplay(request)

def revertDriverView(request):
    db.removeTempDriver(request.session['tempId'])
    del request.session['tempEmail']
    del request.session['tempId']

    request.session['isViewing'] = False

    return views.adminDash(request)

def revertSponsorView(request):
    db.removeTempSponsor(request.session['tempId'])
    del request.session['tempEmail']
    del request.session['tempId']

    request.session['isViewing'] = False

    return views.adminDash(request)
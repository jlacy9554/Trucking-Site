from django.db import models
from django.shortcuts import render
import os
import dbConnectionFunctions as db
from orgPage import views
from Catalog import views as CatalogViews

# Create your models here.
def getNewLogo(request):
    newLogo = request.FILES['logo']
    extension = os.path.splitext(newLogo.name)[1]

    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    elif (request.session['isAdmin']):
        orgNo = request.session['adminOrgChoice']
    else:
        orgNo = db.getOrgNo(request.session['email'])

    imgPath = 'static/img/' + 'user' + str(db.getOrgName(orgNo)) + extension
    response = db.setOrgLogo(orgNo, str(db.getOrgName(orgNo)) + extension)

    with open(imgPath, 'wb+') as f:
        for chunk in newLogo.chunks():
            f.write(chunk)

    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def getNewPointChange(request):
    numPoints = request.POST.get('numPoints')
    desc = request.POST.get('description')

    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    elif (request.session['isAdmin']):
        orgNo = request.session['adminOrgChoice']
    else:
        orgNo = db.getOrgNo(request.session['email'])

    db.addPointChangeReason(desc, numPoints, orgNo)
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def updatePointConversion(request):
    dollarAmt = request.POST.get('dollars')
    pointAmt = request.POST.get('points')

    newConversion = float(dollarAmt) / float(pointAmt)
    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    elif (request.session['isAdmin']):
        orgNo = request.session['adminOrgChoice']
    else:
        orgNo = db.getOrgNo(request.session['email'])

    db.updatePointConversion(orgNo, newConversion)
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def updatePaymentInfo(request):
    ccName = request.POST.get('ccName')
    ccNum = request.POST.get('ccNum')
    ccSec = request.POST.get('ccSec')
    ccDate = request.POST.get('ccDate')
    addr1 = request.POST.get('addr1')
    addr2 = request.POST.get('addr2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip = request.POST.get('zip')

    address = addr1
    if (addr2 != ''):
        address += ' ' + addr2
    address += ', ' + city + ', ' + state + ' ' + zip

    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    elif (request.session['isAdmin']):
        orgNo = request.session['adminOrgChoice']
    else:
        orgNo = db.getOrgNo(request.session['email'])

    currCard = getOrgPayment(orgNo)

    if currCard is None:
        db.addOrgPayment(ccName, ccNum, ccSec, ccDate, address, orgNo)
    else:
        db.updateOrgPayment(ccName, ccNum, ccSec, ccDate, address, orgNo, 1)
    
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def addNewSponsor(request):
    email = request.POST.get('email')
    name = request.POST.get('name')

    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    elif (request.session['isAdmin']):
        orgNo = request.session['adminOrgChoice']
    else:
        orgNo = db.getOrgNo(request.session['email'])

    newPassword = db.getRandomPassword()

    db.createSponsor(name, email, newPassword, orgNo)

    db.emailNewSponsor(email, newPassword, orgNo)

    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def editReason(request):
    reasonID = request.POST.get('reason')

    if reasonID != 'none':
        if 'remove' in request.POST:
            db.removePointChangeReason(reasonID)

            if (request.session['isAdmin']):
                return views.adminOrgs(request)
            else:
                return views.organizationPage(request)

        elif 'edit' in request.POST:
            if request.session['isAdmin']:
                return views.adminEditReason(request, reasonID)
            else:
                return views.sponsorEditReason(request, reasonID)
    
    else:
        if (request.session['isAdmin']):
            return views.adminOrgs(request)
        else:
            return views.organizationPage(request)

def editSponsor(request):
    sponsorID = request.POST.get('sponsor')

    if sponsorID != 'none':
        if 'remove' in request.POST:
            print('Remove')
            if (request.session['isSponsor']):
                currUserID = db.getUserID(request.session['email'])
                if (sponsorID != currUserID):
                    db.removeSponsor(sponsorID, currUserID)

                return views.organizationPage(request)
            else:
                result = db.getSponsors(request.session['adminOrgChoice'])

                for (id, name, email) in result:
                    if id != sponsorID:
                        break
                
                db.removeSponsor(sponsorID, id)
                return views.adminOrgs(request)

        elif 'edit' in request.POST:
            print("Edit")
            if (request.session['isSponsor']):
                return views.sponsorEditUser(request, sponsorID)
            else:
                return views.adminEditUser(request,sponsorID)
    else:
        if (request.session['isAdmin']):
            return views.adminOrgs(request)
        else:
            return views.organizationPage(request)

def editDriver(request):
    driverID = request.POST.get('driver')

    if driverID != 'none':
        if 'remove' in request.POST:
            if (request.session['isSponsor']):
                db.removeDriver(driverID)
                return views.organizationPage(request)
            else:
                db.removeDriver(driverID)
                return views.adminOrgs(request)

        elif 'edit' in request.POST:
            if (request.session['isSponsor']):
                return views.sponsorEditUser(request, driverID)
            else:
                return views.adminEditUser(request,driverID)
    else:
        if (request.session['isAdmin']):
            return views.adminOrgs(request)
        else:
            return views.organizationPage(request)

def adminEditUser(request, userID):
    newEmail = request.POST.get('email')
    password = request.POST.get('pass1')
    confirmPass = request.POST.get('pass2')
    orgID = request.POST.get('org')

    email = db.getUserEmail(userID)

    if newEmail != '':
        db.updateEmail(newEmail, email)

    if password != '' and confirmPass != '':
        if password == confirmPass:
            db.updatePassword(email, password)

    if orgID != 'none':
        db.addDriverOrg(userID, orgID)
    return views.adminOrgs(request)

def sponsorEditUser(request, userID):
    newEmail = request.POST.get('email')
    password = request.POST.get('pass1')
    confirmPass = request.POST.get('pass2')
    orgID = request.POST.get('org')

    email = db.getUserEmail(userID)

    if newEmail != '':
        db.updateEmail(newEmail, email)

    if password != '' and confirmPass != '':
        if password == confirmPass:
            db.updatePassword(email, password)

    return views.organizationPage(request)

def sponsorUpdateReason(request, reasonID):
    points = request.POST.get('points')
    desc = request.POST.get('description')

    db.updatePointChangeReason(reasonID, desc, points)
    return views.organizationPage(request)

def adminUpdateReason(request, reasonID):
    points = request.POST.get('points')
    desc = request.POST.get('description')

    db.updatePointChangeReason(reasonID, desc, points)
    return views.adminOrgs(request)

def getAdminOrgChoice(request):
    orgChoice = request.POST.get('orgs')

    request.session['adminOrgChoice'] = orgChoice
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def getNewCatalogKeyword(request):
    newKeyword = request.POST.get('keyword')

    if request.session['isViewing']:
        orgNo = db.getOrgNo(request.session['tempEmail'])
    else:
        orgNo = db.getOrgNo(request.session['email'])
    
    db.addKeyword(orgNo, newKeyword)
    return views.organizationPage(request)

def removeCatalogKeyword(request, wordID):
    if request.session['isViewing']:
        orgNo = db.getOrgNo(request.session['tempEmail'])
    else:
        orgNo = db.getOrgNo(request.session['email'])

    db.removeKeyword(orgNo, wordID)
    return views.organizationPage(request)

def createCatalog(request):
    CatalogViews.addProducts(request)
        
    return views.organizationPage(request)
from django.shortcuts import render
from truckersite.models import Uregister
from django.contrib import messages
import dbConnectionFunctions as db
import datetime

#add reguser to settings
def application(request):
    result = db.getOrgs()

    class Org:
        def __init__(self):
            id = -1
            name = ''

    orgs = []

    for (orgId, name) in result:
        tempOrg = Org()
        tempOrg.id = orgId
        tempOrg.name = name
        orgs.append(tempOrg)
    
    if 'loggedin' in request.session:
        context = {
            'loggedIn': request.session['loggedin'],
            'orgs': orgs
        }
    else:
        context = {
            'loggedIn': False,
            'orgs': orgs
        }
    
    return render(request, 'apply.html', context)
    

def userreggin(request):
    if request.method=='POST':
        if request.POST.get('Name') and request.POST.get('lname') and request.POST.get('PhoneNo') and request.POST.get('Email') and request.POST.get('Address') and request.POST.get('city') and request.POST.get('state') and request.POST.get('zipcode') and request.POST.get('sponsor'):
            now = datetime.datetime.now()
            today = now.strftime('%Y-%m-%d')
            
            applicant_name = request.POST.get('Name') + ' ' + request.POST.get('lname')
            applicant_phone = request.POST.get('PhoneNo')
            applicant_email = request.POST.get('Email')
            if request.POST.get('address2'):
                applicant_address = request.POST.get('Address') + ' ' + request.POST.get('address2') + ', ' + request.POST.get('city') + ', ' + request.POST.get('state') + ' ' + request.POST.get('zipcode')
            else:
                applicant_address = request.POST.get('Address') + ', ' + request.POST.get('city') + ', ' + request.POST.get('state') + ' ' + request.POST.get('zipcode')
            applicant_org = request.POST.get('sponsor')

            db.createApplicant(today, applicant_name, applicant_email, applicant_phone, applicant_address, applicant_org)

            return render(request,'index.html')
        else:
            return render(request,'apply.html')
    else:
        return render(request,'apply.html')

def getorgs(request):
    result = db.getOrgs()

    class Org:
        def __init__(self):
            id = -1
            name = ''

    orgs = []

    for (orgId, name) in result:
        tempOrg = Org()
        tempOrg.id = orgId
        tempOrg.name = name
        orgs.append(tempOrg)  
	  
	 
    context = {
        'orgs': orgs
    }
    return render(request, 'apply.html', context)

def page_not_found_view(request, exception=None):
    return render(request, '404.html')

def error_view(request):
    return render(request, '500.html')

def permission_denied_view(request, exception=None):
    return render(request, '403.html')

def bad_request_view(request, exception=None):
    return render(request, '400.html')
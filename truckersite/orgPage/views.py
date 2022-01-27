from django.shortcuts import render
import dbConnectionFunctions as db

# Create your views here.
def organizationPage(request):
    if (request.session['isViewing']):
        email = request.session['tempEmail']
        orgNo = db.getOrgNo(request.session['tempEmail'])
    else:
        email = request.session['email']
        orgNo = db.getOrgNo(request.session['email'])
        
    result = db.getPointChangeReasons(orgNo)

    class Reason:
        def __init__(self):
            id = -1
            desc = ''

    reasons = []
    
    if result != None:
        for (id, desc) in result:
            tempReason = Reason()
            tempReason.id = id
            tempReason.desc = desc
            reasons.append(tempReason)

    result = db.getSponsors(orgNo)

    class Sponsor:
        def __init__(self):
            id = -1
            name = ''
            email = ''
    
    sponsors = []

    if result != None:
        for (id, name, email) in result:
            tempSponsor = Sponsor()
            tempSponsor.id = id
            tempSponsor.name = name
            tempSponsor.email = email
            sponsors.append(tempSponsor)

    result = db.getDrivers(orgNo)

    class Driver:
        def __init__(self):
            id = -1
            name = ''
            email = ''
    
    drivers = []

    if result != None:
        for (id, name, email) in result:
            tempDriver = Driver()
            tempDriver.id = id
            tempDriver.name = name
            tempDriver.email = email
            drivers.append(tempDriver)

    imgPath = db.getOrgLogo(orgNo)
    logo = 'img/' + imgPath

    imgPath = db.getProfilePic(email)
    pic = 'img/' + imgPath

    result = db.getKeywords(orgNo)

    class Keyword:
        def __init__(self):
            id = -1
            word = ''
    
    keywords = []

    for (id, word) in result:
        tempWord = Keyword()
        tempWord.id = id
        tempWord.word = word
        keywords.append(tempWord)

    pointRate = db.getPointConversion(orgNo)

    result = db.getOrgPayment(orgNo)

    if not (result is None):
        ccName = result[0]
        ccNum = '************' + result[1]
        ccDate = result[2]
        billAddr = result[3]
    else:
        ccName = ''
        ccNum = ''
        ccDate = ''
        billAddr = ''

    context = {
        'reasons': reasons,
        'sponsors': sponsors,
        'drivers': drivers,
        'logo': logo,
        'keywords': keywords,
        'pic': pic,
        'pointRate': pointRate,
        'ccName': ccName,
        'ccNum': ccNum,
        'ccDate': ccDate,
        'billAddr': billAddr
    }

    return render(request, 'sponsor_organization.html', context)

def adminOrgs(request):
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

    if 'adminOrgChoice' in request.session:
        orgNo = request.session['adminOrgChoice']
            
        result = db.getPointChangeReasons(orgNo)

        class Reason:
            def __init__(self):
                id = -1
                desc = ''

        reasons = []

        for (id, desc) in result:
            tempReason = Reason()
            tempReason.id = id
            tempReason.desc = desc
            reasons.append(tempReason)

        result = db.getSponsors(orgNo)

        class Sponsor:
            def __init__(self):
                id = -1
                name = ''
                email = ''
        
        sponsors = []

        for (id, name, email) in result:
            tempSponsor = Sponsor()
            tempSponsor.id = id
            tempSponsor.name = name
            tempSponsor.email = email
            sponsors.append(tempSponsor)

        result = db.getDrivers(orgNo)

        class Driver:
            def __init__(self):
                id = -1
                name = ''
                email = ''
        
        drivers = []

        for (id, name, email) in result:
            tempDriver = Driver()
            tempDriver.id = id
            tempDriver.name = name
            tempDriver.email = email
            drivers.append(tempDriver)

        imgPath = db.getOrgLogo(orgNo)
        logo = 'img/' + imgPath

        result = db.getProductsInCatalog(orgNo)

        class Product:
            def __init__(self):
                id = -1
                name = ''
                price = ''
                pic = ''
        
        products = []

        for (id, name, price, img) in result:
            tempProduct = Product()
            tempProduct.id = id
            tempProduct.name = name
            tempProduct.price = price
            tempProduct.pic = img
            products.append(tempProduct)


        imgPath = db.getProfilePic(request.session['email'])
        pic = 'img/' + imgPath

        pointRate = db.getPointConversion(orgNo)

        result = db.getOrgPayment(orgNo)

        if not (result is None):
            ccName = result[0]
            ccNum = '************' + result[1]
            ccDate = result[2]
            billAddr = result[3]
        else:
            ccName = ''
            ccNum = ''
            ccDate = ''
            billAddr = ''

        context = {
            'reasons': reasons,
            'sponsors': sponsors,
            'drivers': drivers,
            'orgs': orgs,
            'logo': logo,
            'items': products,
            'pic': pic,
            'pointRate': pointRate,
            'ccName': ccName,
            'ccNum': ccNum,
            'ccDate': ccDate,
            'billAddr': billAddr
        }
    
    else:
        imgPath = db.getProfilePic(request.session['email'])
        pic = 'img/' + imgPath

        context = {
            'orgs': orgs,
            'pic': pic
        }

    return render(request, 'admin_organization.html', context)

def adminEditUser(request, userID):
    email = db.getUserEmail(userID)
    userType = db.getUserType(email)

    if userType == "Driver":
        isDriver = True
    else:
        isDriver = False

    orgs = []
    
    if isDriver:
        result = db.getOrgs()

        class Org:
            def __init__(self):
                id = -1
                name = ''
            
        for (id, name) in result:
            tempOrg = Org()
            tempOrg.id = id
            tempOrg.name = name
            orgs.append(tempOrg)

    imgPath = db.getProfilePic(request.session['email'])
    pic = 'img/' + imgPath
    
    context = {
        'userType': userType,
        'isDriver': isDriver,
        'userName': db.getUserName(email),
        'orgs': orgs,
        'userID': userID,
        'pic': pic,
        'currEmail': email
    }
        
    return render(request, 'admin_edit_user.html', context)

def sponsorEditUser(request, userID):
    email = db.getUserEmail(userID)
    userType = db.getUserType(email)

    if userType == "Driver":
        isDriver = True
    else:
        isDriver = False

    if request.session['isViewing']:
        imgPath = db.getProfilePic(request.session['tempEmail'])
    else:
        imgPath = db.getProfilePic(request.session['email'])
    pic = 'img/' + imgPath
    
    context = {
        'userType': userType,
        'isDriver': isDriver,
        'userName': db.getUserName(email),
        'userID': userID,
        'pic': pic,
        'currEmail': email
    }

    return render(request, 'sponsor_edit_user.html', context)

def sponsorEditReason(request, reasonID):
    if request.session['isViewing']:
        imgPath = db.getProfilePic(request.session['tempEmail'])
    else:
        imgPath = db.getProfilePic(request.session['email'])
    pic = 'img/' + imgPath

    result = db.getPointChangeReason(reasonID)

    for (points, desc) in result:
        currPoints = points
        currDesc = desc

    context = {
        'reasonID': reasonID,
        'currPoints': currPoints,
        'currDesc': currDesc
    }

    return render(request, 'sponsor_edit_reason.html', context)

def adminEditReason(request, reasonID):
    imgPath = db.getProfilePic(request.session['email'])
    pic = 'img/' + imgPath

    result = db.getPointChangeReason(reasonID)

    points = result[0]
    desc = result[1]

    context = {
        'reasonID': reasonID,
        'currPoints': points,
        'currDesc': desc,
        'pic': pic
    }
    
    return render(request, 'admin_edit_reason.html', context)
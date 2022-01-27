from django.shortcuts import render
import dbConnectionFunctions as db

def exists(list, element):
    for elem in list:
        if elem == element:
            return True
        
    return False

def find(list, element):
    index = 0
    for elem in list:
        if elem == element:
            return index
        index += 1

    return -1

# Create your views here.
def driverDash(request):
    if (request.session['isViewing']):
        driverID = db.getUserID(request.session['tempEmail'])
    else:
        driverID = db.getUserID(request.session['email'])
    
    result = db.getDriverOrgs(driverID)

    class Org:
        def __init__(self):
            id = -1
            name = ''
        
    orgs = []

    for (id, name) in result:
        tempOrg = Org()
        tempOrg.id = id
        tempOrg.name = name
        orgs.append(tempOrg)

    if (request.session['isViewing']):
        email = request.session['tempEmail']
        org = db.getOrgNo(request.session['tempEmail'])
    else:
        email = request.session['email']
        org = request.session['orgID']
    
    points = db.getDriverPoints(email, org)

    orgName = db.getOrgName(org)

    if (request.session['isViewing']):
        email = request.session['tempEmail']
        driverID = db.getUserID(request.session['tempEmail'])
        org = db.getOrgNo(request.session['tempEmail'])
    else:
        email = request.session['email']
        driverID = db.getUserID(request.session['email'])
        org = request.session['orgID']
    
    result = db.getDriverOrders(driverID, org)
    pointRate = db.getPointConversion(org)


    class Order:
        def __init__(self):
            id = -1
            date = '00/00/0000'
            self.totalCost = 0
            status = ''

    orderIds = []
    orders = []

    for (orderID, date, productName, qty, price, status) in result:
        if (not exists(orderIds, orderID)):
            tempOrder = Order()
            tempOrder.id = orderID
            tempOrder.date = date
            tempOrder.status = status
            orders.append(tempOrder)

            orderIds.append(orderID)

        i = find(orderIds, orderID)
        orders[i].totalCost += int(price / pointRate) * qty

    pic = db.getProfilePic(email)
    imgPath = 'img/' + pic

    context = {
        'isSponsor': request.session['isSponsor'],
        'isAdmin': request.session['isAdmin'],
        'driverOrgs': orgs,
        'points': points,
        'pic': imgPath,
        'currOrg': orgName,
        'orders': orders,
    }
    return render(request, "driver_dash.html", context)

def sponsorDash(request):
    context = {
        'isSponsor': request.session['isSponsor'],
        'isAdmin': request.session['isAdmin']
    }
    return render(request, "sponsor_dash.html", context)

def adminDash(request):
    result = db.getAllAdmins()

    class Admin:
        def __init__(self):
            id = -1
            name = ''

    admins = []

    for (id, name, email) in result:
        tempAdmin = Admin()
        tempAdmin.id = id
        tempAdmin.name = name
        admins.append(tempAdmin)

    result = db.getOrgs()

    class Org:
        def __init__(self):
            id = -1
            name = ''
        
    orgs = []

    for (id, name) in result:
        tempOrg = Org()
        tempOrg.id = id
        tempOrg.name = name
        orgs.append(tempOrg)

    pic = db.getProfilePic(request.session['email'])

    imgPath = 'img/' + pic

    context = {
        'admins': admins,
        'orgs': orgs,
        'pic': imgPath
    }

    return render(request, "admin_dash.html", context)
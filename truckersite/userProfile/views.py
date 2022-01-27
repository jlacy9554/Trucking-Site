from django.shortcuts import render
from django.http import HttpResponse
import dbConnectionFunctions as db

# Create your views here.
def driverProfile(request):
    if (request.session['isViewing']):
        email = request.session['tempEmail']
        imgPath = db.getProfilePic(request.session['tempEmail'])
    else:
        email = request.session['email']
        imgPath = db.getProfilePic(request.session['email'])

    profilePic = 'img/' + imgPath

    class Address:
        def __init__(self):
            id = -1
            addr = ''

    addresses = []

    if (request.session['isViewing']):
        result = db.getDriverAddresses(request.session['tempEmail'])
    else:
        result = db.getDriverAddresses(request.session['email'])

    for (id, address) in result:
        newAddr = Address()
        newAddr.addr = address
        newAddr.id = id
        addresses.append(newAddr)
    
    phone = db.getDriverPhone(email)
    
    context = {
        'pic': profilePic,
        'addresses': addresses,
        'currEmail': email,
        'currPhone': phone
    }
    return render(request, 'driver_profile.html', context)

def sponsorProfile(request):
    if (request.session['isViewing']):
        email = request.session['tempEmail']
        imgPath = db.getProfilePic(request.session['tempEmail'])
    else:
        email = request.session['email']
        imgPath = db.getProfilePic(request.session['email'])

    profilePic = 'img/' + imgPath
    context = {
        'pic': profilePic,
        'currEmail': email
    }
    return render(request, 'sponsor_profile.html', context)

def adminProfile(request):
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'img/' + imgPath
    context = {
        'pic': profilePic,
        'currEmail': request.session['email']
    }
    return render(request, 'admin_profile.html', context)

def driverPointHistory(request):

    class point_history:
        def __init__(self, points, desc, date):
            self.points = points
            self.desc = desc
            self.date = date
    
    point_list = []

    if (request.session['isViewing']):
        email = request.session['tempEmail']
        org = db.getOrgNo(email)
    else:
        email = request.session['email']
        org = request.session['orgID']

    conn = db.getDB()
    cursor = db.getCursor(conn)

    query_points = """SELECT 
        *
    FROM
        POINT_CHANGE
            INNER JOIN
        SPONSOR ON POINT_CHANGE.SponsorID = SPONSOR.UserID
            INNER JOIN
        POINT_CHANGE_REASON ON POINT_CHANGE.ReasonID = POINT_CHANGE_REASON.ReasonID
    WHERE
        SPONSOR.OrgID = %s
            AND POINT_CHANGE.DriverID = %s
    ORDER BY POINT_CHANGE.ChangeID ASC"""
    cursor.execute(query_points, (org, request.session['id'],))
    result = cursor.fetchall()

    for x in result:
        temp_points = x[10]
        temp_desc = x[9]
        temp_date = x[1]

        temp_point_hist = point_history(temp_points, temp_desc, temp_date)

        point_list.append(temp_point_hist)

    cursor.close()
    conn.close()

    num_points = db.getDriverPoints(email, org)

    pic = db.getProfilePic(email)
    imgPath = 'img/' + pic

    context = {'reason_list': point_list, 'num_points': num_points, 'pic': imgPath}
    return render(request, 'driver_point_history.html', context)
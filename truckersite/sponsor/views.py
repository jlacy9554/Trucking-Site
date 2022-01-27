from django.shortcuts import render, redirect
import dbConnectionFunctions as db
import datetime

def sponsorDashDisplay(request):

    class driver_applicant:
        def __init__(self, name, applicant_id):
            self.name = name
            self.applicant_id = applicant_id

    driver_application_list = []

    if (request.session['isViewing']):
        email = request.session['tempEmail']
        org_num = db.getOrgNo(request.session['tempEmail'])
    else:
        email = request.session['email']
        org_num = db.getOrgNo(request.session['email'])

    conn = db.getDB()
    cursor = db.getCursor(conn)

    query_applicants = "SELECT * FROM APPLICANT WHERE OrgID=%s AND Reason = \"Just applied\""
    cursor.execute(query_applicants, (org_num,))
    result = cursor.fetchall()

    for x in result:
        temp_name = x[4]
        temp_id = x[0]

        temp_driver = driver_applicant(temp_name, temp_id)

        driver_application_list.append(temp_driver)

    cursor.close()
    conn.close()

    profilePic = db.getProfilePic(email)
    imgPath = 'img/' + profilePic

    context = {'driver_application_list': driver_application_list,
               'isSponsor': request.session['isSponsor'], 'isAdmin': request.session['isAdmin'], 'pic': imgPath}
    return render(request, 'sponsor_dash.html', context)


def sponsorViewApplicant(request, applicant_id):
    if request.session['isViewing']:
        email = request.session['tempEmail']
    else:
        email = request.session['email']
    
    conn = db.getDB()
    cursor = db.getCursor(conn)

    query_applicant_name = 'SELECT * FROM APPLICANT WHERE ApplicantID = %s'
    cursor.execute(query_applicant_name, (applicant_id,))
    result = cursor.fetchone()

    applicant_date = result[1]
    applicant_name = result[4]
    applicant_email = result[5]
    applicant_phone = result[6]
    applicant_address = result[7]

    cursor.close()
    conn.close()

    profilePic = db.getProfilePic(email)
    imgPath = 'img/' + profilePic

    context = {'applicant_id': applicant_id, 'applicant_name': applicant_name, 'applicant_date': applicant_date, 'applicant_email': applicant_email,
               'applicant_phone': applicant_phone, 'applicant_address': applicant_address, 'pic': imgPath}
    return render(request, 'view_application.html', context)


def sponsorAcceptApplicant(request, applicant_id):
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')

    conn = db.getDB()
    cursor = db.getCursor(conn)

    query_update_applicant = 'UPDATE APPLICANT SET IsAccepted = %s, Reason = %s, ApplicantDate = %s WHERE ApplicantID = %s'
    cursor.execute(query_update_applicant,
                   (True, 'Sponsor Accepted', today, applicant_id,))

    query_applicant_info = 'SELECT * FROM APPLICANT WHERE ApplicantID = %s'
    cursor.execute(query_applicant_info, (applicant_id,))
    result = cursor.fetchone()
    applicant_name = result[4]
    applicant_email = result[5]
    applicant_phone = result[6]
    applicant_address = result[7]

    applicant_password = db.getRandomPassword()

    if (request.session['isViewing']):
        email = request.session['tempEmail']
        orgNo = db.getOrgNo(request.session['tempEmail'])
    else:
        email = request.session['email']
        orgNo = db.getOrgNo(request.session['email'])

    # name, email, password, address, phone, organization
    query_insert_driver = 'SELECT createDriver (%s, %s, %s, %s, %s, %s)'
    cursor.execute(query_insert_driver, (applicant_name, applicant_email,
                   applicant_password, applicant_address, applicant_phone, orgNo,))

    cursor.close()
    conn.close()

    db.emailNewDriver(applicant_email, applicant_password)

    profilePic = db.getProfilePic(email)
    imgPath = 'img/' + profilePic

    context = {'applicant_name': applicant_name, 'applicant_email': applicant_email, 'applicant_password': applicant_password, 'pic': imgPath}
    return render(request, 'accept_applicant_confirmation.html', context)


def sponsorRejectApplicant(request, applicant_id):
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')

    conn = db.getDB()
    cursor = db.getCursor(conn)

    query_reject_applicant = "UPDATE APPLICANT SET Reason = %s, ApplicantDate = %s WHERE ApplicantID = %s"
    cursor.execute(query_reject_applicant, ('Sponsor Rejected', today, applicant_id,))

    query_applicant_info = 'SELECT * FROM APPLICANT WHERE ApplicantID = %s'
    cursor.execute(query_applicant_info, (applicant_id,))
    result = cursor.fetchone()
    applicant_email = result[5]

    cursor.close()
    conn.close()

    db.emailRejectedDriver(applicant_email)

    response = redirect('/sponsor_dash/')
    return response


def sponsorViewDrivers(request):
    # query driver database and get all for current sponsor
    class indiv_driver:
        def __init__(self, name, driver_id):
            self.name = name
            self.driver_id = driver_id

    driver_list = []

    if request.session['isViewing']:
        email = request.session['tempEmail']
    else:
        email = request.session['email']

    org_num = db.getOrgNo(email)

    conn = db.getDB()
    cursor = db.getCursor(conn)

    query_drivers = "SELECT * FROM USER INNER JOIN DRIVER_ORGS ON DRIVER_ORGS.UserID = USER.UserID WHERE OrgID=%s"
    cursor.execute(query_drivers, (org_num,))
    result = cursor.fetchall()

    for x in result:
        temp_name = x[1]
        temp_id = x[0]

        temp_driver = indiv_driver(temp_name, temp_id)

        driver_list.append(temp_driver)

    cursor.close()
    conn.close()

    profilePic = db.getProfilePic(email)
    imgPath = 'img/' + profilePic

    context = {'driver_list': driver_list, 'pic': imgPath}
    return render(request, 'sponsor_view_drivers.html', context)


def sponsorChangePoints(request, driver_id):
    if request.method == 'POST':
        reason_id = request.POST.get('reason_id')
        sponsor_id = request.session['id']

        conn = db.getDB()
        cursor = db.getCursor(conn)

        # get organization number
        if (request.session['isViewing']):
            email = request.session['tempEmail']
            orgNo = db.getOrgNo(request.session['tempEmail'])
        else:
            email = request.session['email']
            orgNo = db.getOrgNo(request.session['email'])

        # get driver information
        query_driver_name = 'SELECT * FROM USER INNER JOIN DRIVER ON DRIVER.UserID = USER.UserID WHERE USER.UserID=%s'
        cursor.execute(query_driver_name, (driver_id,))
        result = cursor.fetchone()
        driver_name = result[1]
        driver_email = result[2]

        # get current driver points
        query_driver_points = 'SELECT * FROM DRIVER INNER JOIN DRIVER_ORGS ON DRIVER.UserID = DRIVER_ORGS.UserID WHERE DRIVER.UserID = %s'
        cursor.execute(query_driver_points, (driver_id,))
        result = cursor.fetchone()
        original_points = result[4]

        # get number of points based on reason id
        query_point_value = 'SELECT * FROM POINT_CHANGE_REASON WHERE ReasonID=%s'
        cursor.execute(query_point_value, (reason_id,))
        result = cursor.fetchone()
        num_points = result[2]

        # check if point total would be negative
        if original_points + num_points < 0:
            point_message = "* point change failed, driver points can not be negative *"
            successful = False
            after_points = original_points

            context = {'successful': successful, 'driver_name': driver_name, 'driver_email': driver_email, 'original_points': original_points, 
            'point_change': num_points, 'new_total': after_points, 'point_message': point_message}
            return render(request, 'change_points_confirmation.html', context)
        
        #change the points
        query_change_point_total = 'UPDATE DRIVER_ORGS SET Points = Points + %s WHERE UserID = %s AND OrgID = %s'
        cursor.execute(query_change_point_total, (num_points, driver_id, orgNo))

        # find amount of points after change
        cursor.execute(query_driver_points, (driver_id,))
        result = cursor.fetchone()
        after_points = result[4]
        print('after points: ', after_points)

        # check if points where added and send to confirmation page
        if original_points + num_points == after_points:
            point_message = "* points were successfully changed *"
            successful = True
            
            now = datetime.datetime.now()
            query_insert_point_change = 'INSERT INTO POINT_CHANGE (ChangeDate, ReasonID, TotalPoints, DriverID, SponsorID) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(query_insert_point_change, (now.strftime(
                '%Y-%m-%d'), reason_id, after_points, driver_id, request.session['id'],))
        else:
            point_message = "* point change failed *"
            successful = False
    
        cursor.close()
        conn.close()

        context = {'successful': successful, 'driver_name': driver_name, 'driver_email': driver_email, 'original_points': original_points, 'point_change': num_points,
                   'new_total': after_points, 'point_message': point_message}
        return render(request, 'change_points_confirmation.html', context)

    else:
        query_driver_name = 'SELECT * FROM USER INNER JOIN DRIVER ON DRIVER.UserID = USER.UserID WHERE USER.UserID=%s'

        conn = db.getDB()
        cursor = db.getCursor(conn)

        cursor.execute(query_driver_name, (driver_id,))
        result = cursor.fetchone()

        driver_name = result[1]
        driver_email = result[2]

        class point_reasons:
            def __init__(self, reason_id, reason_desc, reason_points):
                self.reason_id = reason_id
                self.reason_desc = reason_desc
                self.reason_points = reason_points

        reasons = []

        if (request.session['isViewing']):
            orgNo = db.getOrgNo(request.session['tempEmail'])
        else:
            orgNo = db.getOrgNo(request.session['email'])

        query_reasons = 'SELECT * FROM POINT_CHANGE_REASON WHERE OrgID=%s'

        cursor.execute(query_reasons, (orgNo,))
        result = cursor.fetchall()

        if result != None:
            for x in result:
                temp_reason_id = x[0]
                temp_reason_desc = x[1]
                temp_reason_points = x[2]

                temp_reason = point_reasons(
                    temp_reason_id, temp_reason_desc, temp_reason_points)

                reasons.append(temp_reason)

        cursor.close()
        conn.close()

        profilePic = db.getProfilePic(driver_email)
        imgPath = 'img/' + profilePic

        context = {'driver_name': driver_name,
                   'driver_id': driver_id, 'reason_list': reasons, 'pic': imgPath}
        return render(request, 'change_driver_points.html', context)

def sponsorApplicationList(request):
    if (request.session['isViewing']):
        email = request.session['tempEmail']
        org_num = db.getOrgNo(request.session['tempEmail'])
    else:
        email = request.session['email']
        org_num = db.getOrgNo(request.session['email'])

    class driver_applicant:
        def __init__(self, name, applicant_id):
            self.name = name
            self.applicant_id = applicant_id

    driver_application_list = []

    # get list of applications to display
    conn = db.getDB()
    cursor = db.getCursor(conn)

    query_applicants = "SELECT * FROM APPLICANT WHERE OrgID=%s AND IsAccepted=0"
    cursor.execute(query_applicants, (org_num,))
    result = cursor.fetchall()

    for x in result:
        temp_name = x[4]
        temp_id = x[0]
        temp_driver = driver_applicant(temp_name, temp_id)
        driver_application_list.append(temp_driver)
    
    cursor.close()
    conn.close()

    profilePic = db.getProfilePic(email)
    imgPath = 'img/' + profilePic

    context = {'driver_application_list': driver_application_list, 'pic': imgPath}

    return render(request, 'sponsor_application_list.html', context)
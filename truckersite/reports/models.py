from django.shortcuts import render
import dbConnectionFunctions as db
from reports import views
from reportlab.pdfgen.canvas import Canvas
from django.http import HttpResponse
import os

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

def updateDriverList(request):
    chosenOrg = request.POST.get('sponsor')

    if chosenOrg != 'all':
        choice = True
        result = db.getDrivers(chosenOrg)

        class Driver:
            def __init__(self):
                id = -1
                name = ''

        drivers = []

        for (id, name, email) in result:
            tempDriver = Driver()
            tempDriver.id = id
            tempDriver.name = name
            drivers.append(tempDriver)

        pic = db.getProfilePic(request.session['email'])
        imgPath = 'img/' + pic
    
        context = {
            'pic': imgPath,
            'chosenOrg': chosenOrg,
            'orgName': db.getOrgName(chosenOrg),
            'drivers': drivers,
            'choice': choice
        }

        return render(request, 'sales_by_sponsor.html', context)

    else:
        return views.sponsorSales(request)


# Create your models here.

def getSponsorReport(request):
    driver = request.POST.get('driver')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    print(driver)

    if (request.session['isViewing']):
        orgID = db.getOrgNo(request.session['tempEmail'])
    else:
        orgID = db.getOrgNo(request.session['email'])

    if (driver == 'all'):
        result = db.allDriverPointChangeReport(startDate, endDate, orgID)
    else:
        result = db.indvDriverPointChangeReport(startDate, endDate, orgID, driver)

    class PointChangeAtributes:
        def __init__(self):
            date = '00/00/00'
            pointChange = 0
            sponsor = 'none'
            reason = 'none'

    driverNames = []
    driverPoints = []
    pointChanges = []

    drivers = []

    for (driverName, pointTotal, changeDate, numPoints, sponsorID, reasonDesc) in result:
        if (not exists(driverNames, driverName)):
            driverNames.append(driverName)
            driverPoints.append(pointTotal)
            pointChanges.append([])

        i = find(driverNames, driverName)
        tempChange = PointChangeAtributes()
        tempChange.date = changeDate
        tempChange.pointChange = numPoints
        if reasonDesc == 'Completed Order':
            tempChange.sponsor = '--'
        else:
            tempChange.sponsor = db.getUserName(db.getUserEmail(sponsorID))
        tempChange.reason = reasonDesc
        pointChanges[i].append(tempChange)

    drivers = zip(driverNames, driverPoints, pointChanges)

    webContext = views.getSponsorContext(request)

    context = {
        'pic': webContext['pic'],
        'orgDrivers': webContext['orgDrivers'],
        'startDate': startDate,
        'endDate': endDate,
        'drivers': drivers,
    }

    if 'download' in request.POST:
        rowNum = 800
        orgName = db.getOrgName(orgID)
        fileName = orgName + "PointReport.pdf"
        canvas = Canvas('static/reports/' + fileName)
        #Print data range
        canvas.drawString(70, rowNum, "Date Range: " + startDate + " - " + endDate)

        for (driver, points, changes) in zip(driverNames, driverPoints, pointChanges):
            if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800

            rowNum -= 35
            canvas.drawString(70, rowNum, "Driver: " + driver)
            canvas.drawString(215, rowNum, "Total Points: " + str(points))

            if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800
            rowNum -= 20
            canvas.drawString(70, rowNum, "Point Changes")

            if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800
            rowNum -= 30
            canvas.drawString(70, rowNum, "Date")
            canvas.drawString(150, rowNum, "Change Amount")
            canvas.drawString(250, rowNum, "Sponsor Responsible")
            canvas.drawString(400, rowNum, "Reasoning")

            if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800

            for change in changes:
                rowNum -= 20
                canvas.drawString(70, rowNum, str(change.date))
                canvas.drawString(150, rowNum, str(change.pointChange))
                canvas.drawString(250, rowNum, change.sponsor)
                canvas.drawString(400, rowNum, change.reason)

        canvas.save()

        pdf = open(fileName, 'rb')
        response = HttpResponse(pdf.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="' + fileName
        return response
    return render(request, 'sponsor_generate_report.html', context)

def getAuditLog(request):
    reportType = request.POST.get('logType')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    if (reportType == 'applications'):
        result = db.driverApplicationsReport(startDate, endDate)

        class Applicant:
            def __init__(self):
                date = '00/00/00'
                orgName = 0
                name = 'none'
                accepted = False
                reason = 'none'

        applicants = []

        for (applicantDate, orgID, applicantName, isAccepted, reason) in result:
            tempApplicant = Applicant()
            tempApplicant.date = applicantDate
            tempApplicant.orgName = db.getOrgName(orgID)
            tempApplicant.name = applicantName
            tempApplicant.accepted = isAccepted
            tempApplicant.reason = reason
            applicants.append(tempApplicant)

        rowNum = 800
        if 'download' in request.POST:
            fileName = 'applicantsAuditLog.pdf'
            canvas = Canvas('static/reports/' + fileName)
            #Print data range
            canvas.drawString(70, rowNum, "Date Range: " + startDate + " - " + endDate)

            if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800
            rowNum -= 30
            canvas.drawString(70, rowNum, "Date")
            canvas.drawString(140, rowNum, "Sponsor")
            canvas.drawString(250, rowNum, "Applicant Name")
            canvas.drawString(375, rowNum, "Status")
            canvas.drawString(475, rowNum, "Reason")

            if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800

            for applicant in applicants:
                rowNum -= 20
                canvas.drawString(70, rowNum, str(applicant.date))
                canvas.drawString(140, rowNum, applicant.orgName)
                canvas.drawString(250, rowNum, applicant.name)

                if applicant.accepted:
                    canvas.drawString(375, rowNum, "Accepted")
                    canvas.drawString(475, rowNum, "---------")

                else:
                    canvas.drawString(375, rowNum, "Rejected")
                    canvas.drawString(475, rowNum, applicant.reason)

            canvas.save()
            pdf = open(fileName, 'rb')
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename="' + fileName
            return response

        context = {
            'startDate': startDate,
            'endDate': endDate,
            'applicants': applicants,
            'applications': True,
            'points': False,
            'passwords': False,
            'login': False
        }

    elif (reportType == 'points'):
        result = db.pointChangeReport(startDate, endDate)

        class PointChangeAtributes:
            def __init__(self):
                date = '00/00/00'
                orgName = 'none'
                pointChange = 0
                reason = 'none'

        
        driverNames = []
        pointChanges = []

        drivers = []

        for (driverName, changeDate, orgName, numPoints, reasonDesc) in result:
            if (not exists(driverNames, driverName)):
                driverNames.append(driverName)
                pointChanges.append([])

            i = find(driverNames, driverName)
            tempChange = PointChangeAtributes()
            tempChange.date = changeDate
            tempChange.orgName = orgName
            tempChange.pointChange = numPoints
            tempChange.reason = reasonDesc
            pointChanges[i].append(tempChange)

        drivers = zip (driverNames, pointChanges)

        rowNum = 800
        if 'download' in request.POST:
            fileName = 'pointChangeAuditLog.pdf'
            canvas = Canvas('static/reports/' + fileName)
            #Print data range
            canvas.drawString(70, rowNum, "Date Range: " + startDate + " - " + endDate)

            for (driver, changes) in zip(driverNames, pointChanges):
                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800

                rowNum -= 35
                canvas.drawString(70, rowNum, "Driver: " + driver)

                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                rowNum -= 20
                canvas.drawString(70, rowNum, "Point Changes")

                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                rowNum -= 30
                canvas.drawString(70, rowNum, "Date")
                canvas.drawString(150, rowNum, "Change Amount")
                canvas.drawString(250, rowNum, "Sponsor")
                canvas.drawString(400, rowNum, "Reasoning")

                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800

                for change in changes:
                    rowNum -= 20
                    canvas.drawString(70, rowNum, str(change.date))
                    canvas.drawString(150, rowNum, str(change.pointChange))
                    canvas.drawString(250, rowNum, change.orgName)
                    canvas.drawString(400, rowNum, change.reason)

            canvas.save()

            pdf = open(fileName, 'rb')
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename="' + fileName
            return response

        context = {
            'startDate': startDate,
            'endDate': endDate,
            'drivers': drivers,
            'applications': False,
            'points': True,
            'passwords': False,
            'login': False
        }

    elif(reportType == 'passwords'):
        result = db.passwordChangeReport(startDate, endDate)

        class PassChange:
            def __init__(self):
                date = '00/00/00'
                changeType = 'none'

        userNames = []
        passChanges = []

        users = []

        for (userName, changeDate, changeType) in result:
            if (not exists(userNames, userName)):
                userNames.append(userName)
                passChanges.append([])

            i = find(userNames, userName)
            tempChange = PassChange()
            tempChange.date = changeDate
            tempChange.changeType = changeType
            passChanges[i].append(tempChange)

        users = zip (userNames, passChanges)

        rowNum = 800
        if 'download' in request.POST:
            fileName = 'passwordChangeAuditLog.pdf'
            canvas = Canvas('static/reports/' + fileName)
            #Print data range
            canvas.drawString(70, rowNum, "Date Range: " + startDate + " - " + endDate)

            for (user, changes) in zip(userNames, passChanges):
                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800

                rowNum -= 35
                canvas.drawString(70, rowNum, "User: " + user)

                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                rowNum -= 30
                canvas.drawString(70, rowNum, "Date")
                canvas.drawString(150, rowNum, "Type of Change")

                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800

                for change in changes:
                    rowNum -= 20
                    canvas.drawString(70, rowNum, str(change.date))
                    canvas.drawString(150, rowNum, change.changeType)

            canvas.save()

            pdf = open(fileName, 'rb')
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename="' + fileName
            return response

        context = {
            'startDate': startDate,
            'endDate': endDate,
            'users': users,
            'applications': False,
            'points': False,
            'passwords': True,
            'login': False
        }

    else:
        result = db.loginAttemptsReport(startDate, endDate)

        class LoginAttempt:
            def __init__(self):
                date = '00/00/00'
                succeeded = False

        userEmails = []
        attempts = []

        users = []

        for (userEmail, attemptDate, succeeded) in result:
            if (not exists(userEmails, userEmail)):
                userEmails.append(userEmail)
                attempts.append([])

            i = find(userEmails, userEmail)
            tempLogin = LoginAttempt()
            tempLogin.date = attemptDate
            tempLogin.succeeded = succeeded
            attempts[i].append(tempLogin)

        users = zip (userEmails, attempts)

        rowNum = 800
        if 'download' in request.POST:
            fileName = 'loginAttemptsAuditLog.pdf'
            canvas = Canvas('static/reports/' + fileName)
            #Print data range
            canvas.drawString(70, rowNum, "Date Range: " + startDate + " - " + endDate)

            for (user, attempts) in zip(userEmails, attempts):
                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800

                rowNum -= 35
                canvas.drawString(70, rowNum, "User: " + user)

                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                rowNum -= 30
                canvas.drawString(70, rowNum, "Date")
                canvas.drawString(150, rowNum, "Status")


                for attempt in attempts:
                    if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                    rowNum -= 20
                    canvas.drawString(70, rowNum, str(attempt.date))
                    if attempt.succeeded:
                        canvas.drawString(150, rowNum, "Success")
                    else:
                        canvas.drawString(150, rowNum, "Failure")

            canvas.save()

            pdf = open(fileName, 'rb')
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename="' + fileName
            return response

        context = {
            'startDate': startDate,
            'endDate': endDate,
            'users': users,
            'applications': False,
            'points': False,
            'passwords': False,
            'login': True
        }


    return render(request, 'audit_log.html', context)

def getInvoice(request):
    orgID = request.POST.get('org')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    if (orgID == 'all'):
        result = db.allSponsorInvoice(startDate, endDate)
    else:
        result = db.indvSponsorInvoice(startDate, endDate, orgID)

    class InvoiceItem:
        def __init__(self):
            date = '00/00/00'
            cost = 0

    class Driver:
        def __init__(self):
            id = -1
            name = ''
            self.orders = []
            self.totalCost = 0
            driverFee = 0

    class Org:
        def __init__(self):
            name = ''
            self.drivers = []
            self.totalSales = 0
            totalFee = 0

    driverIDs = []
    orgNames = []

    orgs = []

    for (orgName, orderDate, driverID, driverName, price, qty) in result:
        if (not exists(orgNames, orgName)):
            orgNames.append(orgName)

            tempOrg = Org()
            tempOrg.name = orgName
            orgs.append(tempOrg)
        
        if (not exists(driverIDs, driverID)):
            i = find(orgNames, orgName)
            driverIDs.append(driverID)

            tempDriver = Driver()
            tempDriver.id = driverID
            tempDriver.name = driverName
            orgs[i].drivers.append(tempDriver)

        i = find(driverIDs, driverID)
        j = find(orgNames, orgName)
        tempItem = InvoiceItem()
        tempItem.date = orderDate
        tempItem.driver = driverName
        tempItem.cost = price * qty
        orgs[j].drivers[i].orders.append(tempItem)

        orgs[j].drivers[i].totalCost += price * qty
        orgs[j].drivers[i].driverFee = orgs[j].drivers[i].totalCost * 0.01

        orgs[j].totalSales += price * qty
        orgs[j].totalFee = orgs[j].totalSales * 0.01

    webContext = views.getInvoiceContext(request)

    rowNum = 800
    if 'download' in request.POST:
        if orgID == "all":
            fileName = 'allSponsorInvoices.pdf'
        else:
            orgName = db.getOrgName(orgID)
            fileName = orgName + 'Invoice.pdf'
        canvas = Canvas('static/reports/' + fileName)

        #Print data range
        canvas.drawString(70, rowNum, "Date Range: " + startDate + " - " + endDate)

        for org in orgs:
            if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800

            rowNum -= 35
            canvas.drawString(70, rowNum, "Sponsor: " + org.name)

            for driver in org.drivers:
                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                rowNum -= 20
                canvas.drawString(70, rowNum, "Sales by " + driver.name)

                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                rowNum -= 30
                canvas.drawString(70, rowNum, "Date")
                canvas.drawString(150, rowNum, "Cost")

                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800

                for order in driver.orders:
                    rowNum -= 20
                    canvas.drawString(70, rowNum, str(order.date))
                    canvas.drawString(150, rowNum, str(order.cost))
                
            if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800
            rowNum -= 20
            canvas.drawString(300, rowNum, "Total Cost: " + str(driver.totalCost))

            if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800
            rowNum -= 20
            canvas.drawString(300, rowNum, "Total Fee for Driver: " + str(driver.driverFee))

            if (rowNum <= 80):
                canvas.showPage()
                rowNum = 800
            rowNum -= 35
            canvas.drawString(300, rowNum, "Total Sales: " + str(org.totalSales))

            if (rowNum <= 80):
                canvas.showPage()
                rowNum = 800
            rowNum -= 20
            canvas.drawString(300, rowNum, "Total Amount Owed: " + str(org.totalFee))

        canvas.save()

        pdf = open(fileName, 'rb')
        response = HttpResponse(pdf.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="' + fileName
        return response

    context = {
        'startDate': startDate,
        'endDate': endDate,
        'orgs': orgs,
        'pic': webContext['pic'],
        'listOrgs': webContext['listOrgs'],
        'totalFee': totalFee
    }


    return render(request, 'invoice.html', context)

def getDriverSales(request):
    driverID = request.POST.get('driver')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    detailed = request.POST.get('detail')

    if detailed == 'on':
        details = True

        if (driverID == 'all'):
            result = db.driverSaleReport(startDate, endDate, details, -1)
        else:
            result = db.driverSaleReport(startDate, endDate, details, driverID)

        class Product:
            def __init__(self):
                name = ""
                qty = 0
                price = 0

        class DriverOrder:
            products = []
            def __init__(self):
                id = -1
                date = '00/00/00'
                products = []
                totalCost = 0

        class Org:
            orders = []
            def __init__(self):
                id = -1
                name = ''
                orders = []
                self.totalCost = 0

        class Driver:
            orgs = []
            def __init__(self):
                id = -1
                name = ''
                orgs = []
                self.totalCost = 0

        drivers = []
        orgIDs = []
        driverIDs = []
        orderIDs = []

        for (driverID, driverName, orgID, orgName, orderID, orderDate, productName, qty, price) in result:
            if (not exists(driverIDs, driverID)):
                driverIDs.append(driverID)

                tempDriver = Driver()
                tempDriver.id = driverID
                tempDriver.name = driverName
                drivers.append(tempDriver)

            i = find(driverIDs, driverID)
            if (not exists(orgIDs, orgID)):
                orgIDs.append(orgID)

                tempOrg = Org()
                tempOrg.id = orgID
                tempOrg.name = orgName
                drivers[i].orgs.append(tempOrg)

            j = find(orgIDs, orgID)
            if (not exists(orderIDs, orderID)):
                orderIDs.append(orderID)

                tempOrder = DriverOrder()
                tempOrder.id = orderID
                tempOrder.date = orderDate
                tempOrder.totalCost = 0
                drivers[i].orgs[j].orders.append(tempOrder)

            k = find(orderIDs, orderID)
            tempProduct = Product()
            tempProduct.name = productName
            tempProduct.qty = qty
            tempProduct.price = price
            drivers[i].orgs[j].orders[k].products.append(tempProduct)
            drivers[i].orgs[j].orders[k].totalCost += price * qty

            drivers[i].orgs[j].totalCost += price * qty

            drivers[i].totalCost += price * qty

        rowNum = 800
        if 'download' in request.POST:
            if driverID == "all":
                fileName = 'allDriverSales.pdf'
            else:
                email = db.getUserEmail(driverID)
                name = db.getUserName(email)
                fileName = name + 'Sales.pdf'
            canvas = Canvas('static/reports/' + fileName)

            #Print data range
            canvas.drawString(70, rowNum, "Date Range: " + startDate + " - " + endDate)

            for driver in drivers:
                if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800

                rowNum -= 35
                canvas.drawString(70, rowNum, "Driver: " + driver.name)

                for org in driver.orgs:
                    if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                    rowNum -= 20
                    canvas.drawString(70, rowNum, "Sales for " + org.name)

                    if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                    rowNum -= 30
                    canvas.drawString(70, rowNum, "Date")
                    canvas.drawString(150, rowNum, "Product")
                    canvas.drawString(450, rowNum, "Quantity")
                    canvas.drawString(500, rowNum, "Cost")

                    if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800

                    for order in org.orders:
                        rowNum -= 20
                        canvas.drawString(70, rowNum, str(order.date))

                        for product in order.products:
                            if (rowNum <= 80):
                                canvas.showPage()
                                rowNum = 800
                            rowNum -= 20

                            printString = ''
                            for x in product.name:
                                printString += x
                                if len(printString) > 45:
                                    break

                            printString += '...'
                            canvas.drawString(150, rowNum, printString)
                            canvas.drawString(450, rowNum, str(product.qty))
                            canvas.drawString(500, rowNum, str(product.price))
                    
                        if (rowNum <= 80):
                                canvas.showPage()
                                rowNum = 800
                        rowNum -= 20
                        canvas.drawString(450, rowNum, "Total Cost: " + str(order.totalCost))

            canvas.save()

            pdf = open(fileName, 'rb')
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename="' + fileName
            return response

    else:
        details = False

        if (driverID == 'all'):
            result = db.driverSaleReport(startDate, endDate, details, -1)
        else:
            result = db.driverSaleReport(startDate, endDate, details, driverID)

        class DriverOrder:
            def __init__(self):
                id = -1
                date = '00/00/00'
                totalCost = 0

        class Org:
            orders = []
            def __init__(self):
                id = -1
                name = ''
                orders = []
                self.totalCost = 0

        class Driver:
            orgs = []
            def __init__(self):
                id = -1
                name = ''
                orgs = []
                self.totalCost = 0

        drivers = []
        orgIDs = []
        driverIDs = []
        orderIDs = []

        for (driverID, driverName, orgID, orgName, orderID, orderDate, qty, price) in result:
            if (not exists(driverIDs, driverID)):
                driverIDs.append(driverID)

                tempDriver = Driver()
                tempDriver.id = driverID
                tempDriver.name = driverName
                drivers.append(tempDriver)

            i = find(driverIDs, driverID)
            if (not exists(orgIDs, orgID)):
                orgIDs.append(orgID)

                tempOrg = Org()
                tempOrg.id = orgID
                tempOrg.name = orgName
                drivers[i].orgs.append(tempOrg)

            j = find(orgIDs, orgID)
            if (not exists(orderIDs, orderID)):
                orderIDs.append(orderID)

                tempOrder = DriverOrder()
                tempOrder.id = orderID
                tempOrder.date = orderDate
                tempOrder.totalCost = 0
                drivers[i].orgs[j].orders.append(tempOrder)

            k = find(orderIDs, orderID)
            drivers[i].orgs[j].orders[k].totalCost += price * qty

            drivers[i].orgs[j].totalCost += price * qty

            drivers[i].totalCost += price * qty

        rowNum = 800
        if 'download' in request.POST:
            if driverID == "all":
                fileName = 'allDriverSales.pdf'
            else:
                email = db.getUserEmail(driverID)
                name = db.getUserName(email)
                fileName = name + 'Sales.pdf'
            canvas = Canvas('static/reports/' + fileName)

            #Print data range
            canvas.drawString(70, rowNum, "Date Range: " + startDate + " - " + endDate)

            for driver in drivers:
                if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800

                rowNum -= 35
                canvas.drawString(70, rowNum, "Driver: " + driver.name)

                for org in driver.orgs:
                    if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                    rowNum -= 20
                    canvas.drawString(70, rowNum, "Sales for " + org.name)

                    if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                    rowNum -= 30
                    canvas.drawString(70, rowNum, "Date")
                    canvas.drawString(150, rowNum, "Cost")

                    if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800

                    for order in org.orders:
                        rowNum -= 20
                        canvas.drawString(70, rowNum, str(order.date))
                        canvas.drawString(150, rowNum, str(order.totalCost))

            canvas.save()

            pdf = open(fileName, 'rb')
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename="' + fileName
            return response

    webContext = views.getDriverSalesContext(request)

    context = {
        'startDate': startDate,
        'endDate': endDate,
        'driverSales': drivers,
        'detailed': details,
        'pic': webContext['pic'],
        'drivers': webContext['drivers']
    }


    return render(request, 'sales_by_driver.html', context)

def getSponsorSales(request):
    if 'choseOrg' in request.POST:
        return updateDriverList(request)
    
    orgID = request.POST.get('sponsor')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    detailed = request.POST.get('detail')
    driver = request.POST.get('driver')

    if detailed == 'on':
        details = True

        if (orgID == 'all'):
            result = db.allSponsorSaleReport(startDate, endDate, details)
        else:
            if (driver == 'all'):
                result = db.indvSponsorSaleReport(startDate, endDate, details, -1, orgID)
            else:
                result = db.indvSponsorSaleReport(startDate, endDate, details, driver, orgID)

        class Product:
            def __init__(self):
                name = ""
                qty = 0
                price = 0

        class DriverOrder:
            products = []
            totalCost = 0
            def __init__(self):
                id = -1
                date = '00/00/00'
                driver = ""
                products = []
                totalCost = 0

        class Driver:
            orders = []
            totalCost = 0
            def __init__(self):
                id = -1
                name = ''
                orders = []
                totalCost = 0

        class Org:
            drivers = []
            totalCost = 0
            def __init__(self):
                id = -1
                name = ''
                drivers = []
                totalCost = 0

        orgIDs = []
        orderIDs = []
        driverIDs = []

        orgs = []

        for (orgID, orgName, orderID, orderDate, driverID, driverName, productName, qty, price) in result:
            if (not exists(orgIDs, orgID)):
                orgIDs.append(orgID)

                tempOrg = Org()
                tempOrg.id = orgID
                tempOrg.name = orgName
                orgs.append(tempOrg)

            i = find(orgIDs, orgID)
            if (not exists(driverIDs, driverID)):
                driverIDs.append(driverID)

                tempDriver = Driver()
                tempDriver.id = driverID
                tempDriver.name = driverName
                orgs[i].drivers.append(tempDriver)

            j = find(driverIDs, driverID)
            if (not exists(orderIDs, orderID)):
                orderIDs.append(orderID)

                tempOrder = DriverOrder()
                tempOrder.id = orderID
                tempOrder.driver = driverName
                tempOrder.date = orderDate
                orgs[i].drivers[j].orders.append(tempOrder)

            k = find(orderIDs, orderID)
            tempProduct = Product()
            tempProduct.name = productName
            tempProduct.qty = qty
            tempProduct.price = price
            orgs[i].drivers[j].orders[k].products.append(tempProduct)
            orgs[i].drivers[j].orders[k].totalCost += price * qty

            orgs[i].drivers[j].totalCost += price * qty

            orgs[i].totalCost += price * qty

        rowNum = 800
        if 'download' in request.POST:
            if driverID == "all":
                fileName = 'allSponsorSales.pdf'
            else:
                name = db.getOrgName(orgID)
                fileName = name + 'Sales.pdf'
            canvas = Canvas('static/reports/' + fileName)

            #Print data range
            canvas.drawString(70, rowNum, "Date Range: " + startDate + " - " + endDate)

            for org in orgs:
                if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800

                rowNum -= 35
                canvas.drawString(70, rowNum, "Sponsor: " + org.name)

                for driver in org.drivers:
                    if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                    rowNum -= 20
                    canvas.drawString(70, rowNum, "Sales by: " + driver.name)

                    if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                    rowNum -= 30
                    canvas.drawString(70, rowNum, "Date")
                    canvas.drawString(150, rowNum, "Product")
                    canvas.drawString(450, rowNum, "Quantity")
                    canvas.drawString(500, rowNum, "Cost")

                    if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800

                    for order in driver.orders:
                        rowNum -= 20
                        canvas.drawString(70, rowNum, str(order.date))

                        for product in order.products:
                            if (rowNum <= 80):
                                canvas.showPage()
                                rowNum = 800
                            rowNum -= 20

                            printString = ''
                            for x in product.name:
                                printString += x
                                if len(printString) > 45:
                                    break

                            printString += '...'
                            canvas.drawString(150, rowNum, printString)
                            canvas.drawString(450, rowNum, str(product.qty))
                            canvas.drawString(500, rowNum, str(product.price))
                    
                        if (rowNum <= 80):
                                canvas.showPage()
                                rowNum = 800
                        rowNum -= 20
                        canvas.drawString(500, rowNum, "Total Cost: " + str(order.totalCost))

                    if (rowNum <= 80):
                            canvas.showPage()
                            rowNum = 800
                    rowNum -= 30
                    canvas.drawString(70, rowNum, "Total Sales by Driver: " + str(driver.totalCost))
            if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800
            rowNum -= 30
            canvas.drawString(70, rowNum, "Total Sales from Sponsor: " + str(org.totalCost))
            canvas.save()

            pdf = open(fileName, 'rb')
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename="' + fileName
            return response

    else:
        details = False

        if (orgID == 'all'):
            result = db.allSponsorSaleReport(startDate, endDate, details)
        else:
            if (driver == 'all'):
                result = db.indvSponsorSaleReport(startDate, endDate, details, -1, orgID)
            else:
                result = db.indvSponsorSaleReport(startDate, endDate, details, db.getUserID(driver), orgID)

        class DriverOrder:
            totalCost = 0
            totalCost = 0
            def __init__(self):
                id = -1
                date = '00/00/00'
                driver = ""
                totalCost = 0

        class Org:
            drivers = []
            totalCost = 0
            def __init__(self):
                id = -1
                name = ''
                drivers = []
                self.orders = []
                totalCost = 0

        orgIDs = []
        orderIDs = []

        orgs = []

        for (org, orgName, orderID, orderDate, qty, price) in result:
            if (not exists(orgIDs, org)):
                orgIDs.append(org)

                tempOrg = Org()
                tempOrg.id = org
                tempOrg.name = orgName
                orgs.append(tempOrg)

            i = find(orgIDs, orgID)
            if (not exists(orderIDs, orderID)):
                orderIDs.append(orderID)

                tempOrder = DriverOrder()
                tempOrder.id = orderID
                tempOrder.date = orderDate
                orgs[i].orders.append(tempOrder)

            j = find(orderIDs, orderID)
            orgs[i].orders[j].totalCost += price * qty

            orgs[i].totalCost += price * qty

        rowNum = 800
        if 'download' in request.POST:
            if driver == "all":
                fileName = 'allSponsorSales.pdf'
            else:
                name = db.getOrgName(orgID)
                fileName = name + 'Sales.pdf'
            canvas = Canvas('static/reports/' + fileName)

            #Print data range
            canvas.drawString(70, rowNum, "Date Range: " + startDate + " - " + endDate)

            for org in orgs:
                if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800

                rowNum -= 35
                canvas.drawString(70, rowNum, "Sponsor: " + org.name)

                if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800
                rowNum -= 30
                canvas.drawString(70, rowNum, "Date")
                canvas.drawString(150, rowNum, "Product")
                canvas.drawString(250, rowNum, "Quantity")
                canvas.drawString(300, rowNum, "Cost")

                if (rowNum <= 80):
                    canvas.showPage()
                    rowNum = 800

                for order in org.orders:
                    rowNum -= 20
                    canvas.drawString(70, rowNum, str(order.date))
                    canvas.drawString(150, rowNum, str(order.totalCost))

                if (rowNum <= 80):
                        canvas.showPage()
                        rowNum = 800
                rowNum -= 30
                canvas.drawString(70, rowNum, "Total Sales from Sponsor: " + str(org.totalCost))
            canvas.save()

            pdf = open(fileName, 'rb')
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename="' + fileName
            return response

    webContext = views.getSponsorSalesContext(request)

    context = {
        'startDate': startDate,
        'endDate': endDate,
        'orgSales': orgs,
        'detailed': details,
        'pic': webContext['pic'],
        'orgs': webContext['orgs'],
    }

    return render(request, 'sales_by_sponsor.html', context)
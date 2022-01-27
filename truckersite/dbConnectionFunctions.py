from datetime import datetime
from mysql.connector import connect, Error
import random
import string
from django.core.mail import EmailMessage

def getDB():
    try:
        connection = connect(host = 'truckingdb.c9tkxb1tjvpp.us-east-1.rds.amazonaws.com', user = 'admin', password = 'accesstodb', database = 'DRIVER_DB', autocommit = True, charset = 'latin1', use_unicode = True)

        while connection is None:
            connection = connect(host = 'truckingdb.c9tkxb1tjvpp.us-east-1.rds.amazonaws.com', user = 'admin', password = 'accesstodb', database = 'DRIVER_DB', autocommit = True, charset = 'latin1', use_unicode = True)
    
    except Error as err:
        print(err)

    else:
        return connection

def getCursor(connection):
    try:
        while connection is None:
            connection = connect(host = 'truckingdb.c9tkxb1tjvpp.us-east-1.rds.amazonaws.com', user = 'admin', password = 'accesstodb', database = 'DRIVER_DB', autocommit = True, charset = 'latin1', use_unicode = True)
            
        cursor = connection.cursor(buffered = True)

        while cursor is None:
            cursor = connection.cursor(buffered = True)
    
    except Error as err:
        print(err)
    
    else:
        return cursor

def getDBReplica():
    try:
        connection = connect(host = 'truckingdbreplica.c9tkxb1tjvpp.us-east-1.rds.amazonaws.com', user = 'admin', password = 'accesstodb', database = 'DRIVER_DB', autocommit = True, charset = 'latin1', use_unicode = True)

        while connection is None:
            connection = connect(host = 'truckingdbreplica.c9tkxb1tjvpp.us-east-1.rds.amazonaws.com', user = 'admin', password = 'accesstodb', database = 'DRIVER_DB', autocommit = True, charset = 'latin1', use_unicode = True)

    except Error as err:
        print(err)

    else:
        return connection

def getCursorReplica(connection):
    try:
        while connection is None:
            connection = connect(host = 'truckingdbreplica.c9tkxb1tjvpp.us-east-1.rds.amazonaws.com', user = 'admin', password = 'accesstodb', database = 'DRIVER_DB', autocommit = True, charset = 'latin1', use_unicode = True)

        cursor = connection.cursor(buffered = True)

        while cursor is None:
            cursor = connection.cursor(buffered = True)

    except Error as err:
        print(err)

    else:
        return cursor

def checkEmail(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT emailExists(%s)"

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for emailExists in result:
            if emailExists == 0:
                cursor.close()
                conn.close()
                return False
            
            else:
                cursor.close()
                conn.close()
                return True
    except Error as err:
        print(err)


def updateEmail(newEmail, oldEmail):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(newEmail)

        if emailExists == False:
            query = "SELECT updateEmail(%s, %s)"

            cursor.execute(query, (oldEmail, newEmail,))

            cursor.close()
            conn.close()
            return "Email successfully updated."
        else:
            cursor.close()
            conn.close()
            return "Email is already taken by another account."
    
    except Error as err:
        print (err)

def updatePassword(email, newPassword):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT updatePassword(%s, %s)"
            cursor.execute(query, (email, newPassword,))

            cursor.close()
            conn.close()
            return "Password successfully updated."
        else:
            cursor.close()
            conn.close()
            return "Error updating password. (Email not found)"
    except Error as err:
        print(err)

def changePassword(email, newPassword):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addPassChange(%s, \"Manual Change\", %s)"
        date = datetime.date.today()
        cursor.execute(query, (email, date))

        cursor.close()
        conn.close()
        return updatePassword(email, newPassword)
    except Error as err:
        print(err)

def login(email, newPassword):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT login(%s, %s)"
        cursor.execute(query, (email, newPassword))
        result = cursor.fetchone()

        for success in result:
            cursor.close()
            conn.close()
            return success
    
    except Error as err:
        print(err)

def resetPassword(email, newPassword):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addPassChange(%s, \"Reset\", %s)"
        date = datetime.date.today()
        cursor.execute(query, (email, date))

        cursor.close()
        conn.close()
        return updatePassword(email, newPassword)
    except Error as err:
        print(err)

def firstPassword(email, newPassword):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addPassChange(%s, \"First Time\", %s)"
        date = datetime.date.today()
        cursor.execute(query, (email, date))

        cursor.close()
        conn.close()
        return updatePassword(email, newPassword)
    except Error as err:
        print(err)
        
def updateAddress(email, newUserAddress, oldUserAddress):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT updateAddress(%s, %s, %s)"
            cursor.execute(query, (email, newUserAddress, oldUserAddress))
    
            cursor.close()
            conn.close()
            return "Address successfully updated."
        else:
            return "Error updating address (Email not found)"
    except Error as err:
        print(err)

def addAddress(email, newAddress):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT addAddress(%s, %s)"
            cursor.execute(query, (email, newAddress,))

            cursor.close()
            conn.close()
            return "Address successfully added."
        else:
            cursor.close()
            conn.close()
            return "Error updating address (Email not found)"
    
    except Error as err:
        print(err)

def setDefaultAddress(email, defaultAddr):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT setAddressDefault(%s, %s)"
            cursor.execute(query, (email, defaultAddr,))

            cursor.close()
            conn.close()
            return "Default address set."
        else:
            cursor.close()
            conn.close()
            return "Error setting default address (Email not found)"

    except Error as err:
        print(err)

def getDefaultAddress(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT getDefaultAddress(%s)"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            for addr in result:
                cursor.close()
                conn.close()
                return addr
        else:
            cursor.close()
            conn.close()
            return "Error finding default address (Email not found)"
  
    except Error as err:
        print(err)

def getDriverAddresses(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getDriverAddresses(%s)"
        cursor.execute(query, (email,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
  
    except Error as err:
        print(err)

def getUserType(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getUserType(%s)"

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for userType in result:
            cursor.close()
            conn.close()
            return userType
    
    except Error as err:
        print(err)

def getUserID(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getUserID(%s)"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for userID in result:
            cursor.close()
            conn.close()
            return userID

    except Error as err:
        print(err)

def getUserEmail(id):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getUserEmail(%s)"
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        for userEmail in result:
            cursor.close()
            conn.close()
            return userEmail

    except Error as err:
        print(err)

def getDriverPhone(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getDriverPhone(%s)"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for phone in result:
            cursor.close()
            conn.close()
            return phone
        
    except Error as err:
        print(err)

def getDriverPoints(email, orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getDriverPoints(%s, %s)"
        cursor.execute(query, (email, orgID, ))
        result = cursor.fetchone()


        for points in result:
            cursor.close()
            conn.close()
            return int(points)
    
    except Error as err:
        print(err)

def checkPassword (email, password):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT checkPassword(%s, %s)"
        cursor.execute(query, (email, password,))
        result = cursor.fetchone()

        for correctPassword in result:
            cursor.close()
            conn.close()
            return correctPassword

    except Error as err:
        print(err)

def updateDriverPhone(email, newPhone):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT updateDriverPhone(%s, %s)"

        cursor.execute(query, (email, newPhone,))

        cursor.close()
        conn.close()
        return "Phone number successfully updated."
    except Error as err:
        print(err)

def setProfilePic(email, picture):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT setProfilePic(%s, %s)"
            cursor.execute(query, (email, picture,))
    
            cursor.close()
            conn.close()
            return "Profile picture successfully updated."
        else:
            return "Error updating profile picture (Email not found)"

    except Error as err:
        print(err)

def setOrgLogo(orgNo, logoPath):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL setOrgLogo(%s, %s)"
        cursor.execute(query, (orgNo, logoPath))

        cursor.close()
        conn.close()
        return "Logo successfully updated"

    except Error as err:
        print(err)

def getOrgLogo(orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT setOrgLogo(%s)"
        cursor.execute(query, (orgNo))
        resutl = cursor.fetchone()

        for logo in result:
            cursor.close()
            conn.close()
            return logo

    except Error as err:
        print(err)

def getProductsInCatalog(org):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getProductsInCatalog(%s)"
        cursor.execute(query, (org,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def checkIsInCatalog (productID, catalogID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT isInCatalog(%s, %s)"
        cursor.execute(query, (productID, catalogID,))
        result = cursor.fetchone()

        for inCatalog in result:
            cursor.close()
            conn.close()
            return inCatalog

    except Error as err:
        print(err)

def addToCatalog (productID, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addToCatalog(%s, %s)"
        cursor.execute(query, (productID, orgNo,))

        cursor.close()
        conn.close()
        return "Product successfuly added to catalog"
    
    except Error as err:
        print(err)

def clearCatalog(orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL clearCatalog(%s)"
        cursor.execute(query, (orgNo,))

        cursor.close()
        conn.close()
        return "Catalog cleared"
    
    except Error as err:
        print(err)

def removeFromCatalog (productID, catalogID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeFromCatalog(%s, %s)"
        cursor.execute(query, (productID, catalogID,))
        result = cursor.fetchone()

        for success in result:
            if success == True:
                cursor.close()
                conn.close()
                return "Product successfuly removed from catalog"

            else:
                cursor.close()
                conn.close()
                return "Error removing product (product or catalog does not exist)"
    
    except Error as err:
        print(err)

def createOrder (driverID, date, org):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createOrder(%s, %s, %s)"
        cursor.execute(query, (driverID, date, org))
        result = cursor.fetchone()

        for orderID in result:
            cursor.close()
            conn.close()
            return orderID
    
    except Error as err:
        print(err)

def cancelOrder (orderID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT cancelOrder(%s)"
        cursor.execute(query, (orderID,))

        cursor.close()
        conn.close()
        return "Order successfully canceled"
    
    except Error as err:
        print(err)

def completeOrder (driver, org, totCost):
    try:
        conn = getDB()
        cursor = getCursor(conn)
        
        query = "SELECT completeOrder(%s, %s, %s)"
        cursor.execute(query, (driver, org, totCost, ))

        cursor.close()
        conn.close()
        return "Order successfully completed"
    
    except Error as err:
        print(err)


def addToCart (driver, org, productID, amt):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addToCart(%s, %s, %s, %s)"
        cursor.execute(query, (driver, org, productID, amt,))

        cursor.close()
        conn.close()
        return "Product successfuly added to order"
    
    except Error as err:
        print(err)

def removeFromCart (driver, org, productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeFromCart(%s, %s, %s)"
        cursor.execute(query, (driver, org, productID,))

        cursor.close()
        conn.close()
        return "Product successfuly removed from catalog"
    
    except Error as err:
        print(err)

def checkIsInCart(driver, org, product):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT isInCart(%s, %s, %s)"
        cursor.execute(query, (driver, org, product))
        result = cursor.fetchone()

        for inCart in result:
            cursor.close()
            conn.close()
            return inCart
        
    except Error as err:
        print(err)

def getProductsInCart (driver, org):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getProductsInCart(%s, %s)"
        cursor.execute(query, (driver, org,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
    
    except Error as err:
        print(err)

def getDriverOrders(driver, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getDriverOrders(%s, %s)"
        cursor.execute(query, (driver, orgNo,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
    
    except Error as err:
        print(err)
    
def getSponsorOrders(orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getSponsorOrders(%s)"
        cursor.execute(query, (orgNo, ))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
    
    except Error as err:
        print(err)

def getQuantityInCart (driver, org, productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getQuantityInCart(%s, %s, %s)"
        cursor.execute(query, (driver, org, productID,))
        result = cursor.fetchone()

        for qty in result:
            cursor.close()
            conn.close()
            return qty
    
    except Error as err:
        print(err)

def updateQuantityInCart (driver, org, productID, newAmt):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT updateQuantity(%s, %s, %s, %s)"
        cursor.execute(query, (driver, org, productID, newAmt,))

        cursor.close()
        conn.close()
        return "Quantity successfully updated"
    
    except Error as err:
        print(err)

def checkIsInOrder (orderID, productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT isInOrder(%s, %s)"
        cursor.execute(query, (orderID, productID,))
        result = cursor.fetchone()

        for inOrder in result:
            cursor.close()
            conn.close()
            return inOrder
    
    except Error as err:
        print(err)

def checkInInCart (driver, org, product):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "Select isInCart(%s, %s, %s)"
        cursor.execute(query, (driver, org, product))
        result = cursor.fetchone()

        for inCart in result:
            cursor.close()
            conn.close()
            return inCart
    
    except Error as err:
        print(err)

def addToWishlist (driverID, productID, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addToWishlist(%s, %s, %s)"
        cursor.execute(query, (driverID, productID, orgNo, ))
        print(cursor.fetchone())

        cursor.close()
        conn.close()
        return "Product successfuly added to wishlist"
    
    except Error as err:
        print(err)

def removeFromWishlist (driverID, productID, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeFromWishlist(%s, %s, %s)"
        cursor.execute(query, (driverID, productID, orgNo, ))

        cursor.close()
        conn.close()
        return "Product successfuly removed from wishlist"
    
    except Error as err:
        print(err)

def checkIsInWishlist (driverID, productID, org):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT isInWishlist(%s, %s, %s)"
        cursor.execute(query, (driverID, productID, org))
        result = cursor.fetchone()

        for inWishlist in result:
            cursor.close()
            conn.close()
            return inWishlist
    
    except Error as err:
        print(err)

def getProductsInWishlist(driver, org):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getProductsInWishlist(%s, %s)"
        cursor.execute(query, (driver, org, ))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
    
    except Error as err:
        print(err)

def createProduct (id, prodName, price, img):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        name = ''

        for i in prodName:
            if i in string.printable or i in string.punctuation:
                name += i
        
        query = "SELECT createProduct(%s, %s, %s, %s)"
        cursor.execute(query, (id, name, price, img, ))

        cursor.close()
        conn.close()
        return "Product successfully created"
    except Error as err:
        print(err)

def getProduct (id):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getProduct(%s)"
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        return result
    except Error as err:
        print(err)

def updatePrice (productID, newPrice):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT updatePrice(%s, %s)"
        cursor.execute(query, (productID, newPrice,))

        cursor.close()
        conn.close()
        return "Product price successfully updated"

    except Error as err:
        print(err)

def getProductName (productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getProductName(%s)"
        cursor.execute(query, (productID,))
        result = cursor.fetchone()

        for productName in result:
            cursor.close()
            conn.close()
            return productName

    except Error as err:
        print(err)

def getProductPrice (productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getProductPrice(%s)"
        cursor.execute(query, (productID,))
        result = cursor.fetchone()

        for productPrice in result:
            cursor.close()
            conn.close()
            return productPrice

    except Error as err:
        print(err)

def getPointChangeReason(reasonID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getPointChangeReason(%s)"
        cursor.execute(query, (reasonID,))
        result = cursor.fetchone()

        print(result)

        cursor.close()
        conn.close()
        return result
    
    except Error as err:
        print(err)

def getPointChangeReasons(orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getPointChangeReasons(%s)"
        cursor.execute(query, (orgNo,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def addPointChangeReason (reason, numPoints, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addPointChangeReason(%s, %s, %s)"
        cursor.execute(query, (reason, numPoints, orgNo))
        result = cursor.fetchone()

        for reasonID in result:
            cursor.close()
            conn.close()
            return reasonID

    except Error as err:
        print(err)

def removePointChangeReason (reason):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL removePointChangeReason(%s)"
        cursor.execute(query, (reason,))

        cursor.close()
        conn.close()
        return "Points successfully moved"
    
    except Error as err:
        print(err)

def updatePointChangeReason (reason, newDesc, newPoints):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL updatePointChangeReason(%s, %s, %s)"
        cursor.execute(query, (reason, newDesc, newPoints))

        cursor.close()
        conn.close()
        return "Point change reason successfully changed"
    
    except Error as err:
        print(err)

def adjustPoints (driverEmail, sponsorEmail, reason, amt):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT manualPointChange(%s, %s, %s, %s, %s)"

        now = datetime.now()
        changeDate = now.strftime('%Y-%m-%d')
        cursor.execute(query, (driverEmail, sponsorEmail, reason, amt, changeDate))
        result = cursor.fetchone()

        for newTotal in result:
            cursor.close()
            conn.close()
            return newTotal

    except Error as err:
        print(err)

def updatePointConversion(orgNo, newConversion):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL updatePointConversion(%s, %s)"
        cursor.execute(query, (orgNo, newConversion))

        cursor.close()
        conn.close()
        return "Point conversion successfully updated"

    except Error as err:
        print(err)

def getPointConversion(orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getPointConversion(%s)"
        cursor.execute(query, (orgNo, ))
        result = cursor.fetchone()

        for pointRate in result:
            cursor.close()
            conn.close()
            return pointRate
    
    except Error as err:
        print(err)

def spendPoints (driverEmail, cost):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT changePointTotal(%s, %s)"
        cursor.execute(query, (driverEmail, cost))
        result = cursor.fetchone()

        for newTotal in result:
            cursor.close()
            conn.close()
            return newTotal

    except Error as err:
        print(err)

def getRandomPassword():
    #Generate a random password that is 20 characters long
    randPassword = ''
    for _ in range(20):
        randPassword = randPassword + random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)

    return randPassword

def createOrg(name):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createOrg(%s, %s)"
        cursor.execute(query, (name, 0.01))
        result = cursor.fetchone()

        for orgNo in result:
            cursor.close()
            conn.close()
            return orgNo

    except Error as err:
        print(err)

def removeOrg(orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL removeOrg(%s)"
        cursor.execute(query, (orgNo, ))
        
        cursor.close()
        conn.close()
        return "Organization delted"

    except Error as err:
        print(err)

def getOrgNo (userEmail):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getOrgNo(%s)"
        cursor.execute(query, (userEmail,))
        result = cursor.fetchone()

        for orgNo in result:
            cursor.close()
            conn.close()
            return orgNo

    except Error as err:
        print(err)

def getOrgName (orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getOrgName(%s)"
        cursor.execute(query, (orgID,))
        result = cursor.fetchone()

        for orgName in result:
            cursor.close()
            conn.close()
            return orgName

    except Error as err:
        print(err)

def getOrgs ():
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getOrgs()"
        cursor.execute(query, ())
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)
        

def createDriver(name, email, password, address, phone, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createDriver(%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, password, address, phone, orgNo))

        return "Driver successfully created" 

    except Error as err:
        print(err)

def getDrivers(org):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getDrivers(%s)"
        cursor.execute(query, (org,))
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def getAllDrivers():
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getAllDrivers()"
        cursor.execute(query, ())
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
    
    except Error as err:
        print(err)

def getDriverOrgs (driverID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getDriverOrgs(%s)"
        cursor.execute(query, (driverID,))
        result = cursor.fetchall()

        
        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def addDriverOrg (driverID, newOrg):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL addDriverOrg(%s, %s)"
        cursor.execute(query, (driverID, newOrg))
        
        cursor.close()
        conn.close()
        return "Successfully added driver to org"

    except Error as err:
        print(err)

def createSponsor(name, email, password, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createSponsor(%s, %s, %s, %s)"
        cursor.execute(query, (name, email, password, orgNo))
        
        cursor.close()
        conn.close()
        return "Sponsor successfully created" 

    except Error as err:
        print(err)

def getSponsors(org):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getSponsors(%s)"
        cursor.execute(query, (org,))
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def createAdmin(name, email, password):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createAdmin(%s, %s, %s)"
        cursor.execute(query, (name, email, password))

        cursor.close()
        conn.close()
        return "Admin successfully created" 

    except Error as err:
        print(err)

def getAllAdmins():
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getAllAdmins()"
        cursor.execute(query, ())
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def createApplicant(date, name, email, phone, address, orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createApplicant(%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (date, name, email, phone, address, orgID))
        result = cursor.fetchone()

        for applicantID in result:
            cursor.close()
            conn.close()
            return applicantID
        
    except Error as err:
        print(err)

def acceptApplicant(email, reasoning, password, acceptDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT acceptApplicant(%s, %s, %s, %s)"
        cursor.execute(query, (email, reasoning, password, acceptDate))
        result = cursor.fetchone()

        for driverID in result:
            cursor.close()
            conn.close()
            return driverID
        
    except Error as err:
        print(err)

def rejectApplicant(email, reasoning, rejectDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT rejectApplicant(%s, %s, %s)"
        cursor.execute(query, (email, reasoning, rejectDate))

        cursor.close()
        conn.close()
        return "Applicant successfully rejected"
        
    except Error as err:
        print(err)

def removeDriver(driverID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeDriver(%s)"
        cursor.execute(query, (driverID,))

        cursor.close()
        conn.close()
        return "Driver successfully deleted" 

    except Error as err:
        print(err)

def removeSponsor (sponsorID, newSponsor):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeSponsor(%s, %s)"
        cursor.execute(query, (sponsorID, newSponsor))

        cursor.close()
        conn.close()
        return "Sponsor successfully deleted" 

    except Error as err:
        print(err)

def removeAdmin(adminID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeAdmin(%s)"
        cursor.execute(query, (adminID,))

        cursor.close()
        conn.close()
        return "Admin successfully deleted" 

    except Error as err:
        print(err)

def getProfilePic(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getProfilePic(%s)"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for profilePic in result:
            cursor.close()
            conn.close()
            return profilePic

    except Error as err:
        print(err)

def getOrgLogo(orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getOrgLogo(%s)"
        cursor.execute(query, (orgNo,))
        result = cursor.fetchone()

        for profilePic in result:
            cursor.close()
            conn.close()
            return profilePic

    except Error as err:
        print(err)

def getUserName(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getUserName(%s)"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for name in result:
            cursor.close()
            conn.close()
            return name

    except Error as err:
        print(err)

def indvDriverPointChangeReport(startDate, endDate, orgID, driverID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL indvDriverPointChangeRep(%s, %s, %s, %s)"
        cursor.execute(query, (start, end, orgID, driverID))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def allDriverPointChangeReport(startDate, endDate, orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL allDriverPointChangeRep(%s, %s, %s)"
        cursor.execute(query, (start, end, orgID))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def indvSponsorSaleReport(startDate, endDate, detailed, driverID, orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL indvSponsorSaleRep(%s, %s, %s, %s, %s)"
        cursor.execute(query, (start, end, detailed, driverID, orgID))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def allSponsorSaleReport(startDate, endDate, detailed):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL allSponsorSaleRep(%s, %s, %s)"
        cursor.execute(query, (start, end, detailed))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def driverSaleReport(startDate, endDate, detailed, driverID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL driverSaleRep(%s, %s, %s, %s)"
        cursor.execute(query, (start, end, detailed, driverID))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def indvSponsorInvoice(startDate, endDate, orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL indvSponsorInvoice(%s, %s, %s)"
        cursor.execute(query, (start, end, orgID))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def allSponsorInvoice(startDate, endDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL allSponsorInvoice(%s, %s)"
        cursor.execute(query, (start, end))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def driverApplicationsReport(startDate, endDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL driverApplicationsRep(%s, %s)"
        cursor.execute(query, (start, end))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def pointChangeReport(startDate, endDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL pointChangeRep(%s, %s)"
        cursor.execute(query, (start, end))
        result = cursor.fetchall()

        print(result)

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def passwordChangeReport(startDate, endDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL passwordChangeRep(%s, %s)"
        cursor.execute(query, (start, end))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def loginAttemptsReport(startDate, endDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL loginAttemptsRep(%s, %s)"
        cursor.execute(query, (start, end))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def addOrgPayment (name, ccNum, ccSec, ccDate, billAddr, org):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        digits = ccNum[12] + ccNum[13] + ccNum[14] + ccNum[15]

        query = "CALL addOrgPayment(%s, %s, %s, %s, %s, %s, %s)"
        ccDate = datetime.strptime(ccDate, '%m/%y').date()
        cursor.execute(query, (name, ccNum, digits, ccSec, ccDate, billAddr, org))

        cursor.close()
        conn.close()
        return "Payment successfully added"

    except Error as err:
        print(err)

def updateOrgPayment (name, ccNum, ccSec, ccDate, billAddr, org, payID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        digits = ccNum[12] + ccNum[13] + ccNum[14] + ccNum[15]

        query = "CALL updateOrgPayment(%s, %s, %s, %s, %s, %s, %s, %s)"
        ccDate = datetime.strptime(ccDate, '%m/%y').date()
        cursor.execute(query, (name, ccNum, digits, ccSec, ccDate, billAddr, org, payID))

        cursor.close()
        conn.close()
        return "Payment successfully updated"

    except Error as err:
        print(err)

def getOrgPayment(org):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getOrgPayment(%s)"
        cursor.execute(query, (org, ))
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def emailNewDriver(driverEmail, password):
    driverName = getUserName(driverEmail)

    result = getDriverOrgs(driverEmail)
    count = 0

    for _ in result:
        count += 1
    
    if count > 1:
        subject = "Acceptance into New Sponsor"

        message = """\
        Congratualations %s!
        
        You're applicantion to another sponsor organization has been accepted. You can login as normal, and change to the new organization on your dashboard.
        
        Login Link: http://ec2-23-23-99-117.compute-1.amazonaws.com/""" % (driverName)
    subject = "Acceptance to the Good Driver Incentive Program"

    message = """\
    Welcome %s!
    
    Congratualations! You've been accepted into the Good Driver Incentive Program. Once you login for the first time, you'll be able to create your own password and start earning points. For your first login, please use this temporary password: %s. Welcome to the Program!
    
    Login Link: http://ec2-23-23-99-117.compute-1.amazonaws.com/""" % (driverName,password)

    #Send email
    email = EmailMessage(subject, message, 'gooddriverprogram@gmail.com', [driverEmail])
    email.send()

def emailRejectedDriver(driverEmail):
    try:
        conn = getDB()
        cursor = getCursor(conn)
        driverName = getUserName(driverEmail)

        query = "SELECT * FROM APPLICANT WHERE Email=%s"
        cursor.execute(query, (driverEmail,))
        result = cursor.fetchone()

        if result != None:
            driverName = result[4]

        cursor.close()
        conn.close()
        
        subject = "Rejected from the Good Driver Incentive Program"

        message = """\
        Hello %s!
        
        We regret to inform you that you have been rejected from the Good Driver Incentive Program.""" % (driverName)

        #Send email
        email = EmailMessage(subject, message, 'gooddriverprogram@gmail.com', [driverEmail])
        email.send()
    
    except Error as err:
        print(err)

def emailNewSponsor(sponsorEmail, password, orgNo):
    sponsorName = getUserName(sponsorEmail)
    orgName = getOrgName(orgNo)
    
    subject = "Added as Sponsor User in Good Driver Incentive Program"

    message = """\
    Welcome %s!
    
    Welcome to the Good Driver Incentive Program. You have been added as a new sponsor user for %s. Once you login for the first time, you'll be able to create your own password and be able to access and update the information pertaining to your sponsor. For your first login, please use this temporary password: %s. Welcome to the Program!
    
    Login Link: http://ec2-23-23-99-117.compute-1.amazonaws.com/""" % (sponsorName, orgName, password)

    #Send email
    email = EmailMessage(subject, message, 'gooddriverprogram@gmail.com', [sponsorEmail])
    email.send()

def emailNewAdmin(adminEmail, password):
    adminName = getUserName(adminEmail)
    
    subject = "Added as Administrator in Good Driver Incentive Program"

    message = """\
    Welcome %s!
    
    Welcome to the Good Driver Incentive Program. You have been added as a new administrator. Once you login for the first time, you'll be able to create your own password and be able to access and manage the various functions fo the application. For your first login, please use this temporary password: %s. Welcome to the Program!
    
    Login Link: http://ec2-23-23-99-117.compute-1.amazonaws.com/""" % (adminName, password)

    #Send email
    email = EmailMessage(subject, message, 'gooddriverprogram@gmail.com', [adminEmail])
    email.send()

def createTempDriver(tempEmail, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createTempDriver(%s, %s)"
        cursor.execute(query, (tempEmail, orgNo))
        result = cursor.fetchone()

        for tempID in result:
            cursor.close()
            conn.close()
            return tempID

    except Error as err:
        print(err)

def removeTempDriver(tempID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL removeTempDriver(%s)"
        cursor.execute(query, (tempID, ))

        cursor.close()
        conn.close()
        return "Successfully deleted temporary driver"

    except Error as err:
        print(err)

def createTempSponsor(tempEmail, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createTempSponsor(%s, %s)"
        cursor.execute(query, (tempEmail, orgNo))
        result = cursor.fetchone()

        for tempID in result:
            cursor.close()
            conn.close()
            return tempID

    except Error as err:
        print(err)

def removeTempSponsor(tempID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL removeTempSponsor(%s)"
        cursor.execute(query, (tempID, ))

        cursor.close()
        conn.close()
        return "Successfully deleted temporary Sponsor"

    except Error as err:
        print(err)

def getKeywords(org):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL getKeywords(%s)"
        cursor.execute(query, (org, ))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def addKeyword(org, keyword):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addKeyword(%s, %s)"
        cursor.execute(query, (org, keyword))
        result = cursor.fetchone()

        for wordID in result:
            cursor.close()
            conn.close()
            return wordID

    except Error as err:
        print(err)

def removeKeyword(org, wordID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL removeKeyword(%s, %s)"
        cursor.execute(query, (org, wordID))

        cursor.close()
        conn.close()
        return "Keyword successfully removed"

    except Error as err:
        print(err)
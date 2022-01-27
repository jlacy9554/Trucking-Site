DELIMITER ;;

DROP FUNCTION IF EXISTS emailExists;

CREATE FUNCTION emailExists(userEmail VARCHAR(50))
RETURNS BOOLEAN
READS SQL DATA
    BEGIN
        DECLARE doesExist BOOLEAN;
        SELECT EXISTS (
            SELECT Email 
            FROM USER
            WHERE Email = userEmail) INTO doesExist;

        RETURN doesExist;
    END;;

DROP FUNCTION IF EXISTS createWishlist;

CREATE FUNCTION createWishlist (user INT, org INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        INSERT INTO WISHLIST (DriverID, OrgID) VALUES (user, org);

        SELECT ListID INTO newID
        FROM WISHLIST
        WHERE DriverID = user;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS createUser;

CREATE FUNCTION createUser (userName VARCHAR(100), userEmail VARCHAR(50), userPassword VARCHAR(20))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE validEmail BOOLEAN;
        DECLARE newID INT;

        SELECT emailExists (userEmail) INTO validEmail;

        IF validEmail = TRUE THEN
            SET newID = -1;
        ELSE
            INSERT INTO USER (Name, Email, HashedPassword, ProfilePicPath) VALUES (userName, userEmail, SHA(userPassword), 'Defaultpfp.png');

            SELECT UserID INTO newID
            FROM USER
            WHERE Email = userEmail;
        END IF;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS getUserID;

CREATE FUNCTION getUserID (userEmail VARCHAR(50))
RETURNS INT
READS SQL DATA
    BEGIN
        DECLARE id INT;

        SELECT userID INTO id
        FROM USER
        WHERE Email = userEmail;

        RETURN id;
    END;;

DROP PROCEDURE IF EXISTS getUserEmail;

CREATE PROCEDURE getUserEmail (id INT)
READS SQL DATA
    BEGIN
        SELECT Email
        FROM USER
        WHERE UserID = id;
    END;;

DROP FUNCTION IF EXISTS createAdmin;

CREATE FUNCTION createAdmin (userName VARCHAR(100), userEmail VARCHAR(50), userPassword VARCHAR(20))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        SELECT createUser(userName, userEmail, userPassword) INTO newID;

        IF newID > -1 THEN
            INSERT INTO ADMINISTRATOR (UserID) VALUES (newID);
        END IF;

        RETURN newID;
    END;;

DROP PROCEDURE IF EXISTS getAllAdmins;

CREATE PROCEDURE getAllAdmins ()
    BEGIN
        SELECT ADMINISTRATOR.UserID, Name, Email
        FROM USER, ADMINISTRATOR
        WHERE ADMINISTRATOR.UserID = USER.UserID;
    END;;

DROP FUNCTION IF EXISTS createSponsor;

CREATE FUNCTION createSponsor (userName VARCHAR(100), userEmail VARCHAR(50), userPassword VARCHAR(20), organization INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        SELECT createUser(userName, userEmail, userPassword) INTO newID;

        IF newID > -1 THEN
            INSERT INTO SPONSOR (UserID, OrgID) VALUES (newID, organization);
        END IF;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS createTempSponsor;

CREATE FUNCTION createTempSponsor (tempEmail VARCHAR(50), organization INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        SELECT createSponsor('Temp Sponsor', tempEmail, 'temp', organization) INTO newID;

        RETURN newID;
    END;;

DROP PROCEDURE IF EXISTS removeTempSponsor;

CREATE PROCEDURE removeTempSponsor (sponsor INT)
    BEGIN
        DELETE FROM POINT_CHANGE
            WHERE SponsorID = sponsor;

        DELETE FROM LOGIN_ATTEMPT
            WHERE UserID = sponsor;

        DELETE FROM SPONSOR
            WHERE UserID = sponsor;

        DELETE FROM PASSWORD_CHANGE
            WHERE UserID = sponsor;

        DELETE FROM USER
            WHERE UserID = sponsor;
    END;;

DROP PROCEDURE IF EXISTS getSponsors;

CREATE PROCEDURE getSponsors (organization INT)
    BEGIN
        SELECT SPONSOR.UserID, Name, Email
        FROM USER, SPONSOR
        WHERE USER.UserID = SPONSOR.UserID AND SPONSOR.OrgID = organization;
    END;;

DROP FUNCTION IF EXISTS createDriver;

CREATE FUNCTION createDriver (userName VARCHAR(100), userEmail VARCHAR(50), userPassword VARCHAR(20), addr VARCHAR(100), phone CHAR(12), organization INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;
        DECLARE wishID INT;

        SELECT createUser(userName, userEmail, userPassword) INTO newID;

        IF newID > -1 THEN
            INSERT INTO DRIVER (UserID, PhoneNo)
                VALUES (newID, phone);
            INSERT INTO DRIVER_ADDRESSES (DriverID, Address, DefaultAddr)
                VALUES (newID, addr, TRUE);
            INSERT INTO DRIVER_ORGS (UserID, OrgID, Points)
                VALUES (newID, organization, 0);
            SELECT createWishlist(newID, organization) INTO wishID;
        END IF;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS createTempDriver;

CREATE FUNCTION createTempDriver(email VARCHAR(50), orgNo INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newDriver INT;

        SELECT createDriver('Temp Driver', email, 'temp', 'Temp Address', '555-555-5555', orgNo) INTO newDriver;

        UPDATE DRIVER_ORGS
            SET
                Points = 1000
            WHERE UserID = newDriver AND OrgID = orgNo;

        RETURN newDriver;
    END;;

DROP PROCEDURE IF EXISTS removeTempDriver;

CREATE PROCEDURE removeTempDriver (driver INT)
    BEGIN
        DECLARE list INT;
        DECLARE orderID INT;

        SELECT ListID INTO list
        FROM WISHLIST
        WHERE DriverID = driver;

        SELECT OrderID INTO orderID
        FROM BELONGS_TO
        WHERE DriverID = driver;

        DELETE FROM IS_IN_WISHLIST
            WHERE ListID = list;
        
        DELETE FROM WISHLIST
            WHERE ListID = list;

        DELETE FROM BELONGS_TO
            WHERE DriverID = driver;

        DELETE FROM IS_IN_ORDER
            WHERE OrderID = driver;

        DELETE FROM DRIVER_ORDER
            WHERE OrderID = driver;

        DELETE FROM POINT_CHANGE
            WHERE DriverID = driver;

        DELETE FROM LOGIN_ATTEMPT
            WHERE UserID = driver;

        DELETE FROM DRIVER_ADDRESSES
            WHERE DriverID = driver;

        DELETE FROM DRIVER_ORGS
            WHERE UserID = driver;

        DELETE FROM DRIVER
            WHERE UserID = driver;

        DELETE FROM PASSWORD_CHANGE
            WHERE UserID = driver;

        DELETE FROM USER
            WHERE UserID = driver;
    END;;

DROP PROCEDURE IF EXISTS getDrivers;

CREATE PROCEDURE getDrivers (organization INT)
    BEGIN
        SELECT DRIVER.UserID, Name, Email
        FROM USER, DRIVER, DRIVER_ORGS
        WHERE USER.UserID = DRIVER.UserID AND DRIVER.UserID = DRIVER_ORGS.UserID AND
            DRIVER_ORGS.OrgID = organization;
    END;;

DROP PROCEDURE IF EXISTS getAllDrivers;

CREATE PROCEDURE getAllDrivers ()
    BEGIN
        SELECT DRIVER.UserID, Name
        FROM USER, DRIVER
        WHERE USER.UserID = DRIVER.UserID;
    END;;

DROP PROCEDURE IF EXISTS getDriverOrgs;

CREATE PROCEDURE getDriverOrgs (driver INT)
    BEGIN
        SELECT ORGANIZATION.OrgID, ORGANIZATION.Name
        FROM DRIVER_ORGS, ORGANIZATION
        WHERE DRIVER_ORGS.OrgID = ORGANIZATION.OrgID AND
            DRIVER_ORGS.UserID = driver;
    END;;

DROP PROCEDURE IF EXISTS addDriverOrg;

CREATE PROCEDURE addDriverOrg (driver INT, newOrg INT)
MODIFIES SQL DATA
    BEGIN
        INSERT INTO DRIVER_ORGS (UserID, OrgID, Points)
            VALUES (driver, newOrg, 0);
    END;;

DROP FUNCTION IF EXISTS createApplicant;

CREATE FUNCTION createApplicant (currDate DATE, userName VARCHAR(100), email VARCHAR(50), phone CHAR(12), address VARCHAR(100), orgID INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newApplicant INT;

        INSERT INTO APPLICANT (ApplicantDate, IsAccepted, Reason, ApplicantName, Email, PhoneNo, HomeAddress, OrgID) VALUES (currDate, false, "Just applied", userName, email, phone, address, orgID);

        SELECT ApplicantID INTO newApplicant
        FROM APPLICANT
        WHERE ApplicantID = @@Identity;

        RETURN newApplicant;
    END;;

DROP FUNCTION IF EXISTS acceptApplicant;

CREATE FUNCTION acceptApplicant (userEmail VARCHAR(50), reasoning VARCHAR(150), randomPassword VARCHAR(20), acceptDate DATE)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE driverName VARCHAR(100);
        DECLARE phone CHAR(12);
        DECLARE address VARCHAR(100);
        DECLARE org INT;
        DECLARE newDriver INT;
        DECLARE driverExists BOOLEAN;

        UPDATE APPLICANT
            SET
                IsAccepted = true,
                Reason = reasoning,
                ApplicantDate = acceptDate
            WHERE Email = userEmail;

        SELECT ApplicantName, PhoneNo, HomeAddress, OrgID
        INTO driverName, phone, address, org
        FROM APPLICANT
        WHERE Email = userEmail;

        SELECT emailExists(userEmail) INTO driverExists;

        IF (!driverExists) THEN
            SELECT CreateDriver(driverName, userEmail, randomPassword, address, phone, org) INTO newDriver;
        ELSE
            SELECT getUserID(userEmail) INTO newDriver;
            INSERT INTO DRIVER_ORGS (UserID, OrgID, Points)
                VALUES (newDriver, org, 0);
        END IF;

        RETURN newDriver;
    END;;

DROP FUNCTION IF EXISTS rejectApplicant;

CREATE FUNCTION rejectApplicant (userEmail VARCHAR(50), reasoning VARCHAR(150), rejectDate DATE)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        UPDATE APPLICANT
            SET
                Reason = reasoning,
                ApplicantDate = rejectDate
            WHERE Email = userEmail;

        RETURN 0;
    END;;

DROP FUNCTION IF EXISTS createCatalog;

CREATE FUNCTION createCatalog ()
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        INSERT INTO ORG_CATALOG () VALUES ();

        SELECT CatalogID INTO newID
        FROM ORG_CATALOG
        WHERE CatalogID = @@Identity;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS createOrg;

CREATE FUNCTION createOrg (orgName VARCHAR(50), pointRate FLOAT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;
        DECLARE catalogue INT;

        SELECT createCatalog() INTO catalogue;

        INSERT INTO ORGANIZATION (Name, LogoPath, PointConversion, CatalogID) VALUES (orgName, 'defaultLogo.jpg', pointRate, catalogue);

        SELECT OrgID INTO newID
        FROM ORGANIZATION
        WHERE OrgID = @@Identity;

        RETURN newID;
    END;;

DROP PROCEDURE IF EXISTS removeOrg;

CREATE PROCEDURE removeOrg (orgNo INT)
    BEGIN
        DECLARE catalogue INT;

        SELECT CatalogID INTO catalogue
        FROM ORGANIZATION
        WHERE OrgID = orgNo;

        DELETE FROM APPLICANT
        WHERE OrgID = orgNo;

        DELETE FROM IS_IN_CATALOG
        WHERE CatalogID = catalogue;

        DELETE FROM POINT_CHANGE_REASON
        WHERE OrgID = orgNo;

        DELETE FROM ORGANIZATION
        WHERE OrgID = orgNo;

    END;;

DROP PROCEDURE IF EXISTS getOrgs;

CREATE PROCEDURE getOrgs()
    BEGIN
        SELECT OrgID, Name
        FROM ORGANIZATION;
    END;;

DROP FUNCTION IF EXISTS updateEmail;

CREATE FUNCTION updateEmail (oldEmail VARCHAR(50), newEmail VARCHAR(50))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE user INT;

        SELECT UserID INTO user
        FROM USER
        WHERE Email = oldEmail;

        UPDATE USER
            SET 
                Email = newEmail
        WHERE userID = user;

        RETURN user;
    END;;

DROP FUNCTION IF EXISTS updatePassword;

CREATE FUNCTION updatePassword (userEmail VARCHAR(50), newPass VARCHAR(20))
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE emailExists BOOLEAN;

        SELECT EXISTS (
            SELECT Email
            FROM USER
            WHERE Email = userEmail
        ) INTO emailExists;

        UPDATE USER
            SET HashedPassword = SHA(newPass)
        WHERE Email = userEmail;

        RETURN emailExists;
    END;;

DROP FUNCTION IF EXISTS addPassChange;

CREATE FUNCTION addPassChange (userEmail VARCHAR(50), changeType VARCHAR(10), currDate DATE)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newChange INT;
        DECLARE user INT;

        SELECT getUserID(userEmail) INTO user;
        
        INSERT INTO PASSWORD_CHANGE (ChangeDate, ChangeType, UserID) VALUES (currDate, changeType, user);

        SELECT ChangeNo INTO newChange
        FROM PASSWORD_CHANGE
        WHERE ChangeNo = @@Identity;

        RETURN newChange;
    END;;

DROP FUNCTION IF EXISTS addAddress;

CREATE FUNCTION addAddress (userEmail VARCHAR(50), newAddress VARCHAR(100))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newAddressId INT;
        DECLARE user INT;
        DECLARE defaultExists BOOLEAN;

        SELECT getUserID(userEmail) INTO user;
        
        INSERT INTO DRIVER_ADDRESSES (DriverID, Address, DefaultAddr) VALUES (user, newAddress, False);

        SELECT AddressID INTO newAddressId
        FROM DRIVER_ADDRESSES
        WHERE AddressID = @@Identity;

        SELECT EXISTS (
            SELECT AddressID
            FROM DRIVER_ADDRESSES
            WHERE DefaultAddr = TRUE
        ) INTO defaultExists;

        IF (!defaultExists) THEN
            UPDATE DRIVER_ADDRESSES
                SET
                    DefaultAddr = TRUE
                WHERE AddressID = newAddressId;
        END IF;

        RETURN newAddressId;
    END;;
    
DROP FUNCTION IF EXISTS updateAddress;

CREATE FUNCTION updateAddress (userEmail VARCHAR(50), newAddress VARCHAR(100), oldAddress VARCHAR(100))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE user INT;
        DECLARE addressNo INT;

        SELECT getUserID(userEmail) INTO user;

        SELECT AddressId INTO addressNo
        FROM DRIVER_ADDRESSES
        WHERE Address = oldAddress AND DriverID = user;

        UPDATE DRIVER_ADDRESSES
            SET
                Address = newAddress
            WHERE AddressID = addressNo;
        
        RETURN 0;
    END;;

DROP FUNCTION IF EXISTS getUserName;

CREATE FUNCTION getUserName (userEmail VARCHAR(50))
RETURNS VARCHAR(100)
READS SQL DATA
    BEGIN
        DECLARE userName VARCHAR(100);

        SELECT Name INTO userName
        FROM USER
        WHERE Email = userEmail;

        RETURN userName;
    END;;

DROP PROCEDURE IF EXISTS getDriverAddresses;

CREATE PROCEDURE getDriverAddresses (userEmail VARCHAR(50))
    BEGIN
        DECLARE user INT;

        SELECT getUserID(userEmail) INTO user;

        SELECT AddressID, Address
        FROM DRIVER_ADDRESSES
        WHERE DriverID = user;
    END;;

DROP FUNCTION IF EXISTS setAddressDefault;

CREATE FUNCTION setAddressDefault (userEmail VARCHAR(50), defaultAddress VARCHAR(100))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE user INT;
        DECLARE addrID INT;

        SELECT getUserID(userEmail) INTO user;

        SELECT AddressID INTO addrID
        FROM DRIVER_ADDRESSES
        WHERE Address = defaultAddress AND UserID = user;

        UPDATE DRIVER_ADDRESSES
            SET
                DefaultAddr = False
            WHERE DefaultAddr = True;

        UPDATE DRIVER_ADDRESSES
            SET
                DefaultAddr = True
            WHERE AddressID = addrID;

        RETURN 0;
    END;;

DROP FUNCTION IF EXISTS getDefaultAddress;

CREATE FUNCTION getDefaultAddress (userEmail VARCHAR(50))
RETURNS VARCHAR(100)
READS SQL DATA
    BEGIN
        DECLARE user INT;
        DECLARE defaultAddress VARCHAR(100);

        SELECT getUserID(userEmail) INTO user;

        SELECT Address INTO defaultAddress
        FROM DRIVER_ADDRESSES
        WHERE DriverID = user AND DefaultAddr = True;

        RETURN defaultAddress;
    END;;

DROP FUNCTION IF EXISTS getDriverPhone;

CREATE FUNCTION getDriverPhone (userEmail VARCHAR(50))
RETURNS CHAR(12)
READS SQL DATA
    BEGIN
        DECLARE phone CHAR(12);
        DECLARE user INT;

        SELECT getUserID(userEmail) INTO user;

        SELECT PhoneNo INTO phone
        FROM DRIVER
        WHERE UserID = user;

        RETURN phone;
    END;;

DROP FUNCTION IF EXISTS updateDriverPhone;

CREATE FUNCTION updateDriverPhone (userEmail VARCHAR(50), newPhone CHAR(12))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE user INT;

        SELECT getUserID(userEmail) INTO user;

        UPDATE DRIVER
            SET
                PhoneNo = newPhone
            WHERE UserID = user;

        RETURN 0;
    END;;

DROP FUNCTION IF EXISTS setProfilePic;

CREATE FUNCTION setProfilePic (userEmail VARCHAR(50), newPic VARBINARY(256))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        UPDATE USER
            SET ProfilePicPath = newPic
        WHERE Email = userEmail;

        RETURN 0;
    END;;

DROP FUNCTION IF EXISTS getOrgNo;

CREATE FUNCTION getOrgNo (userEmail VARCHAR(50))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE orgNo INT;
        DECLARE userType VARCHAR(10);
        DECLARE user INT;

        SELECT getUserType(userEmail) INTO userType;
        SELECT getUserID(userEmail) INTO user;

        IF userType = "Driver" THEN
            SELECT OrgID INTO orgNo
            FROM DRIVER_ORGS
            WHERE UserID = user;

        ELSEIF userType = "Sponsor" THEN
            SELECT OrgID INTO orgNo
            FROM SPONSOR
            WHERE UserID = user;
        END IF;

        RETURN orgNo;
    END;;

DROP PROCEDURE IF EXISTS getOrgName;

CREATE PROCEDURE getOrgName (org INT)
READS SQL DATA
    BEGIN
        SELECT Name
        FROM ORGANIZATION
        WHERE OrgID = org;
    END;;

DROP FUNCTION IF EXISTS getOrgLogo;

CREATE FUNCTION getOrgLogo(orgNo INT)
RETURNS VARCHAR(100)
READS SQL DATA
    BEGIN
        DECLARE logo VARCHAR(100);

        SELECT LogoPath INTO logo
        FROM ORGANIZATION
        WHERE OrgID = orgNo;

        RETURN logo;
    END;;

DROP PROCEDURE IF EXISTS setOrgLogo;

CREATE PROCEDURE setOrgLogo(orgNo INT, logoPath VARCHAR(100))
    BEGIN
        UPDATE ORGANIZATION
            SET
                LogoPath = logoPath
        WHERE OrgID = orgNo;
    END;;

DROP FUNCTION IF EXISTS removeDriver;

CREATE FUNCTION removeDriver(driver INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE list INT;

        SELECT ListID INTO list
        FROM WISHLIST
        WHERE DriverID = driver;

        DELETE FROM IS_IN_WISHLIST
            WHERE ListID = list;
        
        DELETE FROM WISHLIST
            WHERE ListID = list;

        DELETE FROM BELONGS_TO
            WHERE DriverID = driver;

        DELETE FROM POINT_CHANGE
            WHERE DriverID = driver;

        DELETE FROM LOGIN_ATTEMPT
            WHERE UserID = driver;

        DELETE FROM DRIVER_ADDRESSES
            WHERE DriverID = driver;

        DELETE FROM DRIVER_ORGS
            WHERE UserID = driver;

        DELETE FROM DRIVER
            WHERE UserID = driver;

        DELETE FROM PASSWORD_CHANGE
            WHERE UserID = driver;

        DELETE FROM USER
            WHERE UserID = driver;

        RETURN 0;
    END;;

DROP FUNCTION IF EXISTS removeSponsor;

CREATE FUNCTION removeSponsor(sponsor INT, newSponsor INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        UPDATE POINT_CHANGE
            SET SponsorID = newSponsor
            WHERE SponsorID = sponsor;

        DELETE FROM LOGIN_ATTEMPT
            WHERE UserID = sponsor;

        DELETE FROM SPONSOR
            WHERE UserID = sponsor;

        DELETE FROM PASSWORD_CHANGE
            WHERE UserID = sponsor;

        DELETE FROM USER
            WHERE UserID = sponsor;

        RETURN 0;
    END;;

DROP FUNCTION IF EXISTS removeAdmin;

CREATE FUNCTION removeAdmin (adminID INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DELETE FROM LOGIN_ATTEMPT
            WHERE UserID = adminID;

        DELETE FROM ADMINISTRATOR
            WHERE UserID = adminID;

        DELETE FROM PASSWORD_CHANGE
            WHERE UserID = adminID;

        DELETE FROM USER
            WHERE UserID = adminID;

        RETURN 0;
    END;;

DROP FUNCTION IF EXISTS getProfilePic;

/*Why is VARCHAR not able to be read into varaible?*/
CREATE FUNCTION getProfilePic(userEmail VARCHAR(50))
RETURNS VARCHAR(100)
READS SQL DATA
    BEGIN
        DECLARE imgPath VARCHAR(100);
        DECLARE user INT;

        SELECT getUserID(userEmail) INTO user;

        SELECT ProfilePicPath INTO imgPath
        FROM USER
        WHERE UserID = user;

        RETURN (SELECT ProfilePicPath
                FROM USER
                WHERE UserID = user);
    END;;

DROP FUNCTION IF EXISTS getOrgLogo;

/*Why is VARCHAR not able to be read into varaible?*/
CREATE FUNCTION getOrgLogo(orgNo INT)
RETURNS VARCHAR(100)
READS SQL DATA
    BEGIN
        DECLARE imgPath VARCHAR(100);

        SELECT LogoPath INTO imgPath
        FROM ORGANIZATION
        WHERE OrgID = orgNo;

        RETURN (SELECT LogoPath
                FROM ORGANIZATION
                WHERE OrgID = orgNo);
    END;;

DROP PROCEDURE IF EXISTS getPointChangeReason;

CREATE PROCEDURE getPointChangeReason (reasonID INT)
    BEGIN
        SELECT NumPoints, ReasonDescription
        FROM POINT_CHANGE_REASON
        WHERE ReasonID = reasonID;
    END;;

DROP PROCEDURE IF EXISTS getPointChangeReasons;

CREATE PROCEDURE getPointChangeReasons (orgNo INT)
    BEGIN
        SELECT ReasonID, ReasonDescription
        FROM POINT_CHANGE_REASON
        WHERE OrgID = orgNo;
    END;;

DROP FUNCTION IF EXISTS addPointChangeReason;

CREATE FUNCTION addPointChangeReason (reason VARCHAR(100), numPoints INT, orgNo INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newReason INT;

        INSERT INTO POINT_CHANGE_REASON (ReasonDescription, NumPoints, OrgID)
            VALUES (reason, numPoints, orgNo);
        
        SELECT ReasonID INTO newReason
        FROM POINT_CHANGE_REASON
        WHERE ReasonID = @@Identity;

        RETURN newReason;
    END;;

DROP PROCEDURE IF EXISTS removePointChangeReason;

CREATE PROCEDURE removePointChangeReason (reason INT)
    BEGIN
        DELETE FROM POINT_CHANGE_REASON
        WHERE ReasonID = reason;
    END;;

DROP PROCEDURE IF EXISTS updatePointChangeReason;

CREATE PROCEDURE updatePointChangeReason (reason INT, newDesc VARCHAR(100), points FLOAT)
    BEGIN
        UPDATE POINT_CHANGE_REASON
            SET
                ReasonDescription = newDesc,
                NumPoints = points
            WHERE ReasonID = reason;
    END;;

DROP PROCEDURE IF EXISTS updatePointConversion;

CREATE PROCEDURE updatePointConversion(orgNo INT, newConversion FLOAT)
    BEGIN
        UPDATE ORGANIZATION
            SET
                PointConversion = newConversion
        WHERE OrgID = orgNo;
    END;;

DROP FUNCTION IF EXISTS getPointConversion;

CREATE FUNCTION getPointConversion(orgNo INT)
RETURNS FLOAT
READS SQL DATA
    BEGIN
        DECLARE pointRate FLOAT;

        SELECT PointConversion INTO pointRate
        FROM ORGANIZATION
        WHERE OrgID = orgNo;

        RETURN PointRate;
    END;;

DELIMITER ;
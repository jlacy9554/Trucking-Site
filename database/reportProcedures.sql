DELIMITER ;;

DROP PROCEDURE IF EXISTS indvDriverPointChangeRep;

CREATE PROCEDURE indvDriverPointChangeRep(startDate DATE, endDate DATE, org INT, driver INT)
    BEGIN
        SELECT Name, Points, ChangeDate, NumPoints, SponsorID, ReasonDescription
        FROM USER, DRIVER, DRIVER_ORGS, POINT_CHANGE, POINT_CHANGE_REASON
        WHERE ChangeDate >= startDate AND ChangeDate <= endDate 
            AND DRIVER_ORGS.OrgID = org AND DRIVER.userID = driver AND
            DRIVER_ORGS.UserID = driver AND
            USER.UserID = DRIVER.UserID AND
            POINT_CHANGE.DriverID = DRIVER.UserID AND
            POINT_CHANGE.ReasonID = POINT_CHANGE_REASON.ReasonID;
    END;;

DROP PROCEDURE IF EXISTS allDriverPointChangeRep;

CREATE PROCEDURE allDriverPointChangeRep(startDate DATE, endDate DATE, org INT)
    BEGIN
        SELECT Name, Points, ChangeDate, NumPoints, SponsorID, ReasonDescription
        FROM USER, DRIVER, DRIVER_ORGS, POINT_CHANGE, POINT_CHANGE_REASON
        WHERE ChangeDate >= startDate AND ChangeDate <= endDate AND 
            USER.UserID = DRIVER.UserID AND
            DRIVER_ORGS.UserID = DRIVER.UserID AND DRIVER_ORGS.OrgID = org AND
            POINT_CHANGE.DriverID = DRIVER.UserID AND
            POINT_CHANGE.ReasonID = POINT_CHANGE_REASON.ReasonID;
    END;;

DROP PROCEDURE IF EXISTS indvSponsorSaleRep;

CREATE PROCEDURE indvSponsorSaleRep(startDate DATE, endDate DATE, detailed BOOLEAN, driver INT, org INT)
    BEGIN
        IF detailed = TRUE THEN
            IF driver = -1 THEN
                SELECT ORGANIZATION.OrgID, ORGANIZATION.Name, DRIVER_ORDER.OrderID, OrderDate, USER.UserID, USER.Name, ProductName, Quantity, Price
                FROM ORGANIZATION, PRODUCT, USER, DRIVER, DRIVER_ORDER, IS_IN_ORDER, BELONGS_TO
                WHERE OrderDate >= startDate AND OrderDate <= endDate AND 
                    ORGANIZATION.OrgID = org AND DRIVER_ORDER.OrgID = org AND
                    USER.UserID = DRIVER.UserID AND
                    BELONGS_TO.DriverID = DRIVER.UserID AND
                    BELONGS_TO.OrderID = IS_IN_ORDER.OrderID AND BELONGS_TO.OrderID = DRIVER_ORDER.OrderID AND
                    IS_IN_ORDER.ProductID = PRODUCT.ProductID;
            ELSE
                SELECT ORGANIZATION.OrgID, ORGANIZATION.Name, DRIVER_ORDER.OrderID, OrderDate, USER.UserID, USER.Name, ProductName, Quantity, Price
                FROM ORGANIZATION, PRODUCT, USER, DRIVER, DRIVER_ORDER, IS_IN_ORDER, BELONGS_TO
                WHERE OrderDate >= startDate AND OrderDate <= endDate AND 
                    ORGANIZATION.OrgID = org AND DRIVER.UserID = driver AND
                    USER.UserID = DRIVER.UserID AND DRIVER_ORDER.OrgID = org AND
                    BELONGS_TO.DriverID = DRIVER.UserID AND
                    BELONGS_TO.OrderID = IS_IN_ORDER.OrderID AND BELONGS_TO.OrderID = DRIVER_ORDER.OrderID AND
                    IS_IN_ORDER.ProductID = PRODUCT.ProductID;
            END IF;
        ELSE
            IF driver = -1 THEN
                SELECT ORGANIZATION.OrgID, ORGANIZATION.Name, DRIVER_ORDER.OrderID, OrderDate, Quantity, Price
                FROM ORGANIZATION, PRODUCT, USER, DRIVER, DRIVER_ORDER, IS_IN_ORDER, BELONGS_TO
                WHERE OrderDate >= startDate AND OrderDate <= endDate AND 
                    ORGANIZATION.OrgID = DRIVER_ORDER.OrgID AND DRIVER_ORDER.OrgID = org AND
                    USER.UserID = DRIVER.UserID AND
                    BELONGS_TO.DriverID = DRIVER.UserID AND
                    BELONGS_TO.OrderID = IS_IN_ORDER.OrderID AND BELONGS_TO.OrderID = DRIVER_ORDER.OrderID AND
                    IS_IN_ORDER.ProductID = PRODUCT.ProductID;
            ELSE
                SELECT ORGANIZATION.OrgID, ORGANIZATION.Name, DRIVER_ORDER.OrderID, OrderDate, Quantity, Price
                FROM ORGANIZATION, PRODUCT, USER, DRIVER, DRIVER_ORDER, IS_IN_ORDER, BELONGS_TO
                WHERE OrderDate >= startDate AND OrderDate <= endDate AND 
                    ORGANIZATION.OrgID = DRIVER_ORDER.OrgID AND DRIVER.UserID = driver AND
                    USER.UserID = DRIVER.UserID AND DRIVER_ORDER.OrgID = org AND
                    BELONGS_TO.DriverID = DRIVER.UserID AND
                    BELONGS_TO.OrderID = IS_IN_ORDER.OrderID AND BELONGS_TO.OrderID = DRIVER_ORDER.OrderID AND
                    IS_IN_ORDER.ProductID = PRODUCT.ProductID;
            END IF;
        END IF;
    END;;

DROP PROCEDURE IF EXISTS allSponsorSaleRep;

CREATE PROCEDURE allSponsorSaleRep(startDate DATE, endDate DATE, detailed BOOLEAN)
    BEGIN
        IF detailed = TRUE THEN
            SELECT ORGANIZATION.OrgID, ORGANIZATION.Name, DRIVER_ORDER.OrderID, OrderDate, USER.UserID, USER.Name, ProductName, Quantity, Price
            FROM ORGANIZATION, PRODUCT, USER, DRIVER, DRIVER_ORDER, IS_IN_ORDER, BELONGS_TO
            WHERE OrderDate >= startDate AND OrderDate <= endDate AND
                    USER.UserID = DRIVER.UserID AND DRIVER_ORDER.OrgID = ORGANIZATION.OrgID AND
                    BELONGS_TO.DriverID = DRIVER.UserID AND
                    BELONGS_TO.OrderID = IS_IN_ORDER.OrderID AND BELONGS_TO.OrderID = DRIVER_ORDER.OrderID AND
                    IS_IN_ORDER.ProductID = PRODUCT.ProductID;
        ELSE
            SELECT ORGANIZATION.OrgID, ORGANIZATION.Name, DRIVER_ORDER.OrderID, OrderDate, USER.UserID, USER.Name, Quantity, Price
            FROM ORGANIZATION, PRODUCT, USER, DRIVER, DRIVER_ORDER, IS_IN_ORDER, BELONGS_TO
            WHERE OrderDate >= startDate AND OrderDate <= endDate  AND
                    USER.UserID = DRIVER.UserID AND DRIVER_ORDER.OrgID = ORGANIZATION.OrgID AND
                    BELONGS_TO.DriverID = DRIVER.UserID AND
                    BELONGS_TO.OrderID = IS_IN_ORDER.OrderID AND BELONGS_TO.OrderID = DRIVER_ORDER.OrderID AND
                    IS_IN_ORDER.ProductID = PRODUCT.ProductID;
        END IF;
    END;;

DROP PROCEDURE IF EXISTS driverSaleRep;

CREATE PROCEDURE driverSaleRep(startDate DATE, endDate DATE, detailed BOOLEAN, driver INT)
    BEGIN
        IF detailed = TRUE THEN
            IF driver = -1 THEN
                SELECT USER.UserID, USER.Name, ORGANIZATION.OrgID, ORGANIZATION.Name, DRIVER_ORDER.OrderID, OrderDate, ProductName, Quantity, Price
                FROM ORGANIZATION, USER, DRIVER, DRIVER_ORGS, DRIVER_ORDER, PRODUCT, IS_IN_ORDER, BELONGS_TO
                WHERE OrderDate >= startDate AND OrderDate <= endDate AND 
                    USER.UserID = DRIVER.UserID AND DRIVER_ORGS.OrgID = ORGANIZATION.OrgID AND DRIVER_ORGS.UserID = DRIVER.UserID AND BELONGS_TO.DriverID = DRIVER.userID AND IS_IN_ORDER.OrderID = BELONGS_TO.OrderID AND DRIVER_ORDER.OrderID = IS_IN_ORDER.OrderID AND DRIVER_ORDER.OrgID = ORGANIZATION.OrgID AND
                    PRODUCT.ProductID = IS_IN_ORDER.ProductID;
            ELSE
                SELECT USER.UserID, USER.Name, ORGANIZATION.OrgID, ORGANIZATION.Name, DRIVER_ORDER.OrderID, OrderDate, ProductName, Quantity, Price
                FROM ORGANIZATION, USER, DRIVER, DRIVER_ORGS, DRIVER_ORDER, PRODUCT, IS_IN_ORDER, BELONGS_TO
                WHERE OrderDate >= startDate AND OrderDate <= endDate AND
                    DRIVER.UserID = driver AND 
                    ORGANIZATION.OrgID = DRIVER_ORGS.OrgID AND USER.UserID = DRIVER.UserID AND DRIVER_ORGS.UserID = DRIVER.UserID AND  
                    BELONGS_TO.DriverID = DRIVER.userID AND IS_IN_ORDER.OrderID = BELONGS_TO.OrderID AND DRIVER_ORDER.OrderID = IS_IN_ORDER.OrderID AND DRIVER_ORDER.OrgID = ORGANIZATION.OrgID AND
                    PRODUCT.ProductID = IS_IN_ORDER.ProductID;
            END IF;
        ELSE
            IF driver = -1 THEN
                SELECT USER.UserID, USER.Name, ORGANIZATION.OrgID, ORGANIZATION.Name, DRIVER_ORDER.OrderID, OrderDate, Quantity, Price
                FROM ORGANIZATION, USER, DRIVER, DRIVER_ORGS, DRIVER_ORDER, PRODUCT, IS_IN_ORDER, BELONGS_TO
                WHERE OrderDate >= startDate AND OrderDate <= endDate AND 
                    USER.UserID = DRIVER.UserID AND DRIVER_ORGS.OrgID = ORGANIZATION.OrgID AND DRIVER_ORGS.UserID = DRIVER.UserID AND DRIVER_ORDER.OrgID = ORGANIZATION.OrgID AND
                    BELONGS_TO.DriverID = DRIVER.userID AND IS_IN_ORDER.OrderID = BELONGS_TO.OrderID AND DRIVER_ORDER.OrderID = IS_IN_ORDER.OrderID AND DRIVER_ORDER.OrgID = ORGANIZATION.OrgID AND
                    PRODUCT.ProductID = IS_IN_ORDER.ProductID;
            ELSE
                SELECT USER.UserID, USER.Name, ORGANIZATION.OrgID, ORGANIZATION.Name, DRIVER_ORDER.OrderID, OrderDate, Quantity, Price
                FROM ORGANIZATION, USER, DRIVER, DRIVER_ORGS, DRIVER_ORDER, PRODUCT, IS_IN_ORDER, BELONGS_TO
                WHERE OrderDate >= startDate AND OrderDate <= endDate AND
                    DRIVER.UserID = driver AND 
                    ORGANIZATION.OrgID = DRIVER_ORGS.OrgID AND USER.UserID = DRIVER.UserID AND DRIVER_ORGS.UserID = DRIVER.UserID AND  
                    BELONGS_TO.DriverID = DRIVER.userID AND IS_IN_ORDER.OrderID = BELONGS_TO.OrderID AND DRIVER_ORDER.OrderID = IS_IN_ORDER.OrderID AND DRIVER_ORDER.OrgID = ORGANIZATION.OrgID AND
                    PRODUCT.ProductID = IS_IN_ORDER.ProductID;
            END IF;
        END IF;
    END;;

DROP PROCEDURE IF EXISTS indvSponsorInvoice;

CREATE PROCEDURE indvSponsorInvoice(startDate DATE, endDate DATE, org INT)
    BEGIN
        SELECT ORGANIZATION.Name, OrderDate, USER.UserID, USER.Name, Price, Quantity
        FROM ORGANIZATION, PRODUCT, USER, DRIVER, DRIVER_ORGS, DRIVER_ORDER, IS_IN_ORDER, BELONGS_TO
        WHERE OrderDate >= startDate AND OrderDate <= endDate AND
            ORGANIZATION.OrgID = org AND DRIVER_ORGS.OrgID = org AND
            DRIVER_ORGS.UserID = DRIVER.UserID AND
            USER.UserID = DRIVER.UserID AND DRIVER_ORDER.OrgID = org AND
            BELONGS_TO.DriverID = DRIVER.UserID AND
            BELONGS_TO.OrderID = IS_IN_ORDER.OrderID AND DRIVER_ORDER.OrderID = BELONGS_TO.OrderID AND
            PRODUCT.ProductID = IS_IN_ORDER.ProductID;
    END;;

DROP PROCEDURE IF EXISTS allSponsorInvoice;

CREATE PROCEDURE allSponsorInvoice(startDate DATE, endDate DATE)
    BEGIN
        SELECT ORGANIZATION.Name, OrderDate, USER.UserID, USER.Name, Price, Quantity
        FROM ORGANIZATION, PRODUCT, USER, DRIVER, DRIVER_ORGS, DRIVER_ORDER, IS_IN_ORDER, BELONGS_TO
        WHERE OrderDate >= startDate AND OrderDate <= endDate AND
            USER.UserID = DRIVER.UserID AND DRIVER_ORGS.UserID = DRIVER.UserID AND DRIVER_ORGS.OrgID = ORGANIZATION.OrgID AND
            BELONGS_TO.DriverID = DRIVER.UserID AND
            BELONGS_TO.OrderID = IS_IN_ORDER.OrderID AND DRIVER_ORDER.OrderID = BELONGS_TO.OrderID AND DRIVER_ORDER.OrgID = ORGANIZATION.OrgID AND
            PRODUCT.ProductID = IS_IN_ORDER.ProductID;
    END;;

DROP PROCEDURE IF EXISTS driverApplicationsRep;

CREATE PROCEDURE driverApplicationsRep(startDate DATE, endDate DATE)
    BEGIN
        SELECT ApplicantDate, OrgID, ApplicantName, IsAccepted, Reason
        FROM APPLICANT
        WHERE ApplicantDate >= startDate AND ApplicantDate <= endDate;
    END;;

DROP PROCEDURE IF EXISTS pointChangeRep;

CREATE PROCEDURE pointChangeRep(startDate DATE, endDate DATE)
    BEGIN
        SELECT USER.Name, ChangeDate, ORGANIZATION.Name, NumPoints, ReasonDescription
        FROM USER, DRIVER, DRIVER_ORGS, ORGANIZATION, POINT_CHANGE, POINT_CHANGE_REASON
        WHERE ChangeDate >= startDate AND ChangeDate <= endDate AND
                USER.UserID = DRIVER.UserID AND DRIVER_ORGS.UserID = DRIVER.UserID AND
                DRIVER_ORGS.OrgID = ORGANIZATION.OrgID AND
                POINT_CHANGE.DriverID = DRIVER.UserID AND
                POINT_CHANGE.ReasonID = POINT_CHANGE_REASON.ReasonID;
    END;;

DROP PROCEDURE IF EXISTS passwordChangeRep;

CREATE PROCEDURE passwordChangeRep(startDate DATE, endDate DATE)
    BEGIN
        SELECT Name, ChangeDate, ChangeType
        FROM USER, PASSWORD_CHANGE
        WHERE ChangeDate >= startDate AND ChangeDate <= endDate AND
                USER.UserID = PASSWORD_CHANGE.UserID;
    END;;

DROP PROCEDURE IF EXISTS loginAttemptsRep;

CREATE PROCEDURE loginAttemptsRep(startDate DATE, endDate DATE)
    BEGIN
        SELECT Email, AttemptDate, Suceeded
        FROM USER, LOGIN_ATTEMPT
        WHERE USER.UserID = LOGIN_ATTEMPT.UserID;
    END;;

DELIMITER ;
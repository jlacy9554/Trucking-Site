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

DROP FUNCTION IF EXISTS checkPassword;

CREATE FUNCTION checkPassword(userEmail VARCHAR(50), userPassword VARCHAR(20))
RETURNS BOOLEAN
READS SQL DATA
    BEGIN
        DECLARE isCorrect BOOLEAN;
        DECLARE hashedPass BINARY(64);
        DECLARE correctPass BINARY(64);

        SELECT HashedPassword INTO correctPass
        FROM USER
        WHERE Email = userEmail;

        SET hashedPass = SHA(userPassword);

        IF hashedPass = correctPass THEN
            SET isCorrect = TRUE;
        ELSE
            SET isCorrect = FALSE;
        END IF;

        RETURN isCorrect;
    END;;

DROP FUNCTION IF EXISTS login;

CREATE FUNCTION login(userEmail VARCHAR(50), userPassword VARCHAR(20))
RETURNS BOOLEAN
READS SQL DATA
    BEGIN
        DECLARE success BOOLEAN;
        DECLARE userID INT;

        SELECT getUserID(userEmail) INTO userID;

        SELECT checkPassword(userEmail, userPassword) INTO success;

        INSERT INTO LOGIN_ATTEMPT (AttemptDate, Suceeded, UserID)
            VALUES (CURDATE(), success, userID);
        
        RETURN success;
    END;;

DROP FUNCTION IF EXISTS updatePassword;

CREATE FUNCTION updatePassword(userEmail VARCHAR(50), newPass VARCHAR(20))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        UPDATE USER
            SET HashedPassword = SHA(newPass)
        WHERE Email = userEmail;

        RETURN 1;
    END;;

DROP FUNCTION IF EXISTS getUserType;

CREATE FUNCTION getUserType(userEmail VARCHAR(50))
RETURNS VARCHAR(20)
READS SQL DATA
    BEGIN
        DECLARE user INT;
        DECLARE isDriver BOOLEAN;
        DECLARE isSponsor BOOLEAN;
        DECLARE isAdmin BOOLEAN;

        SELECT getUserID(userEmail) INTO user;

        SELECT EXISTS(
            SELECT UserID
            FROM DRIVER
            WHERE UserID = user
        ) INTO isDriver;

        SELECT EXISTS(
            SELECT UserID
            FROM SPONSOR
            WHERE UserID = user
        ) INTO isSponsor;

        SELECT EXISTS(
            SELECT UserID
            FROM ADMINISTRATOR
            WHERE UserID = user
        ) INTO isAdmin;

        IF isDriver THEN
            RETURN "Driver";
        ELSEIF isSponsor THEN
            RETURN "Sponsor";
        ELSE
            RETURN "Admin";
        END IF;
    END;;

DELIMITER ;
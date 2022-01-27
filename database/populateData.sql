SELECT createOrg ("Test Organization", 0.10);

SELECT createDriver ("Test Driver", "driver@email.com", "driverPass", "42 Road Way, City, ST, 12345", "555-555-5555", 1);

SELECT createSponsor ("Test Sponsor", "sponsor@email.com", "sponsorPass", 1);

SELECT createAdmin ("Test Admin", "admin@email.com", "adminPass");

INSERT INTO POINT_CHANGE_REASON (ReasonDescription, NumPoints, OrgID)
    VALUES ("Test", 50, 1);

INSERT INTO POINT_CHANGE (ChangeDate, ReasonID, TotalPoints, DriverID, SponsorID)
    VALUES ('2021-03-29', 1, 100, 1, 2);

INSERT INTO POINT_CHANGE (ChangeDate, ReasonID, TotalPoints, DriverID, SponsorID)
    VALUES ('2021-03-05', 1, 50, 1, 2);

INSERT INTO ORG_PAYMENTS (CreditCardNum, CreditCardSec, CreditCardDate, BillingAddress, OrgID)
    VALUES (5555555555555555, 123, '2021-03-01', '1 Test Way, City, ST 12345', 1);
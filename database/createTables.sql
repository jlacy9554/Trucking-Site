ALTER TABLE tablename AUTO_INCREMENT = 1;

CREATE TABLE USER
    (UserID             INT             NOT NULL    AUTO_INCREMENT,
    Name                VARCHAR(100)    NOT NULL,
    Email               VARCHAR(50)     NOT NULL,
    HashedPassword      BINARY(64)      NOT NULL,
    ProfilePicPath      VARCHAR(100)    NOT NULL,
    PRIMARY KEY (UserID));

CREATE TABLE PASSWORD_CHANGE
    (ChangeNo   INT             NOT NULL    AUTO_INCREMENT,
    ChangeDate  DATE            NOT NULL,
    ChangeType  VARCHAR(35)     NOT NULL,
    UserID      INT             NOT NULL,
    PRIMARY KEY (ChangeNo),
    FOREIGN KEY (UserID) REFERENCES USER (UserID));

CREATE TABLE ADMINISTRATOR
    (UserID     INT      NOT NULL,
    PRIMARY KEY (UserID),
    FOREIGN KEY (UserID) REFERENCES USER (UserID));

CREATE TABLE ORG_CATALOG
    (CatalogID      INT     NOT NULL    AUTO_INCREMENT,
    PRIMARY KEY (CatalogID));

CREATE TABLE ORGANIZATION
    (OrgID              INT                 NOT NULL    AUTO_INCREMENT,
    Name                VARCHAR(50)         NOT NULL,
    LogoPath            VARCHAR(100),
    PointConversion     FLOAT               NOT NULL,
    CatalogID           INT                 NOT NULL,
    PRIMARY KEY (OrgID),
    FOREIGN KEY (CatalogID) REFERENCES ORG_CATALOG (CatalogID));

CREATE TABLE CATALOG_KEYWORDS
    (WordID     INT             NOT NULL    AUTO_INCREMENT,
    CatalogID   INT             NOT NULL,
    Keyword     VARCHAR(20)     NOT NULL,
    PRIMARY KEY (WordID),
    FOREIGN KEY (CatalogID) REFERENCES ORGANIZATION (CatalogID));

CREATE TABLE ORG_PAYMENTS
    (PayID          INT             NOT NULL    AUTO_INCREMENT,
    BillingName     VARCHAR(50)     NOT NULL,
    CreditCardNum   BINARY(64)      NOT NULL,
    LastDigits      CHAR(4)         NOT NULL,
    CreditCardSec   BINARY(64)      NOT NULL,
    CreditCardDate  DATE            NOT NULL,
    BillingAddress  VARCHAR(100)    NOT NULL,
    OrgID           INT             NOT NULL,
    PRIMARY KEY (PayID),
    FOREIGN KEY (OrgID) REFERENCES ORGANIZATION (OrgID));

CREATE TABLE SPONSOR
    (UserID         INT             NOT NULL,
    OrgID           INT             NOT NULL,
    PRIMARY KEY (UserID),
    FOREIGN KEY (UserID) REFERENCES USER (UserID),
    FOREIGN KEY (OrgID) REFERENCES ORGANIZATION (OrgID));

CREATE TABLE DRIVER
    (UserID     INT         NOT NULL,
    PhoneNo     CHAR(12),
    PRIMARY KEY (UserID),
    FOREIGN KEY (UserID) REFERENCES USER (UserID));

CREATE TABLE DRIVER_ORGS
    (UserID     INT     NOT NULL,
    OrgID       INT     NOT NULL,
    Points      FLOAT   NOT NULL,
    PRIMARY KEY (UserID, OrgID),
    FOREIGN KEY (UserID) REFERENCES DRIVER (UserID),
    FOREIGN KEY (OrgID) REFERENCES ORGANIZATION (OrgID));

CREATE TABLE DRIVER_ADDRESSES
    (AddressID      INT             NOT NULL    AUTO_INCREMENT,
    DriverID        INT             NOT NULL,
    Address         VARCHAR(100)    NOT NULL,
    DefaultAddr     BOOL        NOT NULL,
    PRIMARY KEY (AddressID),
    FOREIGN KEY (DriverID) REFERENCES DRIVER (UserID));

CREATE TABLE LOGIN_ATTEMPT
    (AttemptNo      INT     NOT NULL    AUTO_INCREMENT,
    AttemptDate     DATE    NOT NULL,
    Suceeded        BOOL    NOT NULL,
    UserID          INT     NOT NULL,
    PRIMARY KEY (AttemptNo),
    FOREIGN KEY (UserID) REFERENCES USER (UserID));

CREATE TABLE POINT_CHANGE_REASON
    (ReasonID           INT             NOT NULL    AUTO_INCREMENT,
    ReasonDescription   VARCHAR(100)    NOT NULL,
    NumPoints           FLOAT           NOT NULL,
    OrgID               INT             NOT NULL,
    PRIMARY KEY (ReasonID),
    FOREIGN KEY (OrgID) REFERENCES ORGANIZATION (OrgID));

CREATE TABLE POINT_CHANGE
    (ChangeID       INT     NOT NULL    AUTO_INCREMENT,
    ChangeDate      DATE    NOT NULL,
    ReasonID        INT     NOT NULL,
    TotalPoints     FLOAT   NOT NULL,
    DriverID        INT     NOT NULL,
    SponsorID       INT     NOT NULL,
    PRIMARY KEY (ChangeID),
    FOREIGN KEY (ReasonID) REFERENCES POINT_CHANGE_REASON (ReasonID),
    FOREIGN KEY (DriverID) REFERENCES DRIVER (UserID),
    FOREIGN KEY (SponsorID) REFERENCES SPONSOR (USERID));

CREATE TABLE PRODUCT
    (ProductID      CHAR(12)            NOT NULL,
    ProductName     VARCHAR(100)        NOT NULL,
    Price           FLOAT               NOT NULL,
    ImgUrl          VARCHAR(200)        NOT NULL,
    PRIMARY KEY (ProductID));

CREATE TABLE IS_IN_CATALOG
    (CatalogID      INT          NOT NULL,
    ProductID       CHAR(12)     NOT NULL,
    PRIMARY KEY (CatalogID, ProductID),
    FOREIGN KEY (CatalogID) REFERENCES ORG_CATALOG (CatalogID),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID));

CREATE TABLE DRIVER_ORDER
    (OrderID      INT           NOT NULL    AUTO_INCREMENT,
    OrderDate     DATE          NOT NULL,
    Status        VARCHAR(50)   NOT NULL,
    OrgID         INT           NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrgID) REFERENCES ORGANIZATION (OrgID));

CREATE TABLE IS_IN_ORDER
    (OrderID        INT         NOT NULL,
    ProductID       CHAR(12)    NOT NULL,
    Quantity        INT         NOT NULL,
    PRIMARY KEY (OrderID, ProductID),
    FOREIGN KEY (OrderID) REFERENCES DRIVER_ORDER (OrderID),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID));

CREATE TABLE BELONGS_TO
    (DriverID     INT     NOT NULL,
    OrderID       INT     NOT NULL,
    PRIMARY KEY (DriverID, OrderID),
    FOREIGN KEY (DriverID) REFERENCES DRIVER (UserID),
    FOREIGN KEY (OrderID) REFERENCES DRIVER_ORDER (OrderID));

CREATE TABLE WISHLIST
    (ListID       INT     NOT NULL    AUTO_INCREMENT,
    DriverID      INT     NOT NULL,
    OrgID         INT     NOT NULL,
    PRIMARY KEY (ListID),
    FOREIGN KEY (DriverID) REFERENCES DRIVER (UserID),
    FOREIGN KEY (OrgID) REFERENCES ORGANIZATION (OrgID));

CREATE TABLE IS_IN_WISHLIST
    (ProductID      CHAR(12)     NOT NULL,
    ListID          INT         NOT NULL,
    PRIMARY KEY (ProductID, ListID),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID),
    FOREIGN KEY (ListID) REFERENCES WISHLIST (ListID));

CREATE TABLE APPLICANT
    (ApplicantID    INT             NOT NULL    AUTO_INCREMENT,
    ApplicantDate   DATE            NOT NULL,
    IsAccepted      BOOL            NOT NULL,
    Reason          VARCHAR(150)    NOT NULL,
    ApplicantName   VARCHAR(100)    NOT NULL,
    Email           VARCHAR(50)     NOT NULL,
    PhoneNo         CHAR(12)        NOT NULL,
    HomeAddress     VARCHAR(100)    NOT NULL,
    OrgID           INT             NOT NULL,
    PRIMARY KEY (ApplicantID),
    FOREIGN KEY (OrgID) REFERENCES ORGANIZATION (OrgID));
"""truckersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from Catalog.views import sponsor_catalog
from Catalog.views import product_list
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from truckersite import views, forms

from userProfile import views as profileViews
from userProfile import models as profileOps

from reports import views as reportViews
from reports import models as reportOps

from sponsor import views as sponsorViews
from sponsor import models as sponsorOps

from dashboard import views as dashViews
from dashboard import models as dashOps

from orgPage import views as orgViews
from orgPage import models as orgOps

from Catalog import views as catalogViews
from Catalog import models as catalogOps

from django.conf.urls.static import static
from django.conf import settings

handler404 = 'truckersite.views.page_not_found_view'
handler500 = 'truckersite.views.error_view'
handler403 = 'truckersite.views.permission_denied_view'
handler400 = 'truckersite.views.bad_request_view'

urlpatterns = [
    path('',forms.login), 
    path('loginScreen/', forms.login, name = 'loginScreen'),
    path('login', forms.loginpg, name = 'login'),
    path('changepass',forms.changepass, name='changepass'),

    path('application/', views.application, name = 'application'),
    path('reg',views.userreggin, name = 'reg'),

    #Driver profile forms
    path('getNewDriverEmail', profileOps.getNewDriverEmail, name = "getNewDriverEmail"),
    path('getNewDriverPass', profileOps.getNewDriverPassword, name = 'getNewDriverPass'),
    path('getNewDriverPhone', profileOps.getNewDriverPhone, name = 'getNewDriverPhone'),
    path('getNewDriverAddress', profileOps.getNewDriverAddress, name = 'getNewDriverAddress'),
    path('getDriverDefaultAddr', profileOps.getDriverDefaultAddr, name = 'getDriverDefaultAddr'),
    path('getNewDriverProfilePic', profileOps.getDriverProfilePic, name = 'getNewDriverProfilePic'),
    path('driverProfile', profileViews.driverProfile, name = "driverProfile"),
    path('driver_point_history', profileViews.driverPointHistory, name = "driverPointHistory"),

    #Sponsor profile forms
    path('getNewSponsorProfilePic', profileOps.getSponsorProfilePic, name = 'getNewSponsorProfilePic'),
    path('getNewSponsorEmail', profileOps.getNewSponsorEmail, name = 'getNewSponsorEmail'),
    path('getNewDriverPass', profileOps.getNewSponsorPassword, name = 'getNewDriverPass'),
    path('sponsorProfile/', profileViews.sponsorProfile, name = 'sponsorProfile'),

    #Admin profile forms
    path('getNewAdminProfilePic', profileOps.getAdminProfilePic, name = 'getNewAdminProfilePic'),
    path('getNewAdminEmail', profileOps.getNewAdminEmail, name = 'getNewAdminEmail'),
    path('getNewAdminPass', profileOps. getNewAdminPassword, name = 'getNewAdminPass'),
    path('adminProfile/', profileViews.adminProfile, name = 'adminProfile'),

    #Organization page
    path('orgPage/', orgViews.organizationPage, name = 'orgPage'),
    path('getNewOrgLogo', orgOps.getNewLogo, name = "getNewOrgLogo"),
    path('getNewPointChange', orgOps.getNewPointChange, name = 'getNewPointChange'),
    path('updatePointConversion', orgOps.updatePointConversion, name = 'updatePointConversion'),
    path('updatePaymentInfo', orgOps.updatePaymentInfo, name = 'updatePaymentInfo'),
    path('addNewSponsor', orgOps.addNewSponsor, name = 'addNewSponsor'),
    path('editReason', orgOps.editReason, name = 'editReason'),
    path('editSponsor', orgOps.editSponsor, name = "editSponsor"),
    path('editDriver', orgOps.editDriver, name = 'editDriver'),
    path('adminOrgs/', orgViews.adminOrgs, name = 'adminOrgs'),
    path('getAdminOrgChoice', orgOps.getAdminOrgChoice, name = 'getAdminOrgChoice'),
    path('getNewCatalogKeyword', orgOps.getNewCatalogKeyword, name = "getNewCatalogKeyword"),
    path('removeCatalogKeyword/<int:wordID>/', orgOps.removeCatalogKeyword, name = 'removeCatalogKeyword'),
    path('createCatalog', orgOps.createCatalog, name = 'createCatalog'),

    #Edit existsing users
    path('adminEditUserPage/<int:userID>', orgViews.adminEditUser, name = 'adminEditUserPage'),
    path('adminEditUser/<int:userID>', orgOps.adminEditUser, name = 'adminEditUser'),
    path('sponsorEditUser/<int:userID>', orgOps.sponsorEditUser, name = 'sponsorEditUser'),

    path('adminEditReason/<int:reasonID>', orgOps.adminUpdateReason, name = 'adminEditReason'),
    path('sponsorEditReason/<int:reasonID>', orgOps.sponsorUpdateReason, name = 'sponsorEditReason'),


    #Sponsor report generation
    path('sponsorReportGeneration/', reportViews.sponsorGenerateReport, name = 'sponsorReportGeneration'),
    path('getSponsorReport', reportOps.getSponsorReport, name = 'getSponsorReport'),

    #Admin report generation
    path('adminReportGeneration/', reportViews.adminGenerateReport, name = 'adminReportGeneration'),
    path('auditLog/', reportViews.auditLog, name = 'auditLog'),
    path('invoice/', reportViews.invoice, name = 'invoice'),
    path('driverSales/', reportViews.driverSales, name = 'driverSales'),
    path('sponsorSales/', reportViews.sponsorSales, name = 'sponsorSales'),
    path('getAuditLog', reportOps.getAuditLog, name = 'getAuditLog'),
    path('getInvoice', reportOps.getInvoice, name = 'getInvoice'),
    path('getDriverSales', reportOps.getDriverSales, name = 'getDriverSales'),
    path('getSponsorSales', reportOps.getSponsorSales, name = 'getSponsorSales'),
    path('updateDriverList', reportOps.updateDriverList, name = 'updateDriverList'),

    #Catalog
    path('driverCatalog/', catalogViews.product_list, name = 'driverCatalog'),
    path('wishlist/', catalogViews.wishlist, name = 'wishlist'),
    path('driverOrderHistory/', catalogViews.driverOrderHistory, name = 'driverOrderHistory'),
    path('sponsorCatalog', catalogViews.sponsor_catalog, name = 'sponsorCatalog'),
    path('sponsorCart', catalogViews.sponsorCart, name = 'sponsorCart'),
    path('productPage/<str:id>/', catalogViews.productPage, name = 'productPage'),
    path('driverCart', catalogViews.driverCart, name = 'driverCart'),
    path('checkout', catalogViews.checkout, name = 'checkout'),
    path('addProducts', catalogViews.addProducts, name = 'addProducts'),
    path('admin/', admin.site.urls),
    path('addToCart/<str:id>/', catalogViews.add_to_cart, name = 'addToCart'),
    path('removeFromCart/<str:id>/', catalogViews.remove_from_cart, name = 'removeFromCart'),
    path('addToWishlist/<str:id>/', catalogViews.addToWishlist, name = 'addToWishlist'),
    path('removeFromWishlist/<str:id>/', catalogViews.removeFromWishlist, name = 'removeFromWishlist'),
    path('complete_order/', catalogViews.complete_order, name = 'complete_order'),
    path('cancel_order/', catalogViews.cancel_order, name = 'cancel_order'),

    #Sponsor
    path('sponsor_dash/', sponsorViews.sponsorDashDisplay, name = 'sponsorDashDisplay'),
    path('application/<int:applicant_id>', sponsorViews.sponsorViewApplicant, name = 'sponsorViewApplicant'),
    path('accept_applicant/<int:applicant_id>', sponsorViews.sponsorAcceptApplicant, name = 'sponsorAcceptApplicant'),
    path('reject_applicant/<int:applicant_id>', sponsorViews.sponsorRejectApplicant, name = 'sponsorRejectApplicant'),
    path('sponsor_view_drivers/', sponsorViews.sponsorViewDrivers, name = 'sponsorViewDrivers'),
    path('change_driver_points/<int:driver_id>', sponsorViews.sponsorChangePoints, name = 'sponsorChangePoints'),
    path('sponsor_application_list/', sponsorViews.sponsorApplicationList, name = 'sponsorApplicationList'),

    #Dashboards
    path("driverDash/", dashViews.driverDash, name = 'driverDash'),
    path('adminDash/', dashViews.adminDash, name = 'adminDash'),
    path("editAdmin", dashOps.editAdmin, name = 'editAdmin'),
    path('addAdmin', dashOps.addNewAdmin, name = 'addAdmin'),
    path('setDriverOrg/<int:orgID>', dashOps.setDriverOrg, name = 'setDriverOrg'),
    path('addOrg', dashOps.addOrg, name = 'addOrg'),
    path('removeOrg', dashOps.removeOrg, name = 'removeOrg'),

    #View as
    path('sponSetDriverView', sponsorOps.setDriverView, name = 'sponSetDriverView'),
    path('setOrigSponsorView', sponsorOps.setOriginalView, name = 'setOrigSponsorView'),
    path('adminSetDriverView', dashOps.setDriverView, name = 'adminSetDriverView'),
    path('adminSetSponsorView', dashOps.setSponsorView, name = 'adminSetSponsorView'),
    path('revertDriverView', dashOps.revertDriverView, name = 'revertDriverView'),
    path('revertSponsorView', dashOps.revertSponsorView, name = 'revertSponsorView'),

    #Logout
    path('logout', forms.logoutpg, name = 'logout'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path, include
from .views import *
from . import views
# from .notification import notifications_view
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register('notifications', views.NotificationViewSet, basename='notification')
 
urlpatterns = [
    # path("notifications/", notifications_view, name="notifications"),
    path('api/contact/', ContactInfoView.as_view(), name='contact_api'),
    path('api/packages/', PackageView.as_view(), name='package_api'),
   #  path('api/chats/', ChatView.as_view(), name='chat_api'),
    path('api/tickets/',TicketView.as_view(), name='ticket_api'),
    path('api/tickets/<int:ticket_id>/', TicketView.as_view(), name='ticket-detail'), 
    path('api/newlabels/', newLabelView.as_view(), name='newlabel-api'),
    path('api/newlabels/<int:pk>/', newLabelView.as_view(), name='label-detail'),
    path('api/top-states/', TopStatesView.as_view(), name='top-states'),
   path('api/order/',OrderView.as_view() , name='order_api'),
   path('api/payments/',PaymentView.as_view() , name='Payment_api'),
   path('api/addfunds/',AddFundView.as_view() , name=' AddFunds_api'),
  
   path('api/addresses/', AddressView.as_view(), name='address_api'),
   path('api/addresses/<int:pk>/', AddressView.as_view(), name='address-detail'),
# path('api/create-order/', views.create_order_from_new_label, name='create_order'),
  path('api/tickets/<int:ticket_id>/close/', views.close_ticket, name='close_ticket'),

   path('api/ship-address/', ShipFromAddressView.as_view(), name='ship-address'),
   path('api/profile/', ProfileView.as_view(), name='profile_api'),
   path('api/coupons/', CouponView.as_view(), name='coupons_api'),
   path('api/delete-account/', DeleteAccountView.as_view(), name='delete_account_api'),
     path("create-notification/", create_notification, name="create_notification"),
   path("referrals/", views.referrals_view, name="referrals"),
  
   path('api/', include(router.urls)),
   path('user_dashboard/', views.dashboard,name='dashboard'),
   path('orders/', views.orders,name='orders'),
   path('create_order/', views.create_order,name='create_order'),
   path('orders_admin/', views.orders_admin,name='orders_admin'),
    path('order/<int:order_id>/pdf/', generate_pdf, name='generate_pdf'),
   path('order/<int:order_id>/receipt/', views.view_receipt, name='view_receipt'),
   path('view_receipt_admin/<int:order_id>/', views.view_receipt_admin, name='view_receipt_admin'),
  path('upload-csv/', views.handle_uploaded_file, name='upload_csv'),
   path('address/',views.address,name='address'),
   path('payments/',views.payment,name='payments'),
   path('referrals/',views.referral,name='referrals'),
   path('packages/',views.package,name='packages'),
   path('create_package',views.create_package,name='create_package'),
   path('settings/',views.setting,name='settings'),
    path('update_profile/', views.update_profile, name='update_profile'),
   path('stores/',views.store,name='stores'),
  
   # path('view_support/<int:id>/',views.view_support,name='view_support'),
   #  path('submit_view_supports/',views.submit_view_supports,name='submit_view_supports'),
   path('view_tickets_user/<int:id>/',views.view_tickets_user,name='view_tickets_user'),
   path('submit_view_tickets_user/',views.submit_view_tickets_user,name='submit_view_tickets_user'),
  path('api/stores/<int:pk>/', StoreView.as_view(), name='store-detail'),
  path('api/stores/', StoreView.as_view(), name='store_api'),
   path('supports/',views.supports,name='supports'),
   path('addfund/',views.addFund,name='addfund'),
   path('newLable/',views.newLable,name='newLable'),
   path('contact',views.contact,name="conatct us"),
   path('delete-account/', views.delete_account, name='delete_account'),
   path('navbar.html', views.load_navbar, name='load_navbar'),
    path('sidebar.html', views.load_sidebar, name='load_sidebar'),
     path('calculate_package_price/', calculate_package_price, name='calculate_package_price'),
]


 
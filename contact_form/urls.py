from django.urls import path, include
from .views import *
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('api/contact/', ContactInfoView.as_view(), name='contact_api'),
    path('api/packages/', PackageView.as_view(), name='package_api'),
    path('api/chats/', ChatView.as_view(), name='chat_api'),
    path('api/tickets/',TicketView.as_view(), name='ticket_api'),
    path('api/tickets/<int:ticket_id>/', TicketView.as_view(), name='ticket-detail'), 
    path('api/order/',OrderView.as_view() , name='order_api'),
    path('api/newlabels/', newLabelView.as_view(), name='newlabel-api'),
    path('api/newlabels/<int:pk>/', newLabelView.as_view(), name='label-detail'),
    path('api/top-states/', TopStatesView.as_view(), name='top-states'),
   path('api/order/',OrderView.as_view() , name='order_api'),
   path('api/payments/',PaymentView.as_view() , name='Payment_api'),
   path('api/addfunds/',AddFundView.as_view() , name=' AddFunds_api'),
   path('api/stores/', StoreView.as_view(), name='store_api'),
   path('api/addresses/', AddressView.as_view(), name='address_api'),
   path('api/addresses/<int:pk>/', AddressView.as_view(), name='address-detail'),
# path('api/create-order/', views.create_order_from_new_label, name='create_order'),
  path('api/tickets/<int:ticket_id>/close/', views.close_ticket, name='close_ticket'),

   path('api/ship-address/', ShipFromAddressView.as_view(), name='ship-address'),
   path('api/profile/', ProfileView.as_view(), name='profile_api'),
   path('api/coupons/', CouponView.as_view(), name='coupons_api'),
   path('api/delete-account/', DeleteAccountView.as_view(), name='delete_account_api'),
   path('api/referrals/', ReferralView.as_view(), name='referral-list'),
   path('api/notifications/', Notificationview.as_view(), name='notification-api'),
   path('api/notifications/<int:pk>/', Notificationview.as_view(), name='notification-details'),
   path('api/', include(router.urls)),
   path('user_dashboard/', views.dashboard,name='dashboard'),
   path('orders/', views.order,name='orders'),
   path('address/',views.address,name='address'),
   path('payments/',views.payment,name='payments'),
   path('referrals/',views.referral,name='referrals'),
   path('packages/',views.package,name='packages'),
   path('settings/',views.setting,name='settings'),
   #  path('view_profile/<int:id>/', views.view_profile, name='view_profile'),  
    path('update_profile/', views.update_profile, name='update_profile'),
   path('stores/',views.store,name='stores'),
   path('api/stores/<int:pk>/', StoreView.as_view(), name='store-detail'),
   # path('view_support/<int:id>/',views.view_support,name='view_support'),
   #  path('submit_view_supports/',views.submit_view_supports,name='submit_view_supports'),
   path('view_tickets_user/<int:id>/',views.view_tickets_user,name='view_tickets_user'),
   path('submit_view_tickets_user/',views.submit_view_tickets_user,name='submit_view_tickets_user'),

   path('supports/',views.supports,name='supports'),
   path('addfund/',views.addFund,name='addfund'),
   path('newLable/',views.newLable,name='newLable'),
   path('contact',views.contact,name="conatct us"),
   path('delete-account/', views.delete_account, name='delete_account'),
   #  path('stores', views.stores, name='stores'),
   #  path('store/create/', views.create_store, name='create_store'),
   #  path('store/<int:pk>/update/', views.update_store, name='update_store'),
   #  path('store/<int:pk>/delete/', views.delete_store, name='delete_store'),
]



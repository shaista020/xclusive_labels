from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('api/signup/', signupView.as_view(), name='signup-api'),
    path('api/signin/', signinView.as_view(), name='signin-api'),
    path('api/batch/', BatchView.as_view(), name='batch-api'),
    path('api/batch/<int:pk>/', BatchView.as_view(),name='batch-detail'),
    path('api/cron/', CronsView.as_view(), name='cron-api'),
    path('api/cron/<int:pk>/', CronsView.as_view(), name='cron-detail'), 
    path('api/type/', TypeView.as_view(), name='type-api'),
    path('api/type/<int:pk>/', TypeView.as_view(), name='type-detail'),
    path('api/pay/', PaymentView.as_view(), name='payments-api'),
    path('api/pay/<int:pk>/', PaymentView.as_view(), name='payment-detail'), 
    path('api/labels/', LabelView.as_view(), name='label-api'),



    path('api/refunds/', RefundView.as_view(), name='refunds-api'),
    path('api/refunds/<int:pk>/', RefundView.as_view(), name='refund-detail'),
    path('api/payment-config/',payment_config_View.as_view(), name='payment-config-api'),
    path('api/email-config/', email_config_View.as_view(), name='email-config-api'),
    path('api/label-api-config/',label_api_config_view.as_view(), name='label-api-config-api'),



    path('api/tic/', Ticketview.as_view(), name='ticket-api'),
    path('api/user/', Userview.as_view(), name='user-api'),
    path('api/user/<int:pk>/', Userview.as_view(), name='user-detail'),
    path('api/weight/', Weightview.as_view(), name='weight-api'),
    path('api/weight/<int:pk>/', Weightview.as_view(), name='weight-detail'),
    path('api/notification/', Notificationview.as_view(), name='notification-api'),
    path('api/notification/<int:pk>/', Notificationview.as_view(), name='notification-update'),


    path('dashboard/', views.dashboard,name='dashboard'),
    path('', views.home,name='home'), 
    path('batch/', views.batch,name='batchs'),
    path('crons/',views.cron,name='crons'),
    path('pay/',views.pay,name='payments'),
    path('refunds/',views.refund,name='refunds'),
    path('tickets/',views.ticket,name='tickets'),
    path('view_tickets/<int:id>/',views.view_ticket,name='view_tickets'),
    path('submit_view_tickets/',views.submit_view_tickets,name='submit_view_tickets'),
    
    path('set/',views.setting,name='settings'),
    path('types/',views.type,name='types'),
    path('users/',views.user,name='users'),
     path('get-user-details/', views.get_user_details, name='get_user_details'),
    path('weights/',views.weight,name='weights'),
    path('new/',views.newlable,name='newlable'),
    path('addFunds/',views.addFunds,name='addFunds'),
]

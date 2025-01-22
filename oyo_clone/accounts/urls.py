from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('login-vendor/', views.login_vendor_page, name='login_vendor_page'),
    path('register-vendor/', views.register_vendor_page, name='register_vendor_page'),
    path('send_otp/<email>', views.send_otp, name='send_otp'),
    path('verify-otp/<email>/', views.verify_otp, name='verify_otp'),
    path('verify-account/<token>/', views.verify_email_token, name='verify_email_token'),
    path('verify-account/<token>/<user_type>/', views.verify_email_token, name='verify_email_token'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-hotel/', views.add_hotel, name='add_hotel'),
    path('edit-hotel/<slug>/', views.edit_hotel, name='edit_hotel'),
    path('<slug>/upload-images/', views.upload_images, name='upload_images'),
    path('delete-images/<id>/', views.delete_images, name='delete_images'),
    path('logout_view/', views.logout_view, name='logout_view')
]



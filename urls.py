from django.urls import path
from Studentapp import views

urlpatterns=[
    path('home_page/',views.home_page,name="home_page"),
    path('room_page/',views.room_page,name="room_page"),
    path('mess_page/',views.mess_page,name="mess_page"),
    path('gallery_page/',views.gallery_page,name="gallery_page"),
    path('student_complaint/',views.student_complaint,name="student_complaint"),
    path('save_complaint/',views.save_complaint,name="save_complaint"),
    path("complaint_success/", views.student_complaint_success, name="student_complaint_success"),

    path('student_profile/', views.student_profile, name="student_profile"),
    path('edit_profile/<int:sid>/', views.edit_student_profile, name='edit_student_profile'),
    path('update_profile/<int:sid>/', views.update_student_profile, name='update_student_profile'),
    path('login/', views.student_login_page, name='student_login_page'),
    path('student_login/', views.student_login, name='student_login'),
    path('payment_success/', views.payment_success, name="payment_success"),
    path('student_payments/', views.student_payments, name="student_payments"),


]
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as app_views

from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("dashboard")

urlpatterns = [

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('accounts/logout/', logout_view, name="logout"),


    path('',  app_views.RequestCreateView.as_view() , name="request_create"),

    path('dashboard/',  app_views.DashboardView.as_view() , name="dashboard"),

    path('request/<pk>/',  app_views.RequestDetailView.as_view() , name="request_detail"),

    path('approval-1/',  app_views.ApprovalOneListView.as_view() , name="request_list_a1"),
    path('approval-2/',  app_views.ApprovalTwoListView.as_view() , name="request_list_a2"),
    path('request-list/',  app_views.RequestListView.as_view() , name="request_list"),

    path('approve-1/<pk>',  app_views.approval_one , name="approve_one"),
    path('approve-2/<pk>',  app_views.approval_two , name="approve_two"),
    
    path('get-report/<pk>',  app_views.generate_pdf , name="get_report"),



    
    path('reject/',  app_views.RequestCreateView.as_view() , name="reject_content"),

    path('sgid-populate/',  app_views.PopulateSGID.as_view() , name="populate_sgid"),
    path('dept-populate/',  app_views.PopulateIDW.as_view() , name="populate_idw"),

]



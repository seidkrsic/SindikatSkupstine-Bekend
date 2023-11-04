
from django.urls import path 
from . import views 
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [ 
    path("routes/", views.getRoutes), 
    path('news/', views.getNews),
    path('filteredNews/', views.getFilteredNews),
    path('news/<str:pk>/', views.getSingleNews),
    path('slides/', views.getNewsForSlides),
    path("categorySessions/", views.getSessions),
    path('sessions/', views.getSessions),
    path('sessions/<str:pk>/', views.getSession),
    path('importantDocuments/<str:pk>/download/', views.download_important_document),
    path('important/', views.importantDocuments),
    path('documents/', views.get_important_documents),
    path("companies/", views.getCompany),
    path("allDocuments/", views.get_all_documents),


    path('boardMembers/', views.get_board_members),
    path('getPresidents/', views.get_presidents), 
    path('getBoardMembers/', views.get_board_members), 
    path('getCommission/', views.get_commission),
    path('getProfile/<str:pk>/', views.get_profile), 
    path('paginationNews/', views.get_paginated_news),
    path("getPresident/", views.get_president), 
    path("getVicePresident/", views.get_vice_president), 
    path("getMainBoardMembers/", views.get_main_board_members), 


    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] 


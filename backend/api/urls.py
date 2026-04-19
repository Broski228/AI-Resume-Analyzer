from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Auth — CBV
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', views.MeView.as_view(), name='me'),

    # Резюме — полный CRUD (CBV через generics)
    path('resumes/', views.MyResumesView.as_view(), name='my_resumes'),
    path('resumes/<int:pk>/', views.ResumeDetailView.as_view(), name='resume_detail'),

    # Поиск для работодателя — CBV
    path('search/', views.ResumeSearchView.as_view(), name='resume_search'),

    # Избранное — CBV
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
    path('favorites/toggle/<int:resume_id>/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),

    # Уведомления — CBV + FBV
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/read/', views.mark_notifications_read, name='notifications_read'),      # FBV #1
    path('notifications/unread-count/', views.unread_count, name='unread_count'),              # FBV #2

    # Профиль — FBV
    path('auth/change-password/', views.change_password, name='change_password'),              # FBV #3
    path('resumes/stats/', views.resume_stats, name='resume_stats'),                           # FBV #4
]

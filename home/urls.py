from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ContactViewSet, Search, UserRegistration, MarkUserAsSpam
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', Search.as_view(), name='search'),
    # path('search/', SearchByPhoneNumber.as_view(), name='search_by_phone_number'),
    # path('search_by_name/', SearchByName.as_view(), name='search_by_name'),

    path('register/', UserRegistration.as_view(), name='register'),
    # path('login/', UserLogin.as_view(), name='login'),

    path('spam/', MarkUserAsSpam.as_view(), name='mark_user_as_spam'),

    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    
]

from django.urls import path
from .views import RegisterAPI, CollectionsView
from .views import SingleCollectionView, MovieApiResponse
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('movies/', MovieApiResponse.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('register/refresh/', TokenRefreshView.as_view()),
    path('collection/', CollectionsView.as_view()),
    path('collection/<uuid:uuid>/', SingleCollectionView.as_view()),
]

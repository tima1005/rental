from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet, CityListAPIView, CityDetailAPIView,
    PropertyListAPIView, PropertyDetailAPIView,
    PropertyImageListAPIView, PropertyImageDetailAPIView,
    BookingListAPIView, BookingDetailAPIView,
    ReviewListAPIView, ReviewDetailAPIView,
    AmenityListAPIView, AmenityDetailAPIView,
    RegisterView, CustomLoginView, LogoutView,
    api_root
)

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', api_root, name='api-root'),  # /api/ чакырганда root view
    path('', include(router.urls)),       # роуттор
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('property/', PropertyListAPIView.as_view(), name='property-list'),
    path('property/<int:pk>/', PropertyDetailAPIView.as_view(), name='property-detail'),
    path('booking/', BookingListAPIView.as_view(), name='booking-list'),
    path('booking/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path('review/', ReviewListAPIView.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
    path('amenity/', AmenityListAPIView.as_view(), name='amenity-list'),
    path('amenity/<int:pk>/', AmenityDetailAPIView.as_view(), name='amenity-detail'),
    path('city/', CityListAPIView.as_view(), name='city-list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(), name='city-detail'),
    path('property_image/', PropertyImageListAPIView.as_view(), name='property_image-list'),
    path('property_image/<int:pk>/', PropertyImageDetailAPIView.as_view(), name='property_image-detail'),
]

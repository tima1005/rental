from tokenize import TokenError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView

from .filter import PropertyFilter
from .pagination import PropertySetPagination
from rest_framework import viewsets, generics, status
from .permissions import CreateProperty
from .models import (User, City, Property, PropertyImage, Booking, Review, Amenity)
from .serializers import (UserSerializer, CityListSerializer, CityDetailSerializer, PropertyListSerializer,
                          PropertyDetailSerializer, PropertySerializer, PropertyImageListSerializer, PropertyImageDetailSerializer,
                          BookingListSerializer, BookingDetailSerializer, ReviewListSerializer, UserProfileSerializer,
                          ReviewDetailSerializer, AmenityListSerializer, AmenityDetailSerializer, LoginSerializer)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'properties': reverse('property-list', request=request, format=format),
        'bookings': reverse('booking-list', request=request, format=format),
        'reviews': reverse('review-list', request=request, format=format),
        'amenities': reverse('amenity-list', request=request, format=format),
        'cities': reverse('city-list', request=request, format=format),
        'property_images': reverse('property_image-list', request=request, format=format),
    })


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh токен не предоставлен.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'detail': 'Недействительный токен.'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer

class CityDetailAPIView(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer

class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['city', 'property_type', 'max_guests', 'price_per_night']
    ordering_fields = ['price_per_night', 'stars']
    pagination_class = PropertySetPagination


class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer

class PropertyCreateAPIView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [CreateProperty]

class PropertyImageListAPIView(generics.ListAPIView):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageListSerializer

class PropertyImageDetailAPIView(generics.RetrieveAPIView):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageDetailSerializer

class BookingListAPIView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer

class BookingDetailAPIView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer

class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer

class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer


class AmenityListAPIView(generics.ListAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenityListSerializer

class AmenityDetailAPIView(generics.RetrieveAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenityDetailSerializer


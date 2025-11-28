from rest_framework import serializers
from .models import (User, City, Property, PropertyImage, Booking, Review, Amenity)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                'phone_number', 'role', 'avatar')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name']

class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name', 'city_image']

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'city', 'price_per_night', 'property_type']


class PropertyImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'property']


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'property', 'rating', 'comment']


class ReviewDetailSerializer(serializers.ModelSerializer):
    property = PropertyListSerializer()
    created_at = serializers.DateTimeField(format='%d-%m-%Y')
    class Meta:
        model = Review
        fields = ['property', 'guest', 'rating', 'stars', 'comment', 'created_at']

class PropertyDetailSerializer(serializers.ModelSerializer):
    property_images = PropertyImageListSerializer(many=True, read_only=True)
    rating = ReviewListSerializer(many=True, read_only=True)
    property_review = ReviewListSerializer(many=True, read_only=True)
    city = CityListSerializer()
    owner = UserSimpleSerializer()
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = ['title', 'city', 'price_per_night', 'property_type',
                  'rules', 'max_guests', 'bedrooms', 'bathrooms',
                  'description', 'property_images', 'rating', 'property_review', 'owner',
                  'is_active', 'stars', 'get_avg_rating', 'get_count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class PropertyImageDetailSerializer(serializers.ModelSerializer):
    property_images = PropertyImageListSerializer(many=True, read_only=True)
    class Meta:
        model = PropertyImage
        fields = ['property', 'property_image', 'property_images']


class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'property', 'check_in', 'check_out']

class BookingDetailSerializer(serializers.ModelSerializer):
    property = PropertyListSerializer()
    created_at = serializers.DateTimeField(format='%d-%m-%Y')
    class Meta:
        model = Booking
        fields = ['property', 'guest', 'check_in', 'check_out', 'status', 'created_at']


class AmenityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'amenity_name', 'property']

class AmenityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['amenity_name', 'icon', 'property']
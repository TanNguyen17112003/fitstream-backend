from rest_framework import serializers
from .models import (
    User, Workout, Subscription, Gym, GymMembership, PersonalTrainer, 
    PTSession, Livestream, EcommerceProduct, Order, OrderItem
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "full_name", "role", "profile_picture"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["id", "title", "description", "level", "video_url", "thumbnail_url", "duration", "created_at"]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "user", "plan", "start_date", "end_date", "payment_status", "created_at"]


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ["id", "name", "location", "contact_info", "opening_hours", "created_at"]


class GymMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMembership
        fields = ["id", "user", "gym", "membership_type", "payment_status", "start_date", "end_date", "created_at"]


class PersonalTrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalTrainer
        fields = ["id", "user", "bio", "specialization", "experience", "certification", "created_at"]


class PTSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PTSession
        fields = ["id", "customer", "pt", "scheduled_at", "status", "feedback", "created_at"]


class LivestreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livestream
        fields = ["id", "host", "title", "start_time", "end_time", "stream_url", "status", "created_at"]


class EcommerceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcommerceProduct
        fields = ["id", "name", "description", "price", "stock", "image_url", "created_at"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "total_price", "payment_status", "created_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "price"]

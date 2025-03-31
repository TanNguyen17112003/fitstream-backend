from rest_framework import serializers
from api.models import Workout

class WorkoutResponseDto(serializers.ModelSerializer):
    """DTO for workout response"""
    id = serializers.UUIDField(read_only=True)  # UUID field for the workout ID
    title = serializers.CharField(required=True, max_length=255)  # Title of the workout
    description = serializers.CharField(required=True, max_length=1000)  # Description of the workout
    level = serializers.ChoiceField(choices=["beginner", "intermediate", "advanced"])  # Difficulty level
    video_url = serializers.URLField(required=True)  # URL to the workout video
    thumbnail_url = serializers.URLField(required=True)  # URL to the thumbnail image
    duration = serializers.IntegerField(required=True)  # Duration in seconds
    created_at = serializers.DateTimeField(read_only=True)  # Timestamp when the workout was created

    class Meta:
        model = Workout
        fields = ["id", "title", "description", "level", "video_url", "thumbnail_url", "duration", "created_at"]
        read_only_fields = ["id", "created_at"]  # Fields that should not be modified by the user

class WorkoutRequestDto(serializers.ModelSerializer):
    """DTO for workout request"""
    title = serializers.CharField(required=True, max_length=255)  # Title of the workout
    description = serializers.CharField(required=True, max_length=1000)  # Description of the workout
    level = serializers.ChoiceField(choices=["beginner", "intermediate", "advanced"])  # Difficulty level
    video_url = serializers.URLField(required=True)  # URL to the workout video
    thumbnail_url = serializers.URLField(required=True)  # URL to the thumbnail image
    duration = serializers.IntegerField(required=True)  # Duration in seconds

    class Meta:
        model = Workout
        fields = ["title", "description", "level", "video_url", "thumbnail_url", "duration"]
        read_only_fields = ["id", "created_at"]
        # Fields that should not be modified by the user
    def create(self, validated_data):
        """Create a new workout instance"""
        return Workout.objects.create(**validated_data)

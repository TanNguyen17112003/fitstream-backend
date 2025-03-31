from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication  # Dùng JWT
from drf_spectacular.utils import extend_schema
from api.models import Workout
from .dtos import WorkoutRequestDto, WorkoutResponseDto  # Đúng với DTO đã định nghĩa


# 🔹 API: Lấy danh sách bài tập
@extend_schema(
    summary="Get list of workouts",
    description="Return a list of workouts.",
    tags=["Workout"],
    responses={200: WorkoutResponseDto(many=True)}
)
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_workouts(request):
    workouts = Workout.objects.all()
    serializer = WorkoutResponseDto(workouts, many=True)
    return Response(serializer.data)


# 🔹 API: Tạo bài tập mới
@extend_schema(
    summary="Create a new workout",
    description="Create and return a new workout.",
    tags=["Workout"],
    request=WorkoutRequestDto,  # Sử dụng đúng DTO request
    responses={201: WorkoutResponseDto, 400: "Invalid data"}
)
@api_view(["POST"])
@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])
def create_workout(request):
    serializer = WorkoutRequestDto(data=request.data)
    if serializer.is_valid():
        workout = serializer.save()
        response_serializer = WorkoutResponseDto(workout)
        return Response(response_serializer.data, status=201)
    return Response(serializer.errors, status=400)

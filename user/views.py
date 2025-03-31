from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication  # Dùng JWT
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from api.models import User
from .dtos import RegisterRequestDto, RegisterResponseDto, LoginRequestDto, LoginResponseDto  # Import DTO

# 🔹 Đăng ký User
@extend_schema(
    summary="Đăng ký User",
    description="Tạo một tài khoản User mới.",
    tags=["Auth"],
    request=RegisterRequestDto,  # <-- Sử dụng request
    responses={201: RegisterResponseDto, 400: "Dữ liệu không hợp lệ"}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterRequestDto(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(RegisterResponseDto(user).data, status=201)
    return Response(serializer.errors, status=400)


# 🔹 Đăng nhập User -> Trả về access token & refresh token
@extend_schema(
    summary="Đăng nhập User",
    description="User đăng nhập và nhận JWT token.",
    tags=["Auth"],
    request=LoginRequestDto,  # <-- Sử dụng request
    responses={200: LoginResponseDto, 400: "Thông tin không hợp lệ"}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginRequestDto(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]
    user = User.objects.filter(email=email).first()

    if user and check_password(password, user.password):  # Kiểm tra mật khẩu đã mã hóa
        refresh = RefreshToken.for_user(user)
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "profile_picture": user.profile_picture,
            "created_at": user.created_at,
        }
        return Response(response_data, status=200)

    return Response({"error": "Invalid email or password"}, status=400)


# 🔹 Lấy thông tin chi tiết User
@extend_schema(
    summary="Lấy thông tin User",
    description="Trả về thông tin User hiện tại (yêu cầu JWT token).",
    tags=["User"],
    responses={200: RegisterResponseDto, 401: "Chưa xác thực"}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # Fix lỗi Swagger không hiển thị Token
def get_user_detail(request):
    user = request.user
    return Response(RegisterResponseDto(user).data, status=200)


# 🔹 Lấy danh sách User dựa trên Role
@extend_schema(
    summary="Lấy danh sách User theo role",
    description="Trả về danh sách User theo role.",
    tags=["User"],
    parameters=[
        {
            "name": "role",
            "in": "query",
            "description": "Role của User",
            "required": True,
            "schema": {"type": "string"},
        }
    ],
    responses={200: RegisterResponseDto(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_users_by_role(request):
    role = request.query_params.get("role")
    
    if not role:
        return Response({"error": "Role parameter is required"}, status=400)

    users = User.objects.filter(role=role)
    serializer = RegisterResponseDto(users, many=True)
    return Response(serializer.data, status=200)
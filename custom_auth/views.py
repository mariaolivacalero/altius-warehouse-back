from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "password"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="User email"),
            "password": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="User password"
            ),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Successful login",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "refresh": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Refresh token"
                    ),
                    "access": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Access token"
                    ),
                },
            ),
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="Invalid credentials"
        ),
    },
)
@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    print(email, password)
    user = User.objects.filter(email=email).first()
    print(user)
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
    return Response(
        {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )

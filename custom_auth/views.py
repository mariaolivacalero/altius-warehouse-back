# custom_auth/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, GroupSerializer
from .models import User
from django.contrib.auth.models import Group
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method="post",
    security=[]
)

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
                type=openapi.TYPE_STRING, description="User password"
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
    security=[]
)
@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = User.objects.filter(email=email).first()
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
@swagger_auto_schema(
    method='get',
    responses={200: UserSerializer(many=True)},
    operation_description="List all users"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_list_create(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    responses={200: UserSerializer},
    operation_description="Retrieve a user by ID"
)
@swagger_auto_schema(
    method='put',
    request_body=UserSerializer,
    responses={200: UserSerializer},
    operation_description="Update a user by ID"
)
@swagger_auto_schema(
    method='patch',
    request_body=UserSerializer,
    responses={200: UserSerializer},
    operation_description="Partially update a user by ID"
)
@swagger_auto_schema(
    method='delete',
    responses={204: 'No Content'},
    operation_description="Delete a user by ID"
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='get',
    responses={200: GroupSerializer(many=True)},
    operation_description="List all groups"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def group_list(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)

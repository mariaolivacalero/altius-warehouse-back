from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Your API description",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="contact@yourapp.com"),
      license=openapi.License(name="Your License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=(SessionAuthentication, JWTAuthentication),
#    security=[{"Bearer": []}],  # This adds Bearer token to Swagger UI
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("auth/", include("custom_auth.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

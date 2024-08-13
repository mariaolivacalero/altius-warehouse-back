from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from inventory.models import AdministrativeUnit
from inventory.serializers import AdministrativeUnitSerializer


@swagger_auto_schema(
    method="post",
    request_body=AdministrativeUnitSerializer,
    responses={
        status.HTTP_201_CREATED: AdministrativeUnitSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    operation_description="Create a new administrative_unit",
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def administrative_unit_list(request):
    if request.method == "GET":
        categories = AdministrativeUnit.objects.all()
        serializer = AdministrativeUnitSerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = AdministrativeUnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def administrative_unit_detail(request, pk):
    try:
        administrative_unit = AdministrativeUnit.objects.get(pk=pk)
    except AdministrativeUnit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AdministrativeUnitSerializer(administrative_unit)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = AdministrativeUnitSerializer(
            administrative_unit, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        administrative_unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

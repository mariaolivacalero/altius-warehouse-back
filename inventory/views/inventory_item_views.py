from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from inventory.models import InventoryItem
from inventory.serializers import InventoryItemSerializer

@swagger_auto_schema(
    method='post',
    request_body=InventoryItemSerializer,
    responses={
        status.HTTP_201_CREATED: InventoryItemSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'
    },
    operation_description="Create a new item"
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def item_list(request):
    if request.method == 'GET':
        items = InventoryItem.objects.all()
        print(f"Number of items: {items.count()}")  # Debugging line
        for item in items:
            print(f"Inventory: {item}")  # Debugging line
        serializer = InventoryItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def item_detail(request, pk):
    try:
        item = InventoryItem.objects.get(pk=pk)
    except InventoryItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InventoryItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = InventoryItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


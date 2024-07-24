from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        print(f"Number of items: {items.count()}")  # Debugging line
        for item in items:
            print(f"Item: {item}")  # Debugging line
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def item_detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
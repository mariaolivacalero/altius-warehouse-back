# inventory/views/batch_views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from inventory.models import Batch
from inventory.serializers import BatchSerializer

@swagger_auto_schema(
    method='post',
    request_body=BatchSerializer,
    responses={
        status.HTTP_201_CREATED: BatchSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'
    },
    operation_description="Create a new batch"
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def batch_list(request):
    if request.method == 'GET':
        reception_batches = Batch.objects.all()
        serializer = BatchSerializer(reception_batches, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def batch_detail(request, pk):
    try:
        reception_batch = Batch.objects.get(pk=pk)
    except Batch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BatchSerializer(reception_batch)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BatchSerializer(reception_batch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        reception_batch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

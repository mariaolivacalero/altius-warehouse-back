# inventory/views/reception_batch_views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from inventory.models import ReceptionBatch
from inventory.serializers import ReceptionBatchSerializer

@swagger_auto_schema(
    method='post',
    request_body=ReceptionBatchSerializer,
    responses={
        status.HTTP_201_CREATED: ReceptionBatchSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'
    },
    operation_description="Create a new reception batch"
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reception_batch_list(request):
    if request.method == 'GET':
        reception_batches = ReceptionBatch.objects.all()
        serializer = ReceptionBatchSerializer(reception_batches, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReceptionBatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def reception_batch_detail(request, pk):
    try:
        reception_batch = ReceptionBatch.objects.get(pk=pk)
    except ReceptionBatch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReceptionBatchSerializer(reception_batch)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ReceptionBatchSerializer(reception_batch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        reception_batch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

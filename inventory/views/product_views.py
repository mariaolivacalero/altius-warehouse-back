import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from inventory.models import Product
from inventory.serializers import ProductSerializer

@swagger_auto_schema(
    method='post',
    request_body=ProductSerializer,
    responses={
        status.HTTP_201_CREATED: ProductSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'
    },
    operation_description="Create a new product"
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        print(f"Number of products: {products.count()}")  # Debugging line
        for product in products:
            print(f"Product: {product}")  # Debugging line
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='get',
    operation_description="Lookup product details using EAN code",
    manual_parameters=[
        openapi.Parameter(
            name='ean',
            in_=openapi.IN_QUERY,
            description='13-digit EAN code',
            type=openapi.TYPE_STRING,
            required=True,
            pattern=r'^\d{13}$'
        )
    ],
    responses={
        200: openapi.Response(
            description="Successful lookup",
            examples={
                "application/json": {
                    "ean": "5099750442227",
                    "name": "Michael Jackson - Thriller",
                    "category": {
                        "id": 15,
                        "name": "Music"
                    },
                    "issuing_country": "UK"
                }
            }
        ),
        400: openapi.Response(
            description="Bad request",
            examples={
                "application/json": {
                    "error": "EAN must be a 13-digit number"
                }
            }
        ),
        404: openapi.Response(
            description="Barcode not found",
            examples={
                "application/json": {
                    "error": "Barcode not found"
                }
            }
        ),
        500: openapi.Response(
            description="Server error",
            examples={
                "application/json": {
                    "error": "EAN Search API token not configured"
                }
            }
        ),
        503: openapi.Response(
            description="Service unavailable",
            examples={
                "application/json": {
                    "error": "EAN Search API error: timeout"
                }
            }
        )
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ean_lookup(request):
    """
    Lookup product details using EAN code
    """
    ean = request.query_params.get('ean')
    
    # Validate EAN parameter
    if not ean:
        return Response(
            {"error": "EAN parameter is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not ean.isdigit() or len(ean) != 13:
        return Response(
            {"error": "EAN must be a 13-digit number"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Get API token from settings
        api_token = getattr(settings, 'EAN_SEARCH_API_TOKEN', None)
        if not api_token:
            return Response(
                {"error": "EAN Search API token not configured"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Make API request to EAN Search
        url = 'https://api.ean-search.org/api'
        params = {
            'token': api_token,
            'op': 'barcode-lookup',
            'ean': ean,
            'format': 'json',
            'language': 4
        }

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()

        # Check if product was found
        if not data or not isinstance(data, list):
            return Response(
                {"error": "Barcode not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Return the first product found
        product_data = data[0]
        
        # Format the response to match your needs
        result = {
            'ean': product_data.get('ean'),
            'name': product_data.get('name'),
            'category': {
                'id': product_data.get('categoryId'),
                'name': product_data.get('categoryName')
            },
            'issuing_country': product_data.get('issuingCountry')
        }

        return Response(result)

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": f"EAN Search API error: {str(e)}"}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
# views.py
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FashionProduct
from .serializers import FashionProductSerializer

class Products(APIView):
    def get(self, request):
        try:
            products = FashionProduct.objects.all()
            product_serializer = FashionProductSerializer(products, many=True)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AddProduct(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Specify the file path here
            file_path = '/Users/adityabisen/Desktop/StyleSense AI/StyleSense-Backend/backend/product/product_info.csv'

            with open(file_path, 'r', encoding='utf-8') as csv_file:
                decoded_file = csv.DictReader(csv_file)
                
                for row in decoded_file:
                    # Extract numerical value from price string (e.g., "Rs.1,499.00")
                    price_str = row['Price'].replace('Rs.', '').replace(',', '')
                    # Convert price to float
                    price = float(price_str)
                    
                    fashion_product_data = {
                        'name': row['Product Name'],
                        'price': price,
                        'url': row['Product Link'],
                        'images': row['Image Link'],
                        'colour': row['Color'],
                    }
                    
                    fashion_product_serializer = FashionProductSerializer(data=fashion_product_data)
                    if fashion_product_serializer.is_valid():
                        fashion_product_serializer.save()
                    else:
                        return Response(fashion_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

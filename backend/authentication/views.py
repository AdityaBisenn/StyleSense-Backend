from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

class Test(APIView):
    def get(self, request):
        # Check PostgreSQL connection
        try:
            # Use a simple query to test the connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                if row:
                    connected = True
                else:
                    connected = False
        except Exception as e:
            connected = False

        if connected:
            message = 'PostgreSQL server is connected.'
        else:
            message = 'Failed to connect to PostgreSQL server.'

        return Response({'message': message})

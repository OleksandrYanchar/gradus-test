from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    """Simple healthcheck endpoint to verify server and database status."""

    def get(self, request, *args, **kwargs):
        errors = []
        try:
            # Check database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")  # Test query
            db_connected = True
        except Exception as e:
            db_connected = False
            errors.append(f"Database connection failed: {str(e)}")

        return Response(
            {
                "database": db_connected,
                "error": errors,
            },
            status=status.HTTP_200_OK,
        )

from django.shortcuts import render
from rest_framework.response import Response 
from django.contrib.auth.models import User

# Create your views here.

def delete_user(request, user_id):
    """
    View to delete a user by ID.
    """
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=204)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

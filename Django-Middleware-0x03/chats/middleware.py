from datetime import datetime
from rest_framework.response import Response

class RequestLoggingMiddleware :
    """
    Middleware to log request details.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request method and path
        user = request.user if request.user.is_authenticated else "Anonymous"
        print(f"{datetime.now()} - User: {user} - Path: {request.path}")
        
        # Call the next middleware or view
        response = self.get_response(request)
        
        return response
    
class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the application based on time.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if 9 <= current_hour < 18:  # Allow access only between 9 AM and 6 PM
            return self.get_response(request)
        else:
            return Response({"detail": "Access restricted outside of business hours."}, status=403)
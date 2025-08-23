from datetime import datetime
from rest_framework.response import Response
import logging

# Configure logging for requests
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class RequestLoggingMiddleware :
    """
    Middleware to log request details.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request method and path
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path} - Method: {request.method}"
        logging.info(log_message)
        
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
        
class OffensiveLanguageMiddleware :
    """
    Middleware to filter offensive language in requests and rate-limit messages per IP.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track message timestamps per IP
        self.ip_message_log = {}
        self.MESSAGE_LIMIT = 5
        self.TIME_WINDOW = 60  # seconds (1 minute)

    def __call__(self, request):
        if request.method == 'POST' and 'message' in getattr(request, 'data', {}):
            ip = self.get_client_ip(request)
            now = datetime.now().timestamp()
            # Initialize or clean up old timestamps
            timestamps = self.ip_message_log.get(ip, [])
            # Remove timestamps older than TIME_WINDOW
            timestamps = [ts for ts in timestamps if now - ts < self.TIME_WINDOW]
            if len(timestamps) >= self.MESSAGE_LIMIT:
                return Response({"detail": "Rate limit exceeded: Max 5 messages per minute."}, status=429)
            # Add current timestamp
            timestamps.append(now)
            self.ip_message_log[ip] = timestamps
            message = request.data['message']

        
        return self.get_response(request)

    def contains_offensive_language(self, message):
        # Placeholder for actual offensive language detection logic
        offensive_words = ['badword1', 'badword2']  # Example offensive words
        return any(word in message.lower() for word in offensive_words)

    def get_client_ip(self, request):
        # Try to get the real IP if behind a proxy
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
class RolepermissionMiddleware:
    """
    Middleware to restrict access based on user roles.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.user.has_role('admin'):
                return Response({"detail": "You do not have permission to view this resource."}, status=403)
        return self.get_response(request)
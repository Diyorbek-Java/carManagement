from django.http import HttpResponse

class CorsMiddleware:
    """
    Custom middleware to handle CORS (Cross-Origin Resource Sharing) headers.
    This middleware ensures that the appropriate headers are added to all responses,
    including preflight requests (OPTIONS).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Handle preflight requests (OPTIONS)
        if request.method == "OPTIONS" and "HTTP_ACCESS_CONTROL_REQUEST_METHOD" in request.META:
            response = HttpResponse(status=204)  # 204 No Content for preflight requests
            response["Content-Length"] = "0"
            response["Access-Control-Max-Age"] = "86400"  # Cache preflight response for 24 hours
        else:
            # For non-preflight requests, proceed with the normal response
            response = self.get_response(request)

        # Add CORS headers to all responses
        origin = request.headers.get("Origin", "*")
        response["Access-Control-Allow-Origin"] = origin  # Dynamically allow the request origin
        response["Access-Control-Allow-Methods"] = "DELETE, GET, OPTIONS, PATCH, POST, PUT"
        response["Access-Control-Allow-Headers"] = "accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with"
        response["Access-Control-Allow-Credentials"] = "true"  # Allow credentials (e.g., cookies)

        return response
from django.shortcuts import redirect
from django.conf import settings


class RestrictAdminAccessMiddleware:
    # Middleware to restrict access to Django Admin to only staff and superusers.
    
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        # Check if the user is trying to access the Django Admin panel
        if request.path.startswith('/admin/'):

            # If user is not staff or superuser, redirect them
            if not (request.user.is_staff or request.user.is_superuser):
                return redirect('home')
        
        return self.get_response(request)
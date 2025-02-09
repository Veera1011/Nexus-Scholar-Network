
import bcrypt
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import SimpleRateThrottle
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from authnsn.models import  Staff
from datetime import timedelta
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.conf import settings
import jwt
from authnsn.session_manager import SessionManager

# Create your views here.
class Staffdashboard(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    session_manager = SessionManager() # We'll handle authentication manually

    def get(self, request):
        # Check for access token in cookies
        session_id = request.COOKIES.get('session_id')
        
        if not session_id:
            return redirect('student-login')
        
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                raise jwt.InvalidTokenError()

            user = get_user_model().objects.get(id=session.user_id)
            # First check if user is a staff member
            staff_data = Staff.objects.filter(staff_id=user.username).first()
            if staff_data:
                context = {
                    'user_type': 'staff',
                    'staff_id': staff_data.staff_id,
                    'email': staff_data.email,
                    'name': staff_data.name if hasattr(staff_data, 'name') else None
                }
                return render(request, 'staff_dashboard.html', context)


            return HttpResponse('Profile not found', status=404)
            
        except (jwt.InvalidTokenError, get_user_model().DoesNotExist):
            response = redirect('student-login')
            response.delete_cookie('session_id')
            return response
            
        except (jwt.InvalidTokenError, get_user_model().DoesNotExist):
            # Invalid token or user not found
            return redirect('staff-login')  # Default to student login


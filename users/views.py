from django.contrib.auth import update_session_auth_hash
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, Address
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserProfileSerializer, 
    ChangePasswordSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    AddressSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user account",
        operation_summary="User Registration",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'username', 'password', 'password_confirm'],
            properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description='User email address (will be used for login)',
                    example='user@example.com'
                ),
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Unique username for the account',
                    example='johndoe123'
                ),
                'first_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='User first name (optional)',
                    example='John'
                ),
                'last_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='User last name (optional)',
                    example='Doe'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_PASSWORD,
                    description='Password (minimum 8 characters)',
                    example='SecurePass123!'
                ),
                'password_confirm': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_PASSWORD,
                    description='Confirm password (must match password)',
                    example='SecurePass123!'
                ),
            }
        ),
        responses={
            201: openapi.Response(
                description="User successfully created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                'email': openapi.Schema(type=openapi.TYPE_STRING, example='user@example.com'),
                                'username': openapi.Schema(type=openapi.TYPE_STRING, example='johndoe123'),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING, example='John'),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='Doe'),
                                'date_joined': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                            }
                        ),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                    }
                )
            ),
            400: openapi.Response(
                description="Validation errors",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'email': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            example=['This field is required.']
                        ),
                        'password': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            example=['This password is too short. It must contain at least 8 characters.']
                        ),
                    }
                )
            )
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Debug information
            print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
            print(f"DEBUG: Request data: {request.data}")
            print(f"DEBUG: Authorization header: {request.META.get('HTTP_AUTHORIZATION', 'Not provided')}")
            
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(
                    {"error": "refresh_token is required in request body"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create RefreshToken object and blacklist it
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                print(f"DEBUG: Token blacklisted successfully")
                return Response(
                    {"message": "Successfully logged out"}, 
                    status=status.HTTP_205_RESET_CONTENT
                )
            except Exception as token_error:
                print(f"DEBUG: Token blacklist error: {str(token_error)}")
                # Even if blacklisting fails, we can still return success
                # as the main purpose is to indicate logout
                return Response(
                    {"message": "Logged out (token may already be invalid)"}, 
                    status=status.HTTP_205_RESET_CONTENT
                )
                
        except Exception as e:
            print(f"DEBUG: General logout error: {str(e)}")
            return Response(
                {"error": f"Logout failed: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response({'message': 'Password changed successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Send email (in production, you'd want to use a proper email service)
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            try:
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'Password reset email sent.'})
            except Exception as e:
                return Response(
                    {'error': 'Failed to send email.'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
                user = User.objects.get(pk=uid)
                token = serializer.validated_data['token']
                
                if default_token_generator.check_token(user, token):
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    return Response({'message': 'Password reset successful.'})
                else:
                    return Response(
                        {'error': 'Invalid token.'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except (User.DoesNotExist, ValueError):
                return Response(
                    {'error': 'Invalid user.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Address.objects.none()
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        address = self.get_object()
        # Set all other addresses to not default
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        # Set this address as default
        address.is_default = True
        address.save()
        return Response({'message': 'Default address updated.'})

    @action(detail=False, methods=['get'])
    def default(self, request):
        try:
            default_address = Address.objects.get(user=request.user, is_default=True)
            serializer = self.get_serializer(default_address)
            return Response(serializer.data)
        except Address.DoesNotExist:
            return Response(
                {'message': 'No default address found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

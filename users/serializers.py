from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User, Address


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace username field with email field
        self.fields['email'] = serializers.EmailField(required=True)
        if 'username' in self.fields:
            del self.fields['username']

    def validate(self, attrs):
        # Use email for authentication
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Since our User model uses email as USERNAME_FIELD, pass email as username
            authenticate_kwargs = {
                'username': email,  # This will be treated as email due to USERNAME_FIELD
                'password': password,
            }
            
            try:
                authenticate_kwargs['request'] = self.context['request']
            except KeyError:
                pass

            self.user = authenticate(**authenticate_kwargs)

            if not self.user:
                raise serializers.ValidationError('Invalid email or password.')

            if not self.user.is_active:
                raise serializers.ValidationError('User account is disabled.')

        else:
            raise serializers.ValidationError('Must include email and password.')

        # Call parent's validate but pass the modified data
        refresh = self.get_token(self.user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not authenticate(username=user.email, password=value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        
        # If this is set as default, make all other addresses not default
        if validated_data.get('is_default', False):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # If this is set as default, make all other addresses not default
        if validated_data.get('is_default', False):
            Address.objects.filter(user=instance.user, is_default=True).exclude(id=instance.id).update(is_default=False)
        
        return super().update(instance, validated_data)

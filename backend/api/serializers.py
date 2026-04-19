from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Resume, Favorite, Notification


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'login', 'password', 'name', 'surname', 'patronymic',
            'email', 'phone', 'address', 'role', 'company', 'auth_method'
        ]

    def validate(self, data):
        if data.get('role') == 'employer' and not data.get('company'):
            raise serializers.ValidationError({'company': 'Название компании обязательно для работодателя'})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['login'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Неверный логин или пароль')
        if not user.is_active:
            raise serializers.ValidationError('Аккаунт заблокирован')
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'login', 'name', 'surname', 'patronymic',
            'email', 'phone', 'address', 'role', 'company', 'auth_method', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ResumeSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_user_name(self, obj):
        return f'{obj.user.surname} {obj.user.name}'

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'employer':
            return Favorite.objects.filter(employer=request.user, resume=obj).exists()
        return False

    def get_favorites_count(self, obj):
        return obj.favorited_by.count()


class FavoriteSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(read_only=True)
    resume_id = serializers.PrimaryKeyRelatedField(
        queryset=Resume.objects.all(), source='resume', write_only=True
    )

    class Meta:
        model = Favorite
        fields = ['id', 'resume', 'resume_id', 'created_at']
        read_only_fields = ['id', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class ChangePasswordSerializer(serializers.Serializer):
    """Смена пароля — plain Serializer (требование: минимум 2 Serializer)"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Неверный текущий пароль')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    """Логаут через инвалидацию refresh токена"""
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        try:
            RefreshToken(value)
        except Exception:
            raise serializers.ValidationError('Невалидный или истёкший токен')
        return value

    def save(self):
        token = RefreshToken(self.validated_data['refresh'])
        token.blacklist()

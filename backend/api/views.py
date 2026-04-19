from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Resume, Favorite, Notification
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    ResumeSerializer, FavoriteSerializer, NotificationSerializer,
    ChangePasswordSerializer, LogoutSerializer,
    get_tokens_for_user
)
from .filters import ResumeFilter


# ─── AUTH ────────────────────────────────────────────────────────────────────

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                **tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                **tokens
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """CBV — логаут через blacklist refresh токена"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Вы вышли из системы'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── RESUME ──────────────────────────────────────────────────────────────────

class MyResumesView(generics.ListCreateAPIView):
    """Работник: список своих резюме и создание"""
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}


class ResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Работник: редактирование/удаление своего резюме (полный CRUD)"""
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}


class ResumeSearchView(generics.ListAPIView):
    """
    Работодатель: поиск специалистов с фильтрами.
    ?profession=programmer&level=senior&city=almaty
    ?experience_min=2&experience_max=10
    ?has_bachelor=true&has_master=true
    ?language=english
    ?search=Иванов
    """
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ResumeFilter
    search_fields = ['name', 'surname', 'about', 'profession_other']
    ordering_fields = ['created_at', 'experience_years']
    ordering = ['-created_at']

    def get_queryset(self):
        return Resume.objects.exclude(user=self.request.user).select_related('user')

    def get_serializer_context(self):
        return {'request': self.request}


# ─── FAVORITES ───────────────────────────────────────────────────────────────

class FavoriteListView(generics.ListAPIView):
    """CBV — Работодатель: список избранных"""
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(employer=self.request.user).select_related('resume__user')


class ToggleFavoriteView(APIView):
    """CBV — Лайк/анлайк резюме"""
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        if request.user.role != 'employer':
            return Response(
                {'error': 'Только работодатели могут добавлять в избранное'},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            resume = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            return Response({'error': 'Резюме не найдено'}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(
            employer=request.user, resume=resume
        )
        if created:
            company_name = request.user.company or request.user.login
            Notification.objects.create(
                user=resume.user,
                message=f'Ваше резюме понравилось компании «{company_name}»'
            )
            return Response({'status': 'added'})
        else:
            favorite.delete()
            return Response({'status': 'removed'})


# ─── NOTIFICATIONS ───────────────────────────────────────────────────────────

class NotificationListView(generics.ListAPIView):
    """CBV — список уведомлений"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


# ─── FBV — Function Based Views ──────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notifications_read(request):
    """FBV #1 — пометить все уведомления прочитанными"""
    count = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return Response({'marked_read': count})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count(request):
    """FBV #2 — счётчик непрочитанных уведомлений"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return Response({'unread': count})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """FBV #3 — смена пароля"""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'Пароль успешно изменён'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resume_stats(request):
    """FBV #4 — статистика: сколько раз лайкнули резюме работника"""
    if request.user.role != 'worker':
        return Response({'error': 'Только для работников'}, status=status.HTTP_403_FORBIDDEN)
    resumes = Resume.objects.filter(user=request.user)
    data = [
        {
            'resume_id': r.id,
            'profession': r.profession,
            'favorites_count': r.favorited_by.count()
        }
        for r in resumes
    ]
    return Response({'stats': data, 'total_resumes': resumes.count()})

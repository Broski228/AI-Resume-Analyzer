from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('Логин обязателен')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [('worker', 'Работник'), ('employer', 'Работодатель')]

    login = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='worker')
    company = models.CharField(max_length=255, blank=True)  # только для работодателя
    auth_method = models.CharField(max_length=20, default='other')  # google/icloud/phone/other

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def __str__(self):
        return f'{self.login} ({self.role})'


class Resume(models.Model):
    LEVEL_CHOICES = [
        # IT
        ('junior', 'Junior'), ('middle', 'Middle'), ('senior', 'Senior'), ('lead', 'Lead'),
        # Педагоги
        ('no_category', 'Без категории'), ('category_2', '2-я категория'),
        ('category_1', '1-я категория'), ('highest', 'Высшая'), ('sheber', 'Шебер'),
        # Врачи
        ('intern', 'Интерн'), ('resident', 'Резидент'), ('specialist', 'Специалист'),
        ('highest_med', 'Высшая категория'),
        # Рабочие
        ('rank_1', '1-й разряд'), ('rank_2', '2-й разряд'), ('rank_3', '3-й разряд'),
        ('rank_4', '4-й разряд'), ('rank_5', '5-й разряд'), ('rank_6', '6-й разряд'),
        # Общие
        ('beginner', 'Начинающий'), ('expert', 'Эксперт'),
    ]

    PROFESSION_CHOICES = [
        ('programmer', 'Программист'),
        ('teacher', 'Учитель'),
        ('doctor', 'Врач'),
        ('lawyer', 'Юрист'),
        ('accountant', 'Бухгалтер'),
        ('driver', 'Водитель'),
        ('engineer', 'Инженер'),
        ('designer', 'Дизайнер'),
        ('manager', 'Менеджер'),
        ('other', 'Другое'),
    ]

    CITY_CHOICES = [
        ('almaty', 'Алматы'), ('astana', 'Астана'), ('shymkent', 'Шымкент'),
        ('karaganda', 'Караганда'), ('aktobe', 'Актобе'), ('taraz', 'Тараз'),
        ('pavlodar', 'Павлодар'), ('ust_kamenogorsk', 'Усть-Каменогорск'),
        ('semey', 'Семей'), ('atyrau', 'Атырау'), ('kostanay', 'Костанай'),
        ('kyzylorda', 'Кызылорда'), ('uralsk', 'Уральск'), ('petropavlovsk', 'Петропавловск'),
    ]

    LANGUAGE_CHOICES = [
        ('kazakh', 'Казахский'), ('russian', 'Русский'), ('english', 'Английский'),
        ('chinese', 'Китайский'), ('german', 'Немецкий'), ('french', 'Французский'),
        ('turkish', 'Турецкий'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    photo = models.ImageField(upload_to='resume_photos/', blank=True, null=True)

    # Личные данные
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    # Профессиональные данные
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES)
    profession_other = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    experience_years = models.PositiveIntegerField(default=0)

    # Местоположение
    city = models.CharField(max_length=30, choices=CITY_CHOICES, default='almaty')

    # Образование
    has_bachelor = models.BooleanField(default=False)
    bachelor_university = models.CharField(max_length=255, blank=True)
    bachelor_years = models.CharField(max_length=20, blank=True)  # например "2018-2022"

    has_master = models.BooleanField(default=False)
    master_university = models.CharField(max_length=255, blank=True)
    master_years = models.CharField(max_length=20, blank=True)

    # Опыт работы
    work_places = models.TextField(blank=True)  # где работал

    # Проекты
    has_projects = models.BooleanField(default=False)
    project_links = models.TextField(blank=True)

    # Языки (хранятся через M2M или просто JSON список)
    languages = models.JSONField(default=list)

    # О себе
    about = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.surname} {self.name} — {self.profession}'


class Favorite(models.Model):
    """Работодатель лайкнул резюме работника"""
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employer', 'resume')

    def __str__(self):
        return f'{self.employer.login} → {self.resume}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.user.login}] {self.message[:50]}'

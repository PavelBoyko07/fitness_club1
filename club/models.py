from django.conf import settings
from django.db import models
from django.utils.text import slugify


class FitnessDirection(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название направления')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL-адрес')
    description = models.TextField(blank=True, null=True, verbose_name='Описание направления')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    icon_image = models.ImageField(upload_to='direction_icons/', blank=True, null=True, verbose_name='Иконка направления')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'направление фитнеса'
        verbose_name_plural = 'направления фитнеса'
        ordering = ['name']

    def __str__(self):
        return self.name


class TrainingType(models.Model):
    name = models.CharField(max_length=120, verbose_name='Тип тренировки')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'тип тренировки'
        verbose_name_plural = 'типы тренировок'
        ordering = ['name']

    def __str__(self):
        return self.name


class Membership(models.Model):
    name = models.CharField(max_length=120, verbose_name='Название абонемента')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='URL')
    description = models.TextField(max_length=2500, verbose_name='Описание абонемента')
    price = models.PositiveIntegerField(verbose_name='Цена')
    duration_days = models.PositiveIntegerField(verbose_name='Срок действия, дней')
    visits_count = models.PositiveIntegerField(default=12, verbose_name='Количество посещений')
    direction = models.ForeignKey(FitnessDirection, on_delete=models.CASCADE, related_name='memberships', verbose_name='Направление')
    training_type = models.ForeignKey(TrainingType, on_delete=models.SET_NULL, null=True, blank=True, related_name='memberships', verbose_name='Тип тренировки')
    image = models.ImageField(upload_to='membership_images/', blank=True, null=True, verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'абонемент'
        verbose_name_plural = 'абонементы'
        ordering = ['price']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='ФИО тренера')
    specialization = models.CharField(max_length=150, verbose_name='Специализация')
    experience = models.PositiveIntegerField(verbose_name='Опыт работы, лет')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='trainer_photos/', blank=True, null=True, verbose_name='Фото тренера')

    class Meta:
        verbose_name = 'тренер'
        verbose_name_plural = 'тренеры'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class MembershipTrainer(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='membership_trainers', verbose_name='Тренер')
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='membership_trainers', verbose_name='Абонемент')

    class Meta:
        verbose_name = 'тренер абонемента'
        verbose_name_plural = 'тренеры абонементов'
        unique_together = ['trainer', 'membership']

    def __str__(self):
        return f'{self.trainer.full_name} — {self.membership.name}'


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает подтверждения'
        ACTIVE = 'active', 'Активна'
        COMPLETED = 'completed', 'Завершена'
        CANCELLED = 'cancelled', 'Отменена'

    class PaymentType(models.TextChoices):
        CASH = 'cash', 'Наличными'
        CARD = 'card', 'Банковская карта'
        ONLINE = 'online', 'Онлайн-оплата'

    client_name = models.CharField(max_length=150, verbose_name='Имя клиента')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name='Статус заявки')
    application_date = models.DateField(auto_now_add=True, verbose_name='Дата заявки')
    total_price = models.PositiveIntegerField(verbose_name='Стоимость')
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, default=PaymentType.CARD, verbose_name='Способ оплаты')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fitness_applications', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'заявка на абонемент'
        verbose_name_plural = 'заявки на абонементы'
        ordering = ['-application_date']

    def __str__(self):
        return f'{self.client_name} — {self.application_date}'


class ApplicationMembership(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='application_memberships', verbose_name='Заявка')
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='application_memberships', verbose_name='Абонемент')
    visits_per_week = models.PositiveIntegerField(default=3, verbose_name='Посещений в неделю')

    class Meta:
        verbose_name = 'абонемент в заявке'
        verbose_name_plural = 'абонементы в заявках'
        unique_together = ['application', 'membership']

    def __str__(self):
        return f'{self.application.client_name} — {self.membership.name}'


class Stock(models.Model):
    title = models.CharField(max_length=180, verbose_name='Название акции')
    description = models.TextField(verbose_name='Описание акции')
    discount_percent = models.PositiveIntegerField(default=10, verbose_name='Скидка, %')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'акция'
        verbose_name_plural = 'акции'
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='fitness_reviews', verbose_name='Пользователь')
    author_name = models.CharField(max_length=150, verbose_name='Имя автора')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='Оценка')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} — {self.rating}/5'


class Visit(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'planned', 'Запланировано'
        VISITED = 'visited', 'Посещено'
        MISSED = 'missed', 'Пропущено'

    client_name = models.CharField(max_length=150, verbose_name='Имя клиента')
    phone_number = models.CharField(max_length=20, verbose_name='Телефон')
    direction = models.ForeignKey(FitnessDirection, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits', verbose_name='Направление')
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits', verbose_name='Тренер')
    visit_date = models.DateTimeField(verbose_name='Дата и время посещения')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED, verbose_name='Статус')

    class Meta:
        verbose_name = 'посещение'
        verbose_name_plural = 'посещения'
        ordering = ['-visit_date']

    def __str__(self):
        return f'{self.client_name} — {self.visit_date:%d.%m.%Y %H:%M}'


class ScheduleType(models.Model):
    class WeekDay(models.TextChoices):
        MONDAY = 'monday', 'Понедельник'
        TUESDAY = 'tuesday', 'Вторник'
        WEDNESDAY = 'wednesday', 'Среда'
        THURSDAY = 'thursday', 'Четверг'
        FRIDAY = 'friday', 'Пятница'
        SATURDAY = 'saturday', 'Суббота'
        SUNDAY = 'sunday', 'Воскресенье'

    name = models.CharField(max_length=150, verbose_name='Название занятия')
    day_of_week = models.CharField(max_length=20, choices=WeekDay.choices, verbose_name='День недели')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedule_items', verbose_name='Тренер')
    direction = models.ForeignKey(FitnessDirection, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedule_items', verbose_name='Направление')
    hall = models.CharField(max_length=100, default='Основной зал', verbose_name='Зал')

    class Meta:
        verbose_name = 'тип расписания'
        verbose_name_plural = 'типы расписания'
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f'{self.name} — {self.get_day_of_week_display()} {self.start_time}'


class Message:
    pass
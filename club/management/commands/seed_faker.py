import random
from datetime import datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from faker import Faker

from club.models import (Application,ApplicationMembership,FitnessDirection,Membership,MembershipTrainer,Review,ScheduleType,Stock,Trainer,TrainingType,Visit,)


class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными через Faker'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Очистить старые тестовые данные')
        parser.add_argument('--users', type=int, default=5)
        parser.add_argument('--trainers', type=int, default=8)
        parser.add_argument('--applications', type=int, default=10)
        parser.add_argument('--reviews', type=int, default=12)
        parser.add_argument('--visits', type=int, default=15)

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker('ru_RU')
        User = get_user_model()

        if options['clear']:
            ApplicationMembership.objects.all().delete()
            Application.objects.all().delete()
            MembershipTrainer.objects.all().delete()
            Membership.objects.all().delete()
            Trainer.objects.all().delete()
            TrainingType.objects.all().delete()
            FitnessDirection.objects.all().delete()
            Stock.objects.all().delete()
            Review.objects.all().delete()
            Visit.objects.all().delete()
            ScheduleType.objects.all().delete()
            User.objects.filter(username__startswith='faker_user_').delete()

            self.stdout.write(self.style.WARNING('Старые тестовые данные удалены'))

        directions_data = [
            ('Тренажёрный зал', 'Силовые тренировки, набор мышечной массы и поддержание формы.'),
            ('Йога', 'Занятия для гибкости, спокойствия и восстановления.'),
            ('Бокс', 'Функциональные тренировки, техника ударов и выносливость.'),
            ('Пилатес', 'Укрепление мышц корпуса, осанка и мягкая нагрузка.'),
            ('Кардио', 'Тренировки для жиросжигания и развития выносливости.'),
        ]

        directions = []

        for index, (name, description) in enumerate(directions_data, start=1):
            direction, _ = FitnessDirection.objects.get_or_create(
                slug=f'{slugify(name, allow_unicode=True)}-{index}',
                defaults={
                    'name': name,
                    'description': description,
                    'is_active': True,
                }
            )
            directions.append(direction)

        training_types_data = [
            ('Групповая', 'Тренировка в группе с тренером.'),
            ('Индивидуальная', 'Персональное занятие с тренером.'),
            ('Онлайн', 'Дистанционная тренировка по расписанию.'),
        ]

        training_types = []

        for name, description in training_types_data:
            training_type, _ = TrainingType.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            training_types.append(training_type)

        memberships = []

        for direction in directions:
            for training_type in training_types:
                visits_count = random.choice([8, 12, 16])
                duration_days = random.choice([30, 60, 90])
                price = random.choice([2500, 3500, 4500, 6000, 7500])

                name = f'{direction.name} — {training_type.name}, {visits_count} занятий'
                slug = slugify(name, allow_unicode=True)

                membership, _ = Membership.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'name': name,
                        'description': fake.paragraph(nb_sentences=4),
                        'price': price,
                        'duration_days': duration_days,
                        'visits_count': visits_count,
                        'direction': direction,
                        'training_type': training_type,
                        'is_active': True,
                    }
                )

                memberships.append(membership)

        trainers = []

        specializations = [
            'Силовой тренинг',
            'Йога',
            'Бокс',
            'Пилатес',
            'Кардио',
            'Функциональный тренинг',
        ]

        for _ in range(options['trainers']):
            trainer = Trainer.objects.create(
                full_name=fake.name(),
                specialization=random.choice(specializations),
                experience=random.randint(1, 15),
                description=fake.paragraph(nb_sentences=4),
            )
            trainers.append(trainer)

        for membership in memberships:
            selected_trainers = random.sample(trainers, k=random.randint(1, min(3, len(trainers))))

            for trainer in selected_trainers:
                MembershipTrainer.objects.get_or_create(
                    trainer=trainer,
                    membership=membership,
                )

        users = []

        for i in range(options['users']):
            user = User.objects.create_user(
                username=f'faker_user_{i + 1}',
                email=f'faker_user_{i + 1}@example.com',
                password='12345678',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            users.append(user)

        for _ in range(options['applications']):
            user = random.choice(users)
            selected_memberships = random.sample(memberships, k=random.randint(1, min(3, len(memberships))))
            total_price = sum(membership.price for membership in selected_memberships)

            application = Application.objects.create(
                client_name=fake.name(),
                phone_number=self.fake_phone(fake),
                status=random.choice([
                    Application.Status.PENDING,
                    Application.Status.ACTIVE,
                    Application.Status.COMPLETED,
                    Application.Status.CANCELLED,
                ]),
                total_price=total_price,
                payment_type=random.choice([
                    Application.PaymentType.CASH,
                    Application.PaymentType.CARD,
                    Application.PaymentType.ONLINE,
                ]),
                user=user,
            )

            for membership in selected_memberships:
                ApplicationMembership.objects.create(
                    application=application,
                    membership=membership,
                    visits_per_week=random.choice([1, 2, 3, 4]),
                )

        today = timezone.localdate()

        stocks_data = [
            ('Скидка на первый абонемент', 15),
            ('Приведи друга', 20),
            ('Летний фитнес', 10),
            ('Семейный абонемент', 25),
        ]

        for title, discount in stocks_data:
            start_date = today - timedelta(days=random.randint(1, 10))
            end_date = today + timedelta(days=random.randint(10, 40))

            Stock.objects.create(
                title=title,
                description=fake.paragraph(nb_sentences=3),
                discount_percent=discount,
                start_date=start_date,
                end_date=end_date,
                is_active=True,
            )

        for _ in range(options['reviews']):
            user = random.choice(users + [None])

            Review.objects.create(
                user=user,
                author_name=fake.name(),
                text=fake.paragraph(nb_sentences=3),
                rating=random.randint(3, 5),
                is_published=True,
            )

        for _ in range(options['visits']):
            visit_date = self.fake_visit_datetime()

            Visit.objects.create(
                client_name=fake.name(),
                phone_number=self.fake_phone(fake),
                direction=random.choice(directions),
                trainer=random.choice(trainers),
                visit_date=visit_date,
                status=random.choice([
                    Visit.Status.PLANNED,
                    Visit.Status.VISITED,
                    Visit.Status.MISSED,
                ]),
            )

        weekdays = [choice[0] for choice in ScheduleType.WeekDay.choices]

        for direction in directions:
            for _ in range(3):
                start_hour = random.randint(8, 20)
                start_time = time(hour=start_hour, minute=random.choice([0, 30]))
                end_time = time(hour=start_hour + 1, minute=start_time.minute)

                ScheduleType.objects.create(
                    name=f'{direction.name} — занятие',
                    day_of_week=random.choice(weekdays),
                    start_time=start_time,
                    end_time=end_time,
                    trainer=random.choice(trainers),
                    direction=direction,
                    hall=random.choice(['Основной зал', 'Зал №1', 'Зал №2', 'Кардио-зона']),
                )

        self.stdout.write(self.style.SUCCESS('База успешно заполнена тестовыми данными через Faker'))

    def fake_phone(self, fake):
        return f'+3712{fake.random_number(digits=7, fix_len=True)}'

    def fake_visit_datetime(self):
        random_date = timezone.localdate() + timedelta(days=random.randint(-20, 30))
        random_time = time(
            hour=random.randint(8, 21),
            minute=random.choice([0, 30])
        )

        return timezone.make_aware(datetime.combine(random_date, random_time))
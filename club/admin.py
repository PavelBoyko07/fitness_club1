from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Application,
    ApplicationMembership,
    FitnessDirection,
    Membership,
    MembershipTrainer,
    Review,
    ScheduleType,
    Stock,
    Trainer,
    TrainingType,
    Visit,
)


@admin.register(FitnessDirection)
class FitnessDirectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'icon_preview', 'name', 'slug', 'is_active', 'created_at')
    list_display_links = ('name',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'icon_preview')

    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" width="60" height="60" style="border-radius:12px; object-fit:cover;" />', obj.icon_image.url)
        return 'Нет изображения'

    icon_preview.short_description = 'Превью'


@admin.register(TrainingType)
class TrainingTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'description')


class MembershipTrainerInline(admin.TabularInline):
    model = MembershipTrainer
    extra = 1


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'name', 'direction', 'training_type', 'price', 'duration_days', 'visits_count', 'is_active')
    list_display_links = ('name',)
    list_editable = ('price', 'is_active')
    list_filter = ('direction', 'training_type', 'is_active')
    search_fields = ('name', 'description', 'direction__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'image_preview')
    inlines = [MembershipTrainerInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="border-radius:12px; object-fit:cover;" />', obj.image.url)
        return 'Нет изображения'

    image_preview.short_description = 'Превью'


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo_preview', 'full_name', 'specialization', 'experience')
    list_display_links = ('full_name',)
    list_filter = ('specialization',)
    search_fields = ('full_name', 'specialization')
    readonly_fields = ('photo_preview',)
    inlines = [MembershipTrainerInline]

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="90" height="90" style="border-radius:50%; object-fit:cover;" />', obj.photo.url)
        return 'Нет фото'

    photo_preview.short_description = 'Фото'


@admin.register(MembershipTrainer)
class MembershipTrainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'trainer', 'membership')
    list_filter = ('trainer', 'membership')
    search_fields = ('trainer__full_name', 'membership__name')


class ApplicationMembershipInline(admin.TabularInline):
    model = ApplicationMembership
    extra = 1


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'phone_number', 'status', 'payment_type', 'total_price', 'application_date')
    list_display_links = ('client_name',)
    list_editable = ('status',)
    list_filter = ('status', 'payment_type', 'application_date')
    search_fields = ('client_name', 'phone_number')
    readonly_fields = ('application_date',)
    inlines = [ApplicationMembershipInline]


@admin.register(ApplicationMembership)
class ApplicationMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'membership', 'visits_per_week')
    list_filter = ('membership',)
    search_fields = ('application__client_name', 'membership__name')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'discount_percent', 'start_date', 'end_date', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'rating', 'is_published', 'created_at')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'rating')
    search_fields = ('author_name', 'text')


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'phone_number', 'direction', 'trainer', 'visit_date', 'status')
    list_editable = ('status',)
    list_filter = ('status', 'direction', 'trainer')
    search_fields = ('client_name', 'phone_number')


@admin.register(ScheduleType)
class ScheduleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'day_of_week', 'start_time', 'end_time', 'trainer', 'direction', 'hall')
    list_filter = ('day_of_week', 'direction', 'trainer')
    search_fields = ('name', 'hall', 'trainer__full_name', 'direction__name')

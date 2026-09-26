from django.contrib import admin
from .models import Category, Task, TimeSession, TaskActivity


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'color', 'created_at')
    search_fields = ('name', 'user__username')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'category',
        'priority',
        'status',
        'due_date',
    )
    list_filter = (
        'priority',
        'status',
        'category',
    )
    search_fields = (
        'title',
        'description',
    )


@admin.register(TimeSession)
class TimeSessionAdmin(admin.ModelAdmin):
    list_display = (
        'task',
        'started_at',
        'ended_at',
        'duration_seconds',
        'is_active',
        'created_at',
    )
    list_filter = ('is_active',)
    search_fields = ('task__title',)


@admin.register(TaskActivity)
class TaskActivityAdmin(admin.ModelAdmin):
    list_display = (
        'task',
        'action',
        'timestamp',
    )
    list_filter = ('action',)
    search_fields = ('task__title',)
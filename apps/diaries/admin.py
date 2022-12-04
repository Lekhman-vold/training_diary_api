from django.contrib import admin
from apps.diaries.models import Diary


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    search_fields = [
        'id',
    ]

    list_display = (
        'id',
        'user',
        'biceps',
        'forearm',
        'chest',
        'leg',
        'calves',
        'waist',
        'created_at',
    )

    readonly_fields = ("updated_at",)

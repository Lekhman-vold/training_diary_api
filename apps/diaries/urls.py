from django.urls import path

from apps.diaries.views import DiaryView

urlpatterns = [
    path('', DiaryView.as_view(), name='diary'),
]

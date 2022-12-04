from rest_framework import serializers

from apps.diaries.models import Diary


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = "__all__"

        extra_kwargs = {
            'updated_at': {'read_only': True}
        }

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.diaries.models import Diary
from apps.diaries.serializers import DiarySerializer


class DiaryView(APIView):
    def get(self, request, format=None):
        if request.user.is_anonymous:
            return Response({'error': 'only authorized'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        diaries = Diary.objects.filter(user=request.user)
        serializer = DiarySerializer(diaries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response({'error': 'only authorized'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            Diary.objects.update_or_create(
                id=request.data.get('id'),
                defaults=request.data,
                user=request.user
            )
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        if request.user.is_anonymous:
            return Response({'error': 'only authorized'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            diary = Diary.objects.filter(id=request.data.get('id'))
            if not diary:
                return Response({'error': 'not found'},
                                status=status.HTTP_404_NOT_FOUND)
            diary.delete()
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)

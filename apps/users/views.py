import requests
from django.core.validators import validate_email
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.base.models import SiteConfiguration
from apps.users.models import User
from apps.users.serializers import UserSerializer


class Signup(APIView):

    def signin_url(self):
        conf = SiteConfiguration.get_solo()
        return f"{conf.protocol}://{conf.domain}"

    def post(self, request, format=None):
        data = request.data

        if not data.get('email') or not data.get('password'):
            return Response({'error': 'email and password is required'},
                            status=status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(email=data.get('email')).first()

        if user:
            return Response({'error': 'user already exists'},
                            status=status.HTTP_404_NOT_FOUND)

        user = User(
            email=data.get('email'),
            first_name=data.get('first_name', None),
        )
        try:
            validate_email(user.email)
        except Exception as e:
            return Response({'error': e},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            user.validate_password(data['password'])
        except Exception as e:
            return Response({'error': e},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            user.set_password(data['password'])
            user.full_clean()
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user.save()

        response = requests.post(f'{self.signin_url()}api/user/signin/', data={
            'email': user.email,
            'password': data['password'],
        })

        if not response.status_code == 200:
            return Response({'error': 'signin failed'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = response.json()

        return Response({'refresh': response.get('refresh'),
                         'access': response.get('access')
                         }, status=status.HTTP_200_OK)


class UpdateUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

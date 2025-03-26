from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Добавление конкретных полей в сообщение об ошибке
        if not email or not password:
            return Response({'email': 'This field is required.', 'password': 'This field is required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Проверяем учетные данные пользователя
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            # Refresh-токен для обновления access-токена
            access_token = str(refresh.access_token)
            # Access-токен для авторизации
            return Response({"access": access_token, "refresh": str(refresh)}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

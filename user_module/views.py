from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from .constants import *
from .models import User



class UserSignupView(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


class UserMetaMaskView(ModelViewSet):
    serializer_class = None
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            metamask = data.get('metamask')
            if not metamask:
                return Response({SUCCESS: False, ERROR: "Metamask is required"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.filter(metamask=metamask).first()
            if not user:
                return Response({SUCCESS: False, ERROR: "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            response = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': user.id,
            }
            if user:
                return Response({SUCCESS: True, MESSAGE: "Metamask exists", DATA: response},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({SUCCESS: False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
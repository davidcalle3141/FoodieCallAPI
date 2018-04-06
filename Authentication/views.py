from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import AccountSerializer


class AuthRegister(APIView):
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class CustomObtainAuthToken(ObtainAuthToken):
    #def post(self, request, *args, **kwargs):
     #   response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
      #  token = Token.objects.get(key=response.data['token'])
       # return Response({'token': token.key, 'id': token.user})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, "BOOOOO")

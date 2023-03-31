from accounts import serializers
from accounts.models import User
from rest_framework import generics, permissions, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class RegisterAPIView(GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserListAPIView(generics.ListAPIView):
#     serializer_class = serializers.UserSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#     queryset = User.objects.all()


# class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.UserSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#     # queryset = User.objects.all()
#     lookup_field = 'id'

#     def get_queryset(self):
#         return User.objects.exclude(is_superuser=True)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.exclude(is_superuser=True)
    lookup_field = 'id'


# Don't understand the use of this yet
# class LoginAPIView(GenericAPIView):
#     serializer_class = serializers.LoginSerializer

#     def post(self, request):
#         email = request.data.get('email', None)
#         password = request.data.get('password', None)

#         user = authenticate(username=email, password=password)
        
#         if user:
#             serializer = self.serializer_class(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({"message": "Invalid Credentials Provided, try again!"}, status=status.HTTP_401_UNAUTHORIZED)
    
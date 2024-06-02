from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import User, Doctor, Review
from .serializers import UserSerializer, DoctorSerializer, LoginSerializer, ReviewSerializer
from .permissions import IsOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create']:
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        return super().get_permissions()

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            if user.is_doctor:
                user_data = DoctorSerializer(user.doctor).data
                role = 'doctor'
            else:
                user_data = UserSerializer(user).data
                role = 'user'

            return Response({
                "token": token.key,
                "role": role,
                "user": user_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return Review.objects.filter(doctor_id=doctor_id)

    def perform_create(self, serializer):
        doctor_id = self.kwargs['doctor_id']
        doctor = Doctor.objects.get(id=doctor_id)
        serializer.save(user=self.request.user, doctor=doctor)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return Review.objects.filter(doctor_id=doctor_id)

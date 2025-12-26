from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
# Create your views here.
class AuthViewSet(viewsets.GenericViewSet):
    '''인증관련 viewset'''
    serializer_class = UserSerializer

    # AllowAny : 로그인 없이 접근가능
    @action(detail=False, methods=['POST'],permission_classes=[AllowAny])
    def register(self, request):
        '''회원가입'''
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # instance가 없으면 create , 있으면 update
            user = serializer.save()   # 내부 규칙에 의해서 update or create 자동 호출 
            token,created = Token.objects.get_or_create(user=user)
            return Response({
                'token' : token.key,
                'user':UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def login(self,request):
        '''로그인'''
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():            
            user = serializer.validated_data
            token,created = Token.objects.get_or_create(user=user)
            return Response({
                'token' : token.key,
                'user':UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['POST'],permission_classes=[IsAuthenticated])
    def logout(self,request):
        '''로그아웃'''
        request.user.auth_token.delete()
        return Response({'message':'로그아웃 되었습니다.'})
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self,request):
        serializer =  UserSerializer(request.user)
        return Response(serializer.data)
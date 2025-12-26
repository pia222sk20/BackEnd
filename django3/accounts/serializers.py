from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    '''로그인후 사용자 정보 반환'''
    class Meta:
        model=User
        fields = ['id','username','email','first_name','last_name']
        read_only_fields = ['id']
class RegisterSerializer(serializers.ModelSerializer):
    '''회원가입'''
    password = serializers.CharField(write_only=True,min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','password_confirm']

    def validate(self,data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        return data
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('이미 사용중인 이메일입니다.')
        return value    

    def create(self,validated_data):
        validated_data.pop('password_confirm')
        # create_user 비밀번호를 자동으로 해싱... 암호화
        user = User.objects.create_user(**validated_data)
        return user
class LoginSerializer(serializers.Serializer):
    '''로그인 처리'''
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)  # 응답 Response에 노출되지 않음
    def validate(self,data):
        user = authenticate(**data)
        if user is None:
            raise serializers.ValidationError('아이디 혹은 비밀번호가 일치하지 않습니다.')
        if not user.is_active:
            raise serializers.ValidationError('비활성화된 사용자입니다.')
        return user
# Funtion-based Views(@api_view) : 가장 간단한 형태의 뷰
# APIview : 클래스 기반의 기본 뷰
# Generic View : 반복되는 패턴을 자동화한 뷰
# ViewSet : 관련된 여러 View를 하나로 묶은 View
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
# Create your views here.
'''
# 함수형 뷰
from rest_framework.decorators import api_view
@api_view(['GET','POST'])
def post_list(request):
    if request == 'GET':
        pass
    elif request == 'POST':
        pass
    pass

# 클래스 뷰
from rest_framework.views import APIView
class PostListAPIView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        pass
    pass
from rest_framework import generics
# Generic view
class PoistListCreateView(generics.ListCreateAPIView):
    pass
'''
# ViewSet과 ModelViewSet  - 최종 권장 방식
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Post, Comment, Category, Tag
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
    CategorySerializer,
    TagSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    '''카테고리 ViewSet(읽기전용)'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    @action(detail=True, methods=['get'])
    def posts(self,request,pk=None):
        '''특정 카테고리의 게시글 목록'''
        category=self.get_object()
        posts = Post.objects.filter(category=category, status='published')
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)  # 리스트형태의 json
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    '''태그 ViewSet(읽기전용)'''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    @action(detail=True, methods=['get'])
    def posts(self,request,pk=None):
        '''특정 태그의 게시글 목록'''
        tag=self.get_object()
        posts = tag.objects.filter(status='published')
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)  # 리스트형태의 json
class PostViewSet(viewsets.ModelViewSet):
    """
    게시글 ViewSet (전체 CRUD)
    """
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)    


class CommentViewSet(viewsets.ModelViewSet):
    """
    댓글 ViewSet (전체 CRUD)
    """
    queryset = Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)    
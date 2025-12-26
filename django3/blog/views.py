# Funtion-based Views(@api_view) : 가장 간단한 형태의 뷰
# APIview : 클래스 기반의 기본 뷰
# Generic View : 반복되는 패턴을 자동화한 뷰
# ViewSet : 관련된 여러 View를 하나로 묶은 View
from django.shortcuts import render

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
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 발행된 게시글만 표시 (작성자는 본인 글 모두 볼 수 있음)
        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        else:
            queryset = queryset.filter(status='published')
        
        return queryset.order_by('-created_at')
    
    # 작성자의 위변조를 방지
    def perform_create(self, serializer):
        """게시글 생성 시 작성자 자동 설정"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """게시글 발행"""
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': '권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.status = 'published'
        post.save()
        return Response({'status': '게시글이 발행되었습니다.'})
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """게시글 비공개"""
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': '권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.status = 'draft'
        post.save()
        return Response({'status': '게시글이 비공개되었습니다.'})
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """내가 작성한 게시글 목록"""
        posts = self.queryset.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def drafts(self, request):
        """임시저장 게시글 목록"""
        posts = self.queryset.filter(author=request.user, status='draft')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """특정 게시글의 댓글 목록"""
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    댓글 ViewSet (전체 CRUD)
    """
    queryset = Comment.objects.select_related('author', 'post')
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 쿼리 파라미터로 필터링
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        return queryset.order_by('created_at')
    
    def perform_create(self, serializer):
        """댓글 생성 시 작성자 자동 설정"""
        serializer.save(author=self.request.user)


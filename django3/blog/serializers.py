from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Post, Comment

class UserSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email','post_count']
        read_only_fields = ['id']
    
    def get_post_count(self, obj):  # get_field_name
        return obj.posts.count()

class CategorySerializer(serializers.ModelSerializer):
    """카테고리 Serializer"""
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_post_count(self, obj):
        return obj.posts.count()


class TagSerializer(serializers.ModelSerializer):
    """태그 Serializer"""
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'post_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_post_count(self, obj):
        return obj.posts.count()


class CommentSerializer(serializers.ModelSerializer):
    """댓글 Serializer"""
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'author_id', 'content', 
            'parent', 'replies', 'is_approved', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []
    
    def validate_content(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("댓글은 최소 2자 이상이어야 합니다.")
        if len(value) > 500:
            raise serializers.ValidationError("댓글은 최대 500자까지 작성 가능합니다.")
        return value


class PostListSerializer(serializers.ModelSerializer):
    """게시글 목록용 Serializer"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author', 'category', 
            'tags', 'status', 'views', 'comment_count', 'featured',
            'created_at', 'published_at'
        ]
        read_only_fields = ['id', 'slug', 'views', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    """게시글 상세용 Serializer"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'author', 'category', 'tags', 'comments', 'comment_count',
            'status', 'views', 'featured',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'slug', 'views', 'created_at', 'updated_at']

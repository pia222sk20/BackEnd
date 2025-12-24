from django.db import models
from django.contrib.auth.models import User
# ORM  - 쿼리대신 DB를 사용하는 방법
# 카테고리 모델 
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # 다대일 관계  Many-to-One
    # related_name='posts'  역참조 할때 사용하는 이름  User -> Post 목록에 접근할때 사용하는 이름
    # 설정안하면.. user.post_set.all()
    # 설정하면 .. user.posts.all()
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    # category.posts.all()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,
                                 blank=True,related_name='posts')   
    
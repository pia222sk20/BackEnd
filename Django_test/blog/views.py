from django.shortcuts import render
from .models import Post
# Create your views here.
def post_list(request): 
    '''모든 포스트 리스트를 보여준다'''   
    # 데이터베이스에서 post 테이블의 데이터를 전부가져와서 html에 전달
    # db를 담당하는 모델을 부른다
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html')
def post_detail(request):
    pass
def post_create(request):
    pass
def post_update(request):
    pass
def post_delete(request):
    pass
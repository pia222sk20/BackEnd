from django.shortcuts import render, redirect
from .models import Post
# Create your views here.
def post_list(request): 
    '''모든 포스트 리스트를 보여준다'''   
    # 데이터베이스에서 post 테이블의 데이터를 전부가져와서 html에 전달
    # db를 담당하는 모델을 부른다
    posts = Post.objects.all()
    print(f'posts: {posts}')    
    content = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html',content)
def post_detail(request):
    pass
def post_create(request):
    '''화면에서 post방식으로 전달한 데이터를 가지고 Post 테이블에 저장'''
    if request.method == 'POST':
        title = request.POST['title']   #  html에서 name = title
        content = request.POST['content']  # html에서 name = content
        post = Post(title=title, content=content)
        post.save()  # insert 쿼리가 실행
        return redirect('blog:post_list')  # DB가 갱신되면 새로운 DB에 정보를 가지고 화면을 refresh
    elif request.method == 'GET':        
        return render(request, 'blog/post_form.html')

def post_update(request):
    pass
def post_delete(request):
    pass
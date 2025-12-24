from django.shortcuts import render
from .models import *
from django.views.generic import CreateView, UpdateView, DeleteView, ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def post_list(request):
    pass
def post_detail(request,pk):
    pass

# LoginRequiredMixin : 인증되지 않은 사용자의 접근을 차단
# 인증되지 않는 사용자가 접근하면 
# 로그인 페이지로 리다이렉트
# 로그인 성공후 원래 요청한 url로 다시 이동
class PostCreateView(LoginRequiredMixin,CreateView):
    pass

class PostUpdateView(LoginRequiredMixin,UpdateView):
    pass
     
class PostDeleteView(LoginRequiredMixin,DeleteView):
    pass

from django.contrib.auth.decorators import login_required
@login_required
def add_comment(request,pk):
    pass

@login_required
def toggle_like(request, pk):
    pass

@login_required
def toggle_bookmark(request, pk):
    pass

# 카테고리 테이블의 값 추출
def category_posts(request,pk)
    pass

def search(request):
    pass

@login_required
def dashboard(request):
    pass
    
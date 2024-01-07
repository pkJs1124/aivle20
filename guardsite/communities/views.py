from django.shortcuts import render,redirect,get_object_or_404
from .models import Notice,Comment
from .forms import NoticeForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    notices = Notice.objects.all()
    page = request.GET.get("page",1)
    paginator = Paginator(notices,6)
    object_list = paginator.get_page(page)
    
    
    context = {
        'notices':object_list
    }
    return render(request,'communities/list.html',context)

@login_required
def create(request):
    if request.method =='POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save()
            
            return redirect(notice)
    else:
        form = NoticeForm()
    context = {'form':form}
    return render(request,'communities/form.html',context)

def detail(request,notice_pk):
    notice = get_object_or_404(Notice,pk=notice_pk)
    user = get_object_or_404(get_user_model(),pk=notice.user_id)
    comments = notice.comment_set.all()
    comment_form = CommentForm()
    context = {
        'notice':notice,
        'user':user,
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request,'communities/detail.html',context)

@require_POST
def delete(request,notice_pk):
    if request.user.is_authenticated:
        notice = get_object_or_404(Notice,pk=notice_pk)
        if request.user == notice.user:
            notice.delete()
        else:
            return redirect(notice)
    return redirect('communities:index')
    
@login_required
def update(request,notice_pk):
    notice = get_object_or_404(Notice,pk=notice_pk)
    if request.user == notice.user:
        if request.method == 'POST':
            form = NoticeForm(request.POST,instance=notice)
            if form.is_valid():
                form.save()
                return redirect(notice)
            
        else:
            form = NoticeForm(instance=notice)
    else:
        return redirect('communities:index')
    context = {'form':form,'notice':notice}
    return render(request,'communities/form.html',context)

@require_POST
def comments_create(request, notice_pk):
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    if request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.notice_id = notice_pk
            comment.user = request.user
            comment.save()
    return redirect('communities:detail', notice_pk)


@require_POST
def comments_delete(request, notice_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('communities:detail', notice_pk)

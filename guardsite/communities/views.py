from django.shortcuts import render,redirect,get_object_or_404
from .models import Notice
from .forms import NoticeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

# Create your views here.
def index(request):
    notices = Notice.objects.all()
    context = {
        'notices':notices
    }
    return render(request,'communities/index.html',context)

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
    context = {
        'notice':notice,
        'user':user
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
    
@require_POST
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
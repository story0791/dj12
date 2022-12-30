from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Board, Reply
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect("acc:login")

    pg = request.GET.get("page",1)
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            from acc.models import User
            try:
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b= Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()

    pag = Paginator(b, 2)
    obj=pag.get_page(pg)
    context={
        "bset": obj,
        "cate" : cate,
        "kw" : kw
    }
    return render(request, "board/index.html", context)

def detail(request, bpk):
    b=Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context={
        "b":b,
        "rset":r
    }
    return render(request, "board/detail.html", context)

def delete(request, bpk):
    b=Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
    else:
        pass # 혼내주기
    return redirect("board:index")

def create(request):
    if request.user.is_anonymous:
        return redirect("acc:login")

    if request.method == "POST":
        s=request.POST.get("sub")
        c=request.POST.get("con")
        Board(subject=s, content=c, pubdate=timezone.now(), writer=request.user).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def update(request, bpk):
    b=Board.objects.get(id=bpk)
    if b.writer != request.user:
        return redirect("board:index")
    if request.method == "POST":
        s=request.POST.get("sub")
        c=request.POST.get("con")
        b.subject, b.content=s,c
        b.save()
        return redirect("board:detail", bpk)
    context={
        "b":b
    }
    return render(request, "board/update.html", context)

def creply(request, bpk):
    b=Board.objects.get(id=bpk)
    c=request.POST.get("co")
    Reply(b=b, replyer=request.user, comment=c).save()
    return redirect("board:detail", bpk)

def dreply(request, bpk, rpk):
    r=Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else:
        pass # 혼내주기
    return redirect("board:detail", bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk)

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail", bpk)

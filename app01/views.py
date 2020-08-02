from django.shortcuts import render, redirect, HttpResponse
from app01 import models


# Create your views here.
def index(request):
    return redirect('/publisher_list/')


def publisher_list(request):
    # 返回所有出版社信息
    all_publisher = models.Publisher.objects.all().order_by("-id")
    # for i in all_publisher:
    #     name = i.name

    return render(request, "publisher_list.html", context={"all_publisher": all_publisher})


def publisher_add(request):
    if request.method == "POST":
        name = request.POST.get("pub_name")
        if not name:
            return render(request, "publisher_add.html", {"error": "出版社名称不能为空"})
        if models.Publisher.objects.filter(name=name):
            return render(request, "publisher_add.html", {"error": "出版社已存在"})
        models.Publisher.objects.create(name=name)
        return redirect("/publisher_list/")

    return render(request, "publisher_add.html")
    pass


def publisher_del(request):
    del_id = request.GET.get("id")
    obj = models.Publisher.objects.filter(pk=del_id)
    obj.delete()

    return redirect("/publisher_list/")


def publisher_edit(request):
    pk = request.GET.get('pk')
    pub_obj = models.Publisher.objects.get(pk=pk)
    if request.method == "POST":
        pub_obj.name = request.POST.get("pub_name", "")
        pub_obj.save()
        return redirect("/publisher_list/")

    return render(request, "publisher_edit.html", {"pk": pub_obj})


# 展示书籍
def book_list(request):
    # 查询所有数据，
    # 返回一个页面
    all_books = models.Book.objects.all()
    return render(request, "book_list.html", {"all_book": all_books})


def book_add(request):
    error = None
    if request.method == "POST":
        book_name = request.POST.get("book_name")
        pub_id = request.POST.get("pub")
        if not book_name:
            error = '填写错误'
        # models.Book.objects.create(name=book_name, publisher=models.Publisher.objects.get(pk=pub_id))
        elif models.Book.objects.filter(name=book_name):
            error = "书名重复"
        else:
            try:
                models.Book.objects.create(name=book_name, publisher_id=pub_id)
                return redirect('/book_list/')
            except Exception:
                pass
                # all_publishers = models.Publisher.objects.all()
                # return render(request, "book_add.html", {"all_publishers": all_publishers})
    all_publishers = models.Publisher.objects.all()
    return render(request, "book_add.html", {"all_publishers": all_publishers, 'error': error})


# 删除书籍
def book_del(request):
    book_id = request.GET.get('id')
    obj = models.Book.objects.filter(pk=book_id)
    obj.delete()
    return redirect('/book_list/')


def book_edit(request):
    pk = request.GET.get("id")
    book_obj = models.Book.objects.get(pk=pk)
    all_publishers = models.Publisher.objects.all()
    if request.method == "POST":
        # book_obj.name = request.POST.get("book_name", "")
        # book_obj.publisher_id = request.POST.get("pub", "")
        # book_obj.save()
        # 方法二
        book_name = request.POST.get("book_name", "")
        pub_id = request.POST.get("pub", "")
        models.Book.objects.filter(pk=pk).update(name=book_name, publisher_id=pub_id)

        return redirect("/book_list/")

    return render(request, "book_edit.html", {"pk": book_obj, "all_publishers": all_publishers})


def author_list(request):
    all_author = models.Author.objects.all()
    # for auth in all_author:
    #     print(auth)
    # auth.books.all()
    return render(request, "author_list.html", {"all_authors": all_author})


def author_add(request):
    all_books = models.Book.objects.all()
    if request.method == "POST":
        author_name = request.POST.get("author_name")
        book_ids = request.POST.getlist("book_ids")
        if models.Author.objects.filter(name=author_name):
            return render(request, "author_add.html", {"all_books": all_books, 'error': "作者也存在"})
        author_obj = models.Author.objects.create(name=author_name)
        author_obj.books.set(book_ids)  # 设置多对多
        return redirect('/author_list/')
    return render(request, "author_add.html", {"all_books": all_books})


def author_del(request):
    author_id = request.GET.get("id")
    obj = models.Author.objects.filter(pk=author_id)
    obj.delete()
    return redirect('/author_list/')


def author_edit(request):
    pk = request.GET.get('id')
    author_obj = models.Author.objects.get(pk=pk)
    all_books = models.Book.objects.all()
    if request.method == "POST":
        author_name = request.POST.get("author_name")
        book_ids = request.POST.getlist("book_ids")
        author_obj.name = author_name
        author_obj.save()
        author_obj.books.set(book_ids)
        return redirect('/author_list/')
    return render(request, "author_edit.html", {"all_books": all_books, "author_obj": author_obj})

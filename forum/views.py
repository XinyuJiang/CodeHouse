from django.http import response
from django.shortcuts import render
from django.template import loader
from py2neo import Graph, Node, Relationship
import pandas as pd
from forum.models import Userinfo, Tiezi, Dongtai, Comment_Dongtai, Comment_Tiezi
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.


def login(request):
    if request.method == "POST":
        mnickname = request.POST.get("nickname", None)
        mpassword = request.POST.get("password", None)
        print(mnickname, mpassword)
        try:
            user = Userinfo.objects.get(nickname=mnickname)
            # print("user",user)
            return HttpResponseRedirect('../index')
        except(KeyError, Userinfo.DoesNotExist):
            print("用户名未找到")
            return render(request, 'forum/login.html', {
                'nickename': mnickname,
                'error_message': "该用户不存在！",
            })
    return render(request, "forum/login.html", )
    # return HttpResponse("hello world!")


def register(request):
    if request.method == "POST":
        mnickname = request.POST.get("nickname", None)
        mpassword = request.POST.get("password", None)
        print(mnickname, mpassword)
        try:
            muser = Userinfo(nickname=mnickname, password=mpassword)
            # print("user",user)
            muser.save()
            print("注册成功")
            return HttpResponseRedirect('../index.html')
        except(KeyError, Userinfo.DoesNotExist):
            print("用户已存在，插入错误")
            return render(request, 'forum/register.html', {
                'nickename': mnickname,
                'error_message': "该用户不存在！",
            })
    return render(request, "forum/register.html", )


@csrf_exempt
def index(request):
    print(request, type(request))
    if True:
        print(request.POST.get("tag"))
        print(request.POST.get("tag"), request.POST.get("nickname"), request.POST.get("password"))
        if request.POST.get("tag") == "1":
            mnickname = request.POST.get("nickname", None)
            mpassword = request.POST.get("password", None)
            print(mnickname, mpassword)
            try:
                user = Userinfo.objects.get(nickname=mnickname)
                print("欢迎你，user", user.nickname)

                request.session['user_id'] = user.id
                print("session:", request.session['user_id'])

                return HttpResponse(json.dumps({
                    'nickname': mnickname,
                    'password': mpassword,
                }))
                # return render(request, 'forum/index.html', {#用render的话第三个参数会渲染页面
                #         'nickename': mnickname,
                #         'password': mpassword,
                #     })
            except(KeyError, Userinfo.DoesNotExist):
                print("用户名未找到")
                return render(request, 'forum/index.html', {
                    'nickename': mnickname,
                    'error_message': "该用户不存在！",
                })

        if request.POST.get("tag") == "2":
            mnickname = request.POST.get("nickname", None)
            mpassword = request.POST.get("password", None)
            memail = request.POST.get("email", None)
            mdepartment = request.POST.get("department", None)
            msex = request.POST.get("sex", None)
            print(mnickname, mpassword, memail, mdepartment, msex)
            try:
                muser = Userinfo(nickname=mnickname, password=mpassword, email=memail, sex=msex, department=mdepartment)
                # print("user",user)
                muser.save()
                request.session['user_id'] = muser.id
                print("注册成功聊！")
                return HttpResponse(json.dumps({
                    'nickname': mnickname,
                    'password': mpassword,
                }))
            except(KeyError, Userinfo.DoesNotExist):
                print("用户已存在，插入错误")
            print("session:",request.session['user_id'])
            return render(request, 'forum/index.html', {
                'nickname': 'Tom',
                'error_message': "该用户不存在！",
            })
        if request.POST.get("tag") == "4":
            request.session.flush()  # 删除所有session
            print("用户已注销")
            return HttpResponse(json.dumps({
                'status': "success",
            }))
        try:
            userid = request.session["user_id"]
        except:
            print("游客状态")
            return render(request, "forum/index.html")
        user = Userinfo.objects.get(id=userid)
        template = loader.get_template('forum/index.html')
        context = {
            'nickname': user.nickname,
        }
        print("刷新界面")
        return HttpResponse(template.render(context, request))


class CView(generic.ListView):
    template_name = 'forum/C.html'
    context_object_name = 'latest_tiezi_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return (Tiezi.objects.order_by('-create_time').filter(category="C")[:5])[::-1]


class CsharpView(generic.ListView):
    template_name = 'forum/Csharp.html'
    context_object_name = 'latest_tiezi_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return (Tiezi.objects.order_by('-create_time').filter(category="C#")[:5])[::-1]


class CplusView(generic.ListView):
    template_name = 'forum/C++.html'
    context_object_name = 'latest_tiezi_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return (Tiezi.objects.order_by('-create_time').filter(category="C++")[:5])[::-1]


class JavaView(generic.ListView):
    template_name = 'forum/Java.html'
    context_object_name = 'latest_tiezi_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return (Tiezi.objects.order_by('-create_time').filter(category="Java")[:5])[::-1]


class PythonView(generic.ListView):
    template_name = 'forum/Python.html'
    context_object_name = 'latest_tiezi_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return (Tiezi.objects.order_by('-create_time').filter(category="Python")[:5])[::-1]


class RView(generic.ListView):
    template_name = 'forum/R.html'
    context_object_name = 'latest_tiezi_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return (Tiezi.objects.order_by('-create_time').filter(category="R")[:5])[::-1]


@csrf_exempt
def postedit(request):
    print(request, type(request))
    print(request.POST.get("tag"), request.POST.get("title"), request.POST.get("content"))
    if request.POST.get("tag") == "1":
        mtitle = request.POST.get("title", None)
        mcontent = request.POST.get("content", None)
        print(mtitle, mcontent)
        try:
            muser_id = request.session['user_id']
        except:
            print("当前为游客状态")
            muser_id = "1"
        muser = Userinfo.objects.get(id=muser_id)
        try:
            mtiezi = Tiezi(user=muser, title=mtitle, content=mcontent, category="C", nickname=muser.nickname)
            # print("user",user)
            mtiezi.save()
            print("插入成功")
            return HttpResponse({
                'status': "success"
            })
        except(KeyError, Tiezi.DoesNotExist):
            print("插入帖子信息失败")
        return render(request, 'forum/index.html', {
            'error_message': "帖子插入失败！",
        })
    return render(request, "forum/postedit.html")


@csrf_exempt
def tucao(request):
    print(request, type(request))
    print(request.POST.get("tag"), request.POST.get("content"))
    if request.POST.get("tag") == "1":
        mcontent = request.POST.get("content", None)
        print(mcontent)
        try:
            muser_id = request.session['user_id']
        except:
            print("当前为游客状态")
            muser_id = 1
        muser = Userinfo.objects.get(id=muser_id)
        try:
            mdongtai = Dongtai(user=muser, content=mcontent, nickname=muser.nickname)
            # print("user",user)
            mdongtai.save()
            print("吐槽成功")
            return HttpResponse({
                'status': "success"
            })
        except(KeyError, Dongtai.DoesNotExist):
            print("发布吐槽失败")
        return render(request, 'forum/index.html', {
            'error_message': "吐槽发布失败！",
        })
    return render(request, "forum/tucao.html")


class Tiezi_DetailView(generic.DetailView):
    model = Tiezi
    template_name = 'forum/tiezi_details.html'
    # print(request, type(request))
    # print(request.POST.get("tag"), request.POST.get("content"))
    # if request.POST.get("tag") == "1":
    #     mcontent = request.POST.get("content", None)
    #     print(mcontent)
    #     try:
    #         muser_id = request.session['user_id']
    #     except:
    #         print("当前为游客状态")
    #         muser_id = 1
    #     muser = Userinfo.objects.get(id=muser_id)
    #     try:
    #         mdongtai = Dongtai(user=muser, content=mcontent,nickname=muser.nickname)
    #         # print("user",user)
    #         mdongtai.save()
    #         print("吐槽成功")
    #         return HttpResponse({
    #             'status': "success"
    #         })
    #     except(KeyError, Dongtai.DoesNotExist):
    #         print("发布吐槽失败")
    #     return render(request, 'forum/index.html', {
    #         'error_message': "吐槽发布失败！",
    #     })


# class LanguageCsharp(generic.ListView):
#     template_name = 'forum/Csharp.html'
#     context_object_name = 'C#_list'
#
#     def get_queryset(self):
#         """Return the last five published tiezi in C# language."""
#         return Tiezi.objects.get(category='C#').order_by('create_time')[:20]
#
#
# class LanguageJava(generic.ListView):
#     template_name = 'forum/Java.html'
#     context_object_name = 'Java_list'
#
#     def get_queryset(self):
#         """Return the last five published tiezi in Java language."""
#         return Tiezi.objects.get(category='Java').order_by('create_time')[:20]
#
#
# class LanguagePython(generic.ListView):
#     template_name = 'forum/Python.html'
#     context_object_name = 'Python_list'
#
#     def get_queryset(self):
#         """Return the last five published tiezi in Python language."""
#         return Tiezi.objects.get(category='Python').order_by('create_time')[:20]
#
#
# class LanguageR(generic.ListView):
#     template_name = 'forum/R.html'
#     context_object_name = 'R_list'
#
#     def get_queryset(self):
#         """Return the last five published tiezi in R language."""
#         return Tiezi.objects.get(category='R').order_by('create_time')[:20]


def tech_index(request):
    print(request, type(request))
    if request.is_ajax():
        print("ajax请求a ")
        print(request.POST.get("tag"), request.POST.get("nickname"), request.POST.get("password"))
        if request.POST.get("tag") == "1":
            mnickname = request.POST.get("nickname", None)
            mpassword = request.POST.get("password", None)
            print(mnickname, mpassword)
            try:
                user = Userinfo.objects.get(nickname=mnickname)
                print("欢迎你，user", user.nickname)

                request.session['user_id'] = user.id
                return HttpResponse(json.dumps({
                    'nickname': mnickname,
                    'password': mpassword,
                }))
                # return render(request, 'forum/index.html', {#用render的话第三个参数会渲染页面
                #         'nickename': mnickname,
                #         'password': mpassword,
                #     })
            except(KeyError, Userinfo.DoesNotExist):
                print("用户名未找到")
                return render(request, 'forum/tech_index.html', {
                    'nickename': mnickname,
                    'error_message': "该用户不存在！",
                })

        if request.POST.get("tag") == "2":
            mnickname = request.POST.get("nickname", None)
            mpassword = request.POST.get("password", None)
            memail = request.POST.get("email", None)
            mdepartment = request.POST.get("department", None)
            msex = request.POST.get("sex", None)
            print(mnickname, mpassword, memail, mdepartment, msex)
            try:
                muser = Userinfo(nickname=mnickname, password=mpassword, email=memail, sex=msex, department=mdepartment)
                # print("user",user)
                muser.save()
                request.session['user_id'] = muser.id
                print("注册成功聊！")
                return HttpResponse(json.dumps({
                    'nickname': mnickname,
                    'password': mpassword,
                }))
            except(KeyError, Userinfo.DoesNotExist):
                print("用户已存在，插入错误")
            return render(request, 'forum/tech_index.html', {
                'nickname': 'Tom',
                'error_message': "该用户不存在！",
            })
    else:
        try:
            userid = request.session["user_id"]
        except:
            print("游客状态")
            return render(request, "forum/tech_index.html")
        user = Userinfo.objects.get(id=userid)
        template = loader.get_template('forum/tech_index.html')
        context = {
            'nickname': user.nickname,
        }
        print("非AJAX")
        return HttpResponse(template.render(context, request))


@csrf_exempt
def chat_index(request):
    # print(request, type(request))
    # print(request.POST.get("tag"), request.POST.get("pinglun"))
    # print(request, type(request))
    # if request.is_ajax():
    #     print("ajax请求a ")
    #     print(request.POST.get("tag"), request.POST.get("nickname"), request.POST.get("password"))
    #     if request.POST.get("tag") == "1":
    #         mnickname = request.POST.get("nickname", None)
    #         mpassword = request.POST.get("password", None)
    #         print(mnickname, mpassword)
    #         try:
    #             user = Userinfo.objects.get(nickname=mnickname)
    #             print("欢迎你，user", user.nickname)
    #
    #             request.session['user_id'] = user.id
    #             return HttpResponse(json.dumps({
    #                 'nickname': mnickname,
    #                 'password': mpassword,
    #             }))
    #             # return render(request, 'forum/index.html', {#用render的话第三个参数会渲染页面
    #             #         'nickename': mnickname,
    #             #         'password': mpassword,
    #             #     })
    #         except(KeyError, Userinfo.DoesNotExist):
    #             print("用户名未找到")
    #             return render(request, 'forum/index.html', {
    #                 'nickename': mnickname,
    #                 'error_message': "该用户不存在！",
    #             })
    #
    #     if request.POST.get("tag") == "2":
    #         mnickname = request.POST.get("nickname", None)
    #         mpassword = request.POST.get("password", None)
    #         memail = request.POST.get("email", None)
    #         mdepartment = request.POST.get("department", None)
    #         msex = request.POST.get("sex", None)
    #         print(mnickname, mpassword, memail, mdepartment, msex)
    #         try:
    #             muser = Userinfo(nickname=mnickname, password=mpassword, email=memail, sex=msex, department=mdepartment)
    #             # print("user",user)
    #             muser.save()
    #             request.session['user_id'] = muser.id
    #             print("注册成功聊！")
    #             return HttpResponse(json.dumps({
    #                 'nickname': mnickname,
    #                 'password': mpassword,
    #             }))
    #         except(KeyError, Userinfo.DoesNotExist):
    #             print("用户已存在，插入错误")
    #         return render(request, 'forum/index.html', {
    #             'nickname': 'Tom',
    #             'error_message': "该用户不存在！",
    #         })
    if request.POST.get("tag") == "3":
        mpinglun = request.POST.get("pinglun", None)
        mnickname = request.POST.get("nickname", None)
        mcontent = request.POST.get("content", None)
        print("评论，动态主人姓名，动态内容")
        print(mpinglun, mnickname, mcontent)
        try:
            muser_id = request.session['user_id']
        except:
            print("当前为游客状态")
            muser_id = 1
        muser = Userinfo.objects.get(id=muser_id)
        try:
            mdongtai = Dongtai.objects.filter(content=mcontent, nickname=mnickname)[0]
            # print("user",user)
            mpinglun = Comment_Dongtai(user=muser, dongtai=mdongtai, nickname=muser.nickname, content=mpinglun)
            mpinglun.save()
            print("吐槽成功")
            pinglun_list = []
            latest_tucao_list = (Dongtai.objects.order_by('-create_time')[0:10])[::-1]
            for tucao in latest_tucao_list:
                pinglun = Comment_Dongtai.objects.filter(dongtai_id=tucao.id)
                if pinglun:
                    pinglun_list.append(pinglun)  # 这条动态有评论的情况下存储评论
            template = loader.get_template('forum/chat_index.html')
            context = {
                'latest_tucao_list': latest_tucao_list,
                'pinglun_list': pinglun_list,
                'status': "success"
            }
            return HttpResponse(template.render(context, request))
        except(KeyError, Dongtai.DoesNotExist):
            print("发布吐槽失败")
        return render(request, 'forum/index.html', {
            'error_message': "吐槽发布失败！",
        })
    pinglun_list = []
    latest_tucao_list = (Dongtai.objects.order_by('-create_time')[0:10])[::-1]
    for tucao in latest_tucao_list:
        pinglun = Comment_Dongtai.objects.filter(dongtai_id=tucao.id)
        if pinglun:
            pinglun_list.append(pinglun)  # 这条动态有评论的情况下存储评论
    try:
        userid = request.session["user_id"]
    except:
        print("游客状态")
        template = loader.get_template('forum/chat_index.html')
        context = {
            'latest_tucao_list': latest_tucao_list,
            'pinglun_list': pinglun_list,
        }
        return HttpResponse(template.render(context, request))
    user = Userinfo.objects.get(id=userid)
    print("非AJAX")
    template = loader.get_template('forum/chat_index.html')
    context = {
        'latest_tucao_list': latest_tucao_list,
        'pinglun_list': pinglun_list,
        'nickname': user.nickname,

    }

    return HttpResponse(template.render(context, request))


def person_index(request):
    print(request, type(request))
    if request.is_ajax():
        print("ajax请求a ")
        print(request.POST.get("tag"), request.POST.get("nickname"), request.POST.get("password"))
        if request.POST.get("tag") == "1":
            mnickname = request.POST.get("nickname", None)
            mpassword = request.POST.get("password", None)
            print(mnickname, mpassword)
            try:
                user = Userinfo.objects.get(nickname=mnickname)
                print("欢迎你，user", user.nickname)

                request.session['user_id'] = user.id
                return HttpResponse(json.dumps({
                    'nickname': mnickname,
                    'password': mpassword,
                }))
                # return render(request, 'forum/index.html', {#用render的话第三个参数会渲染页面
                #         'nickename': mnickname,
                #         'password': mpassword,
                #     })
            except(KeyError, Userinfo.DoesNotExist):
                print("用户名未找到")
                return render(request, 'forum/person_index.html', {
                    'nickename': mnickname,
                    'error_message': "该用户不存在！",
                })

        if request.POST.get("tag") == "2":
            mnickname = request.POST.get("nickname", None)
            mpassword = request.POST.get("password", None)
            memail = request.POST.get("email", None)
            mdepartment = request.POST.get("department", None)
            msex = request.POST.get("sex", None)
            print(mnickname, mpassword, memail, mdepartment, msex)
            try:
                muser = Userinfo(nickname=mnickname, password=mpassword, email=memail, sex=msex, department=mdepartment)
                # print("user",user)
                muser.save()
                request.session['user_id'] = muser.id
                print("注册成功聊！")
                return HttpResponse(json.dumps({
                    'nickname': mnickname,
                    'password': mpassword,
                }))
            except(KeyError, Userinfo.DoesNotExist):
                print("用户已存在，插入错误")
            return render(request, 'forum/person_index.html', {
                'nickname': 'Tom',
                'error_message': "该用户不存在！",
            })
    else:
        try:
            userid = request.session["user_id"]
        except:
            print("游客状态")
            return render(request, "forum/person_index.html")
        user = Userinfo.objects.get(id=userid)
        template = loader.get_template('forum/person_index.html')
        context = {
            'nickname': user.nickname,
        }
        print("非AJAX")
        return HttpResponse(template.render(context, request))


def other(request):
    print(request, type(request))
    if request.is_ajax():
        print("ajax请求a ")
        print(request.POST.get("tag"), request.POST.get("nickname"), request.POST.get("password"))
        if request.POST.get("tag") == "1":
            mnickname = request.POST.get("nickname", None)
            mpassword = request.POST.get("password", None)
            print(mnickname, mpassword)
            try:
                user = Userinfo.objects.get(nickname=mnickname)
                print("欢迎你，user", user.nickname)

                request.session['user_id'] = user.id
                return HttpResponse(json.dumps({
                    'nickname': mnickname,
                    'password': mpassword,
                }))
                # return render(request, 'forum/index.html', {#用render的话第三个参数会渲染页面
                #         'nickename': mnickname,
                #         'password': mpassword,
                #     })
            except(KeyError, Userinfo.DoesNotExist):
                print("用户名未找到")
                return render(request, 'forum/Other.html', {
                    'nickename': mnickname,
                    'error_message': "该用户不存在！",
                })

        if request.POST.get("tag") == "2":
            mnickname = request.POST.get("nickname", None)
            mpassword = request.POST.get("password", None)
            memail = request.POST.get("email", None)
            mdepartment = request.POST.get("department", None)
            msex = request.POST.get("sex", None)
            print(mnickname, mpassword, memail, mdepartment, msex)
            try:
                muser = Userinfo(nickname=mnickname, password=mpassword, email=memail, sex=msex, department=mdepartment)
                # print("user",user)
                muser.save()
                request.session['user_id'] = muser.id
                print("注册成功聊！")
                return HttpResponse(json.dumps({
                    'nickname': mnickname,
                    'password': mpassword,
                }))
            except(KeyError, Userinfo.DoesNotExist):
                print("用户已存在，插入错误")
            return render(request, 'forum/Other.html', {
                'nickname': 'Tom',
                'error_message': "该用户不存在！",
            })
    else:
        try:
            userid = request.session["user_id"]
        except:
            print("游客状态")
            return render(request, "forum/Other.html")
        user = Userinfo.objects.get(id=userid)
        template = loader.get_template('forum/Other.html')
        context = {
            'nickname': user.nickname,
        }
        print("非AJAX")
        return HttpResponse(template.render(context, request))

@csrf_exempt
def kg(request):
    if request.POST.get("tag") == "1":
        mitem = request.POST.get("item", None)
        print(mitem,type(mitem))
        graph = Graph(host='localhost', auth=('xinyu', 'jxy961031'))
        mitem = "'" + mitem + "'"
        l = "MATCH (a) where a.name =" + mitem + "return a.name, a.time, a.type"
        g0 = graph.run(l).to_data_frame()
        s = "MATCH (a)-[r:RELATION]->(b) where a.name=" + mitem + " and r.type = " + "'co_times' " + " return b.name, b.type order by r.value DESC LIMIT 10"
        g = graph.run(s).to_data_frame()
        if len(g0) == 0:
            print("不存在")
            return render(request, 'forum/kg.html', {
                'status': 2,
            })
        print(g0["a.name"][0], g0["a.time"][0], g0["a.type"][0])
        return HttpResponse(json.dumps({
            'status': 1,
            'name0': g0["a.name"][0],
            'time0': g0["a.time"][0],
            'type0': g0["a.type"][0],
            'name1': g["b.name"][0],
            'name2': g["b.name"][1],
            'name3': g["b.name"][2],
            'name4': g["b.name"][3],
            'name5': g["b.name"][4],
            'type1': g["b.type"][0],
            'type2': g["b.type"][1],
            'type3': g["b.type"][2],
            'type4': g["b.type"][3],
            'type5': g["b.type"][4],

        }))
    print("刷新界面")
    return render(request, 'forum/kg.html')
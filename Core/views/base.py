"""
note
----
所有类均继承自django, 可直接使用 `from Core.views import x` 进行导入

See Also
--------
详细使用说明参见 `基于类的Django视图(官方文档)`_ , `基于类的Django视图检查器`_.

.. _基于类的Django视图检查器 : http://ccbv.co.uk
.. _基于类的Django视图(官方文档) :
    https://docs.djangoproject.com/en/1.11/topics/class-based-views/
"""
from django.views import generic
from django.contrib.auth import views, mixins, authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# AUTH VIEWS
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(views.LoginView):
    """
    用于处理用户登录的视图
    """
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'status': True})
        return JsonResponse({'status': False})


class LogoutView(views.LogoutView):
    """
    用于处理用户登出的视图
    """
    pass


# GENERIC BASE
class View(generic.View):
    """
    所有基于类的视图的基类, 只实现了请求方法检测与方法分发
    """
    pass


class RedirectView(generic.RedirectView):
    """
    用于处理重定向的视图
    """
    pass


class TemplateView(generic.TemplateView):
    """
    用于处理带有模板渲染的视图
    """
    pass


# GENERIC DETAIL
class DetailView(generic.DetailView):
    """
    用于处理单个对象细节渲染的视图
    """
    pass


# GENERIC EDIT
class CreateView(generic.CreateView):
    """
    用于处理创建某一类对象的视图
    """
    pass


class DeleteView(generic.DeleteView):
    """
    用于处理删除某一个对象的视图
    """
    pass


class UpdateView(generic.UpdateView):
    """
    用于处理更新某一个对象的视图
    """
    pass


class FormView(generic.FormView):
    """
    用于渲染表单并验证表单的视图
    """
    pass


# GENERIC LIST
class ListView(generic.ListView):
    """
    用于展示多个对象的视图
    """
    pass


# Mixins
class LoginRequiredMixin(mixins.LoginRequiredMixin):
    """
    用于验证用户登录状态的组件
    """
    pass

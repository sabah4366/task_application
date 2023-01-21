from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,FormView
from django.urls import reverse_lazy
from tasks.forms import TaskForm,RegistrationForm,LoginForm
from tasks.models import Tasks
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm


def sigin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'You must login')
            return redirect('signin')

        else:
            return fn(request,*args,**kwargs)
    return wrapper


class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self, request, *args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(self.request,'you are logged in')
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})


class SignUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")
    def form_valid(self, form):
        messages.success(self.request,"You are registered successfully ")
        return super().form_valid(form)
  
@method_decorator(sigin_required,name='dispatch')
class IndexView(TemplateView):
    template_name="index.html"

@method_decorator(sigin_required,name='dispatch')
class TaskCreateView(CreateView):
    template_name="task-add.html"
    form_class=TaskForm
    success_url=reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Task has been added")

        return super().form_valid(form)
    

    # def get(self,request,*args,**kw):
    #     form=TaskForm()
    #     return render(request,"task-add.html",{"form":form})

    # def post(self,request,*args,**kw):
    #     form=TaskForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("task-list")
    #     else:
    #         return render(request,'task-add.html',{"form":form})
@method_decorator(sigin_required,name='dispatch')
class TasksListView(ListView):
    model=Tasks 
    template_name="task-list.html"
    context_object_name="todos"

    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user)
    #if you are using under code then inherit in View class
    # def get(self,request,*args,**kw):
    #     qs=Tasks.objects.all()
    #     return render(request,"task-list.html",{"todos":qs})
@method_decorator(sigin_required,name='dispatch')
class TaskDetailView(DetailView):
    model=Tasks
    template_name="task-details.html"
    context_object_name="todo"
    #pk_url_kwarg="id"  #if you are using this variable or attribute then the urls.py has to become <int:id>

    #if you are using under code then inherit in View class
    # def get(self,request,*args,**kw):
    #     id=kw.get("pk")
    #     qs=Tasks.objects.get(id=id)
    #     return render(request,"task-details.html",{"todo":qs})
@method_decorator(sigin_required,name='dispatch')
class TaskDeleteView(View):
    def get(self,request,*args,**kw):
        id=kw.get("pk")
        Tasks.objects.get(id=id).delete()
        messages.success(self.request,'task removed successfully')
        return redirect("task-list")
@sigin_required
def signout(request,*args,**kwargs):
    logout(request)
    messages.success(request,'You are Logouted')
    return redirect('signin')
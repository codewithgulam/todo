
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView,DeleteView  , FormView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.views import LoginView ,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

#unable to understand

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks'] =  context['tasks'].filter(user=self.request.user)
        context['count'] =  context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search_area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input
       

        # print(context)
        # print(search_input)
        return context

#unable to understand


class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    # template_name = 'todoapp/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description', 'complete']
    # template_name = 'todoapp/task_form.html'
    success_url =reverse_lazy('tasks')  #it will return user to name='task' .

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self ).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description', 'complete']
    success_url =reverse_lazy('tasks')  #it will return user to name='task' .


    
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    template_name = 'todoapp/delete.html'

    success_url =reverse_lazy('tasks')  #it will return user to name='task' .


class CustomLoginView(LoginView):
    template_name = 'todoapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True


    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'todoapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url =reverse_lazy('tasks')  #it will return user to name='task' .

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage, self).form_valid(form)
    
    # it stop the logged in user to access login page
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)
    # it stop the logged in user to access login page

from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .forms import Sign_Up_Form,Login_User_Form
from django.views.generic import CreateView,View,ListView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy,reverse    
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import User_Post_Creation,User_Profile_Creation,UserUpdateForm,ProfileUpdateForm,CommentForm
from .models import Create_Post,Profile,Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
import json
from django.utils import timezone
# Create your views here.



"""Login Class View"""
class LogIn(View):
    form_classs = Login_User_Form
    template_name = 'myapp/login.html'


    def get(self,request):
        form = self.form_classs
        # print("hello")
        return render(request,self.template_name,{'login_form':form})
    

    def post(self,request):
        if request.method == 'POST':
            
            form = Login_User_Form(request,data=request.POST)
            if form.is_valid():
                usern = form.cleaned_data.get('username')
                passw = form.cleaned_data.get('password')

                user = authenticate(username=usern,password=passw)
                if user is not None:
                    login(request,user)
                    return redirect('home')
                else:
                    messages.error(request,'invalid user')
            else:
                messages.error(request,"username and password is incorrect.")

        form = Login_User_Form()
        return render(request,'myapp/login.html',{'login_form':form})



"""Sign In Class View"""
class sign_up(CreateView):
    form_class = Sign_Up_Form
    template_name = 'myapp/registration.html' 
    success_url = reverse_lazy('login')  



"""Home Class View"""
@method_decorator(login_required,name='dispatch')
class Home_Page(ListView):
    model = Create_Post
    template_name = "myapp/home.html"
    success_url = reverse_lazy('home')      

    def get_queryset(self): 
    #     # import pdb;pdb.set_trace()
    #     """Return the last five published questions."""
    #     # return Question.objects.order_by("-pub_date")[:5]
        return Create_Post.objects.order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm() # Inject CommentForm
        return context


"""Like and Dislike Function"""
@login_required
def like(request):
    if request.POST.get('action') == 'post':
        # print(request.POST)
        # print("chlra hai")
        result = ''
        # print("result:-",result)
        id = int(request.POST.get('postid'))
        # print(id)
        posts = get_object_or_404(Create_Post, id=id)
        # print(posts)
        if posts.likes.filter(id=request.user.id).exists():
            posts.likes.remove(request.user)
            posts.news_likes_count -= 1
            checker = 0
            if posts.news_likes_count <= 0:
                posts.news_likes_count = 0
            result = posts.news_likes_count
            posts.save()
        else:
            posts.likes.add(request.user)
            posts.news_likes_count += 1
            checker = 1
            result = posts.news_likes_count
            posts.save()
        # ctx = {'result': result}

        info = {
            "check" :checker,
            'result': result
        }

        return JsonResponse(info)
        # return HttpResponse(json.dumps(ctx), content_type='application/json')
        

"""Detail View for showing one post on single page"""
class Detail_Post(LoginRequiredMixin,DetailView):
    model = Create_Post
    template_name = 'myapp/detail_post.html'
    context_object_name = 'detaildata'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm() # Inject CommentForm
        return context
    

"""Add comment on the post of detail page"""
@login_required
def comment(request, pk):
    print(request)
    import pdb;pdb.set_trace()
    post = get_object_or_404(Create_Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            form.instance.name = request.user
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('detailpost', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'myapp/detail_post.html', {'form': form})


"""Add comment on the posts of Home page"""  
@login_required
def AddCommentHome(request, pk):
    post = get_object_or_404(Create_Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            form.instance.name = request.user
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'myapp/home.html', {'form': form})



"""Display User Profile Class View"""
class User_Profile(LoginRequiredMixin,ListView):
    template_name = 'myapp/user_profile.html'
    model = Profile
    success_url = reverse_lazy('profile')
    context_object_name = 'profiledata'

    def get_queryset(self):
         return Profile.objects.filter(user_id = self.request.user.id )
    


"""Create Profile"""
class Create_Profile(LoginRequiredMixin,CreateView):
    template_name = "myapp/create_profile.html"
    form_class = User_Profile_Creation 
    model = Profile
    success_url = reverse_lazy('profile')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



"""Update Profile"""
class Update_Profile(LoginRequiredMixin,UpdateView):
    model = Profile
    fields = ["image","bio"]
    template_name = 'myapp/update_profile.html'
    success_url = reverse_lazy('profile')


"""Delete Profiile"""
class Delete_Profile(LoginRequiredMixin,DeleteView):
    model = User
    template_name = 'myapp/delete_profile.html'
    success_url = reverse_lazy('login')



"""Create User Post Class View"""
@method_decorator(login_required,name='dispatch')
class create_user_post(CreateView):
    form_class = User_Post_Creation
    model = Create_Post
    template_name = "myapp/create_post.html"
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
 


"""Display Logged In User Post Class View"""   
@method_decorator(login_required,name='dispatch')
class MyPost(ListView):
    model = Create_Post
    template_name = 'myapp/user_post.html'
    context_object_name = 'userpost'
    
    def get_queryset(self):
         return Create_Post.objects.filter(user_id = self.request.user.id )



"""Update User Post Class View"""   
@method_decorator(login_required,name='dispatch')
class UpdatePost(UpdateView):
    # import pdb;pdb.set_trace()
    model = Create_Post
    fields = ["post_img","caption"]
    template_name = 'myapp/update_post.html'
    success_url = reverse_lazy('mypost')

    

"""Delete User Post Class View"""
@method_decorator(login_required,name='dispatch')
class DeletePost(DeleteView):
    model = Create_Post
    success_url = reverse_lazy('mypost')
    template_name = 'myapp/delete_post.html'


# class AddComment(CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = "myapp/detail_post.html"
#     success_url = reverse_lazy('/')

#     def form_valid(self, form):
#         form.instance.name = self.request.user
#         form.instance.post = self.kwargs.get("id")
#         return super().form_valid(form)



"""Logout Class View"""
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('home')
    
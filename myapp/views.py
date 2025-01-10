from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .forms import Sign_Up_Form,Login_User_Form
from django.views.generic import CreateView,View,ListView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy,reverse    
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import User_Post_Creation,User_Profile_Creation,UserUpdateForm,ProfileUpdateForm
from .models import Create_Post,Profile
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
                    messages.success(request,"You Successfully Loged in.")
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
        # import pdb;pdb.set_trace()
        """Return the last five published questions."""
        # return Question.objects.order_by("-pub_date")[:5]
        # return Create_Post.objects.all().order_by("-date")


def like_post(request):
    data = json.loads(request.body)
    print(data)
    # import pdb;pdb.set_trace()    
    id = data["id"]
    post = Create_Post.objects.get(id=id)
    checker = None
    print("django Views code")
    
    if request.user.is_authenticated:
        
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            checker = 0
            
            
        else:
            post.likes.add(request.user)
            checker = 1
    
    likes = post.likes.count()
    
    info = {
        "check": checker,
        "num_of_likes": likes
    }
    
    return JsonResponse(info, safe=False)

@login_required
def like(request):
    if request.POST.get('action') == 'post':
        print(request.POST)
        # print("chlra hai")
        result = ''
        print("result:-",result)
        id = int(request.POST.get('postid'))
        print(id)
        posts = get_object_or_404(Create_Post, id=id)
        print(posts)
        if posts.likes.filter(id=request.user.id).exists():
            posts.likes.remove(request.user)
            posts.news_likes_count -= 1
            if posts.news_likes_count <= 0:
                posts.news_likes_count = 0
            result = posts.news_likes_count
            posts.save()
        else:
            posts.likes.add(request.user)
            posts.news_likes_count += 1
            result = posts.news_likes_count
            posts.save()
        # ctx = {'result': result}
        return JsonResponse({'result': result})
        # return HttpResponse(json.dumps(ctx), content_type='application/json')
        

class Detail_Post(LoginRequiredMixin,DetailView):
    model = Create_Post
    template_name = 'myapp/detail_post.html'
    context_object_name = 'detaildata'



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
    model = Create_Post
    template_name = 'myapp/update_post.html'
    fields = ["caption"]
    success_url = reverse_lazy('mypost')



"""Delete User Post Class View"""
@method_decorator(login_required,name='dispatch')
class DeletePost(DeleteView):
    model = Create_Post
    success_url = reverse_lazy('mypost')
    template_name = 'myapp/delete_post.html'



# def PostLike(request,pk):
#     post = get_object_or_404(Create_Post,id = request.POST.get('post_id'))
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)

#     return HttpResponseRedirect(reverse('detailpost', args=[str(pk)]))




    # def get_context_data(self, **kwargs):
    #     # import pdb;pdb.set_trace()
    #     data = super().get_context_data(**kwargs)

    #     likes_connected = get_object_or_404(Create_Post, id=self.kwargs['pk'])
    #     liked = False
    #     if likes_connected.likes.filter(id=self.request.user.id).exists():
    #         liked = True
    #     data['number_of_likes'] = likes_connected.number_of_likes()
    #     data['post_is_liked'] = liked
    #     return data
    


"""Logout Class View"""
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('home')
    
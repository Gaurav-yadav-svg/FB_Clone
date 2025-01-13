from django.urls import path
from .views import sign_up,LogIn,Logout,Home_Page,create_user_post,MyPost,UpdatePost,DeletePost,User_Profile,Create_Profile,Update_Profile,Delete_Profile,Detail_Post 
from .import views
from django.contrib.auth.decorators import login_required


urlpatterns = [

    path('',Home_Page.as_view(),name='home'),
    path('register/',sign_up.as_view(),name='signup'),
    path('accounts/login/',LogIn.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('createpost/',create_user_post.as_view(),name='createpost'),
    path('mypost/',MyPost.as_view(),name='mypost'),#detail_View    
    path('<int:pk>/updatepost/',UpdatePost.as_view(),name='updatepost'),
    path('<int:pk>/deletepost/',DeletePost.as_view(),name='deletepost'),
    path('profile/',User_Profile.as_view(),name='profile'),
    path('createprofile/',Create_Profile.as_view(),name='createprofile'),
    path('<int:pk>/updateprofile/',Update_Profile.as_view(),name='updateprofile'),
    path('<int:pk>/deleteprofile/',Delete_Profile.as_view(),name='deleteprofile'),
    path('<int:pk>/detailpost/',Detail_Post.as_view(),name='detailpost'),
    path("like/", views.like, name="like"),
    
]
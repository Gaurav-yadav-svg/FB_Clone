from django.urls import path
from .views import sign_up,LogIn,Logout,Home_Page,create_user_post,MyPost,UpdatePost,DeletePost,User_Profile,Create_Profile,Update_Profile,Delete_Profile,Detail_Post,MyPasswordChangeView,MyPasswordResetDoneView
from .import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('',Home_Page.as_view(),name='home'),
    path('accounts/signup/',sign_up.as_view(),name='signup'),
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
    path("comment/",views.comment_create,name = "comm"),
    # path("homecomment/<int:pk>",views.AddCommentHome,name = "homecomment"),
    path("delete-comment/",views.Delete_Comment,name = "delcomment"),
    # path('addcomment/<int:pk>',AddComment.as_view(),name='comm'),

    path("reset_password/",auth_views.PasswordResetView.as_view(template_name = "myapp/password_reset.html"),name = "reset_password"),

    path("reset_password_sent/",auth_views.PasswordResetDoneView.as_view(template_name = "myapp/password_reset_sent.html"),name = "password_reset_done"),

    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name = "myapp/password_reset_form.html"),name = "password_reset_confirm"),

    path("reset_password_complete/",auth_views.PasswordResetCompleteView.as_view(template_name = "myapp/password_reset_done.html"),name = "password_reset_complete"),


    path("change-password/",MyPasswordChangeView.as_view(), name = "password-change-view"),
    path("change-password/done/",MyPasswordResetDoneView.as_view(),name = "password-change-done-view"),   
] 
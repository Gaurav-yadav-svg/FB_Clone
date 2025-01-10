from django.contrib import admin
from .models import Create_Post
# Register your models here.


@admin.register(Create_Post)
class show_list(admin.ModelAdmin):
    list_display = ('id','post_img','caption','user_id')


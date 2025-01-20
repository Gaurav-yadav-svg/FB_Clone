from django.contrib import admin
from .models import Create_Post,Comment
# Register your models here.


@admin.register(Create_Post)
class show_list(admin.ModelAdmin):
    list_display = ('id','post_img','caption','user_id')

admin.site.register(Comment)
from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name = 'home'),
    path('detail_blog/<int:pk>',detail_blog,name = 'detail_blog'),
    path('edit_blog/<int:pk>',edit_blog,name = 'edit_blog'),
    path('delete_blog/<int:pk>',delete_blog,name = 'delete_blog'),
    path('tag/<slug:tag_slug>',get_tag,name = 'get_tag'),
    path('comment',save_comment,name = 'comment'),
    path('comment_delete',delete_comment,name = 'comment_delete'),
    path('create_post',create_blog,name = 'create_post'),
    path('about',about,name = 'about'),
    # path('update_comment',update_comment,name = 'update_comment'),
]
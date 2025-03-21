
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    
    path('profile/', profile, name="profile"),
    path('profile/edit/', edit_profile, name='edit_profile'),

    # --------------admin---------------

    path('custom_admin-login/', admin_login, name='admin_login'),
    path('custom_admin-logout/', admin_logout, name='admin_logout'),
    path('custom-admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('custom-admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('custom-admin-user-detail/<int:user_id>/', admin_user_detail, name='admin-user-detail'),
    path('custom-admin-users/', admin_user_list, name='admin-users'),
    path('blogs/', blog_list, name='blog-list'),
    path('blogs/<int:blog_id>/', blog_detail, name='blog-detail'),
    path('add-blog/', add_blog, name="add-blog"),
    path('custom-admin/manage-blogs/', manage_blogs, name='manage-blogs'),
    path('custom-admin/update-blog/<int:blog_id>/', update_blog, name='update-blog'),
    path('custom-admin/delete-blog/<int:blog_id>/', delete_blog, name='delete-blog'),

]

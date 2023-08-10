from django.urls import path
from .views import (
    login_view,
    logout_view,
    register_view,
    homepage,
    create_group,
    group_detail,
    delete_member,
    run_secret_santa,
    request_join_group,
    accept_request,
    reject_request,
    search_groups
)

urlpatterns = [
    # Authentication routes
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    # Home and search routes
    path('home/', homepage, name='homepage'),
    path('search/', search_groups, name='search_groups'),

    # Group management routes
    path('create_group/', create_group, name='create_group'),
    path('group/<int:group_id>/', group_detail, name='group_detail'),
    path('delete_member/<int:member_id>/', delete_member, name='delete_member'),
    path('run_secret_santa/<int:group_id>/', run_secret_santa, name='run_secret_santa'),
    path('search_results/', search_groups, name='search_groups'),

    # Group join request
    path('group/<int:group_id>/join/', request_join_group, name='request_join_group'),
    path('accept_request/<int:request_id>/', accept_request, name='accept_request'),
    path('reject_request/<int:request_id>/', reject_request, name='reject_request'),
]

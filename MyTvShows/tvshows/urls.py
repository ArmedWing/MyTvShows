from django.urls import path, include
from MyTvShows.tvshows import views
from MyTvShows.tvshows.views import index, \
    delete_profile, RegisterView, LoginUserView, LogoutUserView, profile_info, update_profile, \
    create_reply, UsersInfoListView, CreateThreadView, ThreadDeleteView, DeleteReplyView

urlpatterns = (
    path('', index, name='index'),

    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('users-info/', UsersInfoListView.as_view(), name='users_info'),
    path('create-thread/', CreateThreadView.as_view(), name='create_thread'),
    path('create-reply/<int:thread_id>/', create_reply, name='create_reply'),
    path('delete_reply/<int:reply_id>/', DeleteReplyView.as_view(), name='delete_reply'),
    path('thread/', views.thread_detail, name='thread_detail'),
    path('thread/view_thread/<int:thread_id>/', views.view_thread, name='view_thread'),
    path('delete_thread/<int:thread_id>/', ThreadDeleteView.as_view(), name='delete_thread'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),


    path('profile/', include([
        path('details/', profile_info, name='details_profile'),
        path('delete/', delete_profile, name='delete_profile'),
        path('update/', update_profile, name='update_profile'),
    ])),
)

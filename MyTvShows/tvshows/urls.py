from django.urls import path, include
from MyTvShows.tvshows import views
from MyTvShows.tvshows.views import index, delete_show, \
    delete_profile, RegisterView, LoginUserView, LogoutUserView, profile_info, update_profile, AddShowReview, \
    AddShowView, ShowDetailsView, users_Info, shows_info, create_thread, create_reply, EditShowView

urlpatterns = (
    path('', index, name='index'),

    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('users-info/', users_Info, name='users_info'),
    path('shows-info/', shows_info, name='shows_info'),
    path('create-thread/', create_thread, name='create_thread'),
    path('create-reply/<int:thread_id>/', create_reply, name='create_reply'),
    path('thread/', views.thread_detail, name='thread_detail'),
    path('thread/view_thread/<int:thread_id>/', views.view_thread, name='view_thread'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),


    path('show/', include([
        path('add/', AddShowView.as_view(), name='add_show'),
        path('details/<int:pk>/', ShowDetailsView.as_view(), name='details_show'),
        path('edit/<int:pk>/', EditShowView.as_view(), name='edit_show'),
        path('delete/<int:pk>/', delete_show, name='delete_show'),
        path('increase_counter/<int:pk>/', views.IncreaseCounter, name='Increase-Counter'),
        path('review/<int:pk>/', AddShowReview.as_view(), name='add_review'),
        path('delete_review/<int:pk>/', views.DeleteReview, name='DeleteReview'),


    ])),
    path('profile/', include([
        path('details/', profile_info, name='details_profile'),
        path('delete/', delete_profile, name='delete_profile'),
        path('update/', update_profile, name='update_profile'),
    ])),
)
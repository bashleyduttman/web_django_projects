from django.urls import path
from new import  views
urlpatterns=[
    path('',views.main,name="main"),
    path('login-user',views.login_user,name="login-user"),
    path('logout-user',views.logout_user,name="logout-user"),
    path("post",views.post_user,name='post'),
    path('delete_post/<int:postId>/', views.delete_post, name='delete_post'),
    path("change",views.change_password,name="change"),
    path("newpassword",views.new_fpassword,name="new_password"),
    path("comments/<int:postId>/",views.comments,name="comments"),
    path("profile/<int:profId>/",views.profiles,name="profile"),
    path("followers_inc/<int:user_id>/",views.followers_increase,name='followers_increament'),
    path("signup-user",views.signup,name="signup-user"),
    path("search",views.search_post,name="search"),
    path('chat_room/<int:otheruser>/',views.start_or_create_chat,name="chat_room"),
    path("chat/room/message/<int:room_id>/",views.chat_room,name="chat_room_message"),
    path('chat/room/list',views.chat_room_list,name="chat_room_list")
]
from django.urls import path
# para user olvide contraseña, user cambiar contraseña
from django.contrib.auth import views as auth_views



from .views import (
    home_view, list_view_bookings, search_view_bookings, detail_view_bookings, create_booking_view,
    list_room_view, create_room_view, delete_room_view, update_room_view, search_room_view, detail_room_view,
    # Vistas basadas en clases "VBC"
    CommentListView, CommentCreateView, CommentDetailView, CommentUpdateView, CommentDeleteView,MyCommentsListView,
    RoomListView, RoomCreateView, RoomDetailView, RoomUpdateView, RoomDeleteView,
    #user
    user_creation_view, user_login_view, user_logout_view, avatar_view, UserUpdateView, UserAboutDetailView,
)


urlpatterns = [
    path("", home_view, name="booking_home"),
    path("bookings/list/", list_view_bookings, name="booking_list"),
    path("bookings/detail/<booking_id>", detail_view_bookings, name="booking_detail"),
    path("booking/create/", create_booking_view, name="bookings_create"),
    # path("booking/search/<nombre_de_usuario>", search_view_bookings, name="booking_search_"),
    path("booking/search/", search_view_bookings, name="booking_search"),

    # comentarios
    path('comment/list/', CommentListView.as_view(), name="comment_list"),
    path('comment/list/my-comments', MyCommentsListView.as_view(), name="comment_my_comments"),
    path('comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/detail/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),

    # CRUD Rooms
    path("room/list/", list_room_view, name="room_list"),
    path("room/create/", create_room_view, name="room_create"),
    path("room/detail/<room_id>", detail_room_view, name="room_detail"),
    path("room/delete/<room_id>", delete_room_view, name="room_delete"),
    path("room/update/<room_id>", update_room_view, name="room_update"),
    path("room/search/", search_room_view, name="room_search"),

    # Vistas basadas en clases "VBC"
    path('room/vbc/list', RoomListView.as_view(), name='vbc_room_list'),
    path('room/vbc/create/', RoomCreateView.as_view(), name='vbc_room_create'),
    path('room/vbc/<int:pk>/detail', RoomDetailView.as_view(), name='vbc_room_detail'),
    path('room/vbc/<int:pk>/update/', RoomUpdateView.as_view(), name='vbc_room_update'),
    path('room/vbc/<int:pk>/delete/', RoomDeleteView.as_view(), name='vbc_room_delete'),

    # users
    path("create-user/", user_creation_view, name="create_user"),
    path("login/", user_login_view, name="login"),
    path("logout/", user_logout_view, name="logout"),
    path('update-perfil/', UserUpdateView.as_view(), name='update_perfil'),
    path('about/', UserAboutDetailView, name='user_about'),

    path('avatar/add/', avatar_view, name='avatar_add'),

    # URL para la recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
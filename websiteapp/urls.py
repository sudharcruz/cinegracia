from django.contrib import admin
from django.urls import path
from .import views
from .views import *
from register.views import logout
from  django.contrib.auth import views as auth_views

app_name = "websiteapp"
app_name = "toprating"
app_name = "register"
urlpatterns = [
    path('',views.index, name='index'),
    path('register/',views.register, name='register'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',custom.as_view(),name='password_reset_complete'),
    path('password_change/',auth_views.PasswordChangeView.as_view()),
    path('favouritelist/',views.favlist,name='favlist'),
    path('deleterating/<int:deleteid>/',views.ratingdelete,name='rating-delete'),
    path('like/<str:movieid>/<int:id>/',views.addlike,name='addlike'),
    path('search',views.search,name='search'),
    path('collection-list/<int:collection_id>/',views.display_collection_movies,name='collection'),
    path('discover/<str:genre_name>/<str:genreid>/<str:section>/',views.discover,name='discover-genre'),
    path('register/',views.register, name='register'),
    path('logout/',views.logout,name='logout'),
    path('myprofile/<int:id>/',views.myprofile,name='myprofile'),
    #path('info/<int:user_id>/update/',views.update_profile,name='info-update'),
    path('createprofile/<int:id>/',createprofile.as_view(),name='createprofile'),
    path('profile/<int:pk>/update/',profileupdateview.as_view(),name='update-profile'),
    path('favouritelist/',views.favlist,name='favlist'),
    path('allshows/<str:section>/<int:id>/',views.allshows,name='allshows'),
    path('<str:movieid>/<int:id>/',MovieDetailView.as_view(),name='movie-details'),
    #path('<str:movieid>/tmdb/',MovieDetailView.as_view(),name='movie-details'),
    path('add-comment/<str:movieid>/<int:id>/',views.post_comment,name='add-comment'),
    path('add-Rating/<str:movieid>/<int:id>/',views.post_rating,name='add-rating'),
    path('delete-Rating/<str:movieid>/<int:id>/<int:did>/',views.ratedelete,name='delete-rating'),
    path('delete-comment/<str:movieid>/<int:id>/<int:did>/',views.comment_delete,name='delete-comment'),
    path('deletecomment/<int:delid>/<int:id>/',views.commentdelete,name='comment-delete'),
    path('add-to-favourite/<str:movieid>/<int:id>/',views.addfavourite_tmdb,name='add-to-favourite'),
    path('addfavourite/<str:movieid>/<int:id>/',views.addfavourite,name='addfavourite'),
    path('register/',views.register, name='register'),
    path('register/login/',views.login,name='login'),
    path('toprating/<str:movd>/',views.toprating,name='toprating'),
]

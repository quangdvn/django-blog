from django.urls import path
from . import views

urlpatterns = [
    path(route="",
         view=views.StartingPageView.as_view(),
         name='starting-page'),
    path(route="posts",
         view=views.AllPostsView.as_view(),
         name='posts'),
    path(route="posts/<slug:slug>",
         view=views.PostDetailView.as_view(),
         name='post-detail'),
    path("readlater",
         views.ReadLaterView.as_view(),
         name="readlater")
]

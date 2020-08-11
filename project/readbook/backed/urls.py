from django.urls import path
from rest_framework import routers
from django.conf.urls import url

from rest_framework.authtoken import views
from .views import *

app_name='backed'
urlpatterns=[
    # url('login/', views.obtain_auth_token),
    url('login/', CustomAuthToken.as_view()),
    url('register/', RegisterAPIView.as_view()),
    url('account/', AccountDetailAPIView.as_view()),
    url('add_to_collection/', AddBookToCollectionAPIView.as_view()),
    url('collection/', CreateCollectionAPIView.as_view()),
    url('add_book_to_db/', AddBookAPIView.as_view()),
    url('review/', ReviewAPIView.as_view()),
    url('rating/', RatingAPIView.as_view()),
    url('likeit/', LikeItAPIView.as_view()),
    url('set_goal/', MonthlyGoalAPIView.as_view()),
    url('bookdetail/', BookDetailPageAPIView.as_view()),
    url('searchbook/', SearchBookAPIView.as_view()),
    # url(r'filtersearchbook/$', FilterSearchBookAPIView.as_view()),
    url('filter/', FilterSearchBookAPIView.as_view()),
    url('mainpagerec/', MainPageRecAPIView.as_view()),
    url('recommend/', UserBaseRecAPIView.as_view()),
    url('historyrecord/', HistoryAPIView.as_view()),
    url('historyrecord/', HistoryAPIView.as_view()),
    url('test/', TestAPIView.as_view()),

]
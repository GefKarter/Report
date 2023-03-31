from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, CategoryListView, subscriptions, IndexView

urlpatterns = [
   path('', PostList.as_view(), name = 'post_list'),
   path('<int:pk>', PostDetail.as_view(), name = 'post_detail'),
   path('create/', PostCreate.as_view(), name = 'post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name = 'post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('subscriptions/', subscriptions, name = 'subscriptions'),
   path('', IndexView.as_view()),
]
from django.urls import path, include

from .views import NotificationList, NotificationDetail, NotificationSearch, NotificationCreate, NotificationUpdate, \
    NotificationDelete, ResponsesCreate, ResponsesUpdate, ResponsesDelete, response_accept, response_reject

app_name = 'Board'

urlpatterns = [
    path('', NotificationList.as_view(), name='notification_list'),
    path('notification_detail/<int:pk>', NotificationDetail.as_view(), name='notification_detail'),
    path('search/', NotificationSearch.as_view(), name='notification_search'),
    path('create/', NotificationCreate.as_view(), name='notification_create'),
    path('notification_detail/<int:pk>/update', NotificationUpdate.as_view(), name='notification_update'),
    path('notification_detail/<int:pk>/delete', NotificationDelete.as_view(), name='notification_delete'),
    path('notification_detail/<int:pk>/responses/create', ResponsesCreate.as_view(), name='responses_create'),
    path('notification_detail/<int:notification_id>/responses/update/<int:response_id>', ResponsesUpdate.as_view(),
         name='responses_update'),
    path('notification_detail/<int:notification_id>/responses/delete/<int:response_id>', ResponsesDelete.as_view(),
         name='responses_delete'),
    path('notification_detail/<int:notification_id>/responses/accept/<int:response_id>', response_accept,
         name='response_accept'),
    path('notification_detail/<int:notification_id>/responses/reject/<int:response_id>', response_reject,
         name='response_reject'),

]

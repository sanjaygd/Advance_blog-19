from django.urls import path

from .views import comment_thread

app_name = 'comments'
urlpatterns = [
    path('<int:id>/',comment_thread, name='thread'),
    # path('delete/<int:id>/',post_delete, name='post_delete')
]

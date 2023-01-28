from django.urls import path
from solo.views import index

app_name='solo'
urlpatterns = [
    path('', index, name='index'),
]
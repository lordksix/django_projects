from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
app_name = 'hello'
urlpatterns = [
    path('', views.home, name='home'),
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
urlpatterns += staticfiles_urlpatterns()
#path('', TemplateView.as_view(template_name='gview/main.html')),
#from django.views.generic import TemplateView
#ya no necesitaria agregar a views.py
#you must you as_view() when using clases
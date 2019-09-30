
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name = "Hello World"),
    path('predict/', views.predict_req, name='Predict'),
    path('add/', views.add, name='Add document')
]

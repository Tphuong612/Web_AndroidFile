# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.index),
#     path('', views.predict),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),  # Đảm bảo có dấu gạch chéo ở cuối
]

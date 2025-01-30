from django.urls import path
from .views import PolicyViewList, PolicyViewDetail

urlpatterns = [
    path('policies/', PolicyViewList.as_view(), name='policy-list'),
    path('policies/<int:pk>/', PolicyViewDetail.as_view(), name='policy-detail'),
]   


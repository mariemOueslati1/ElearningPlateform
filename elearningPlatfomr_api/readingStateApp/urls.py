# urls.py
from django.urls import path
from .views import ReadingStateView , ListReadingStatesView

urlpatterns = [
    path('reading/add/<int:material_id>/', ReadingStateView.as_view(), name='add-reading'),
    path('reading/list/', ListReadingStatesView.as_view(), name='list-reading-states'),
]

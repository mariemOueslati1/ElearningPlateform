# urls.py
from django.urls import path
from .views import AddInteractionView , ListInteractionsView

urlpatterns = [
    path('interactions/add/<int:material_id>/<str:interaction_type>/', AddInteractionView.as_view(), name='add-interaction'),
    path('interactions/interationList/', ListInteractionsView.as_view(), name='list-interaction'),

]

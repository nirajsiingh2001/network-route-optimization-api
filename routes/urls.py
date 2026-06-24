from django.urls import path
from . views import AddNodeView,AddEdgeView,ShortestRouteView,RouteHistoryView

urlpatterns = [
    path('nodes/', AddNodeView.as_view(), name='add-node'),
    path('edges/', AddEdgeView.as_view(), name='add-edge'),
    path('routes/shortest/', ShortestRouteView.as_view(), name='shortest-route'),
    path('routes/history/', RouteHistoryView.as_view(), name='route-history'),
]

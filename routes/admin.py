from django.contrib import admin
from .models import Node, Edge, RouteHistory

admin.site.register(Node)
admin.site.register(Edge)
admin.site.register(RouteHistory)

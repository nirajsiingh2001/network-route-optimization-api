from django.db import models
from django.core.exceptions import ValidationError

class Node(models.Model):
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Edge(models.Model):
    source=models.ForeignKey(Node,on_delete=models.CASCADE,
                             related_name='outgoing_edges')
    destination=models.ForeignKey(Node,on_delete=models.CASCADE,
                                  related_name='incoming_edges')
    latency=models.FloatField()

    def clean(self):
        if self.source == self.destination:
            raise ValidationError("Source and destination cannot be the same.") 
        if self.latency <= 0:
            raise ValidationError("Latency must be greater than 0.")
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['source', 'destination'], name='unique_edge')
        ]

    def __str__(self):
        return f"{self.source} -> {self.destination} (Latency: {self.latency})"
    

class RouteHistory(models.Model):
    source=models.ForeignKey(Node,on_delete=models.CASCADE,
                             related_name='route_source_history')
    destination=models.ForeignKey(Node,on_delete=models.CASCADE,
                                  related_name='route_destination_history')
    total_latency=models.FloatField()
    path=models.JSONField()
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.source} -> {self.destination}"
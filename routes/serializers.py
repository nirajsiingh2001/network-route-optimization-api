from rest_framework import serializers
from .models import Node, Edge, RouteHistory

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name']

class EdgeSerializer(serializers.ModelSerializer):
    source=serializers.SlugRelatedField(queryset=Node.objects.all(),
                                         slug_field='name')
    destination=serializers.SlugRelatedField(queryset=Node.objects.all(), 
                                             slug_field='name')
    def validate(self, data):
        if data['source'] == data['destination']:
            raise serializers.ValidationError(
                "Source and destination cannot be the same."
            )

        if data['latency'] <= 0:
            raise serializers.ValidationError(
                "Latency must be greater than 0."
            )

        return data
    class Meta:
        model = Edge
        fields = ['id', 'source', 'destination', 'latency']

class RouteHistorySerializer(serializers.ModelSerializer):
    source=serializers.CharField(source='source.name')
    destination=serializers.CharField(source='destination.name')
    class Meta:
        model = RouteHistory
        fields = ['id', 'source', 'destination', 'total_latency', 'path', 'created_at']

class ShortestRouteSerializer(serializers.Serializer):
    source = serializers.CharField()
    destination = serializers.CharField()
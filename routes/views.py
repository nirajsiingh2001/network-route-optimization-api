from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Node, Edge, RouteHistory
from .serializers import NodeSerializer, EdgeSerializer, RouteHistorySerializer, ShortestRouteSerializer
import heapq
class AddNodeView(APIView):
    def post(self, request):
        serializer = NodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddEdgeView(APIView):
    def post(self,request):
        serializer=EdgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ShortestRouteView(APIView):

    def post(self, request):

        serializer = ShortestRouteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        source_name = serializer.validated_data['source']
        destination_name = serializer.validated_data['destination']

        try:
            source = Node.objects.get(name=source_name)
            destination = Node.objects.get(name=destination_name)

            edges = Edge.objects.all()

            graph = {}

            for edge in edges:

                if edge.source.name not in graph:
                    graph[edge.source.name] = []

                graph[edge.source.name].append(
                    (edge.destination.name, edge.latency)
                )

            if destination.name not in graph:
                graph[destination.name] = []

            distances = {}
            previous = {}

            for node in graph:
                distances[node] = float('inf')
                previous[node] = None

            distances[source.name] = 0

            priority_queue = [(0, source.name)]

            while priority_queue:

                current_distance, current_node = heapq.heappop(priority_queue)

                if current_node == destination.name:
                    break

                for neighbor, latency in graph[current_node]:

                    distance = current_distance + latency

                    if distance < distances[neighbor]:

                        distances[neighbor] = distance
                        previous[neighbor] = current_node

                        heapq.heappush(
                            priority_queue,
                            (distance, neighbor)
                        )

            if distances[destination.name] == float('inf'):
                return Response(
                    {
                        "error": f"No path exists between {source.name} and {destination.name}"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            path = []

            current = destination.name

            while current is not None:
                path.append(current)
                current = previous[current]

            path.reverse()

            RouteHistory.objects.create(
                source=source,
                destination=destination,
                total_latency=distances[destination.name],
                path=path
            )

            return Response(
                {
                    "total_latency": distances[destination.name],
                    "path": path
                },
                status=status.HTTP_200_OK
            )

        except Node.DoesNotExist:
            return Response(
                {"error": "Invalid node name"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

class RouteHistoryView(APIView):
    def get(self,request):
        history=RouteHistory.objects.all().order_by('-created_at')
        serializer=RouteHistorySerializer(history,many=True)
        return Response(serializer.data)
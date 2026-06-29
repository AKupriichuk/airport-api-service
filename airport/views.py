from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Crew,
    Flight,
    Order,
)
from airport.serializers import (
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirportSerializer,
    RouteSerializer,
    RouteDetailSerializer,
    CrewSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    OrderSerializer,
    OrderListSerializer,
)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    # Оптимізуємо: підтягуємо тип літака одним SQL JOIN-запитом
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")

    # Якщо користувач просто дивиться список або конкретний маршрут — показуємо деталі.
    # Якщо створює новий (POST) — використовуємо базовий серіалізатор.
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RouteDetailSerializer
        return RouteSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related(
                "route__source", "route__destination", "airplane"
            ).prefetch_related("crew")

        if self.action == "retrieve":
            queryset = queryset.prefetch_related("tickets")

        def get_queryset(self):
            queryset = self.queryset

            source = self.request.query_params.get("source")
            destination = self.request.query_params.get("destination")
            date = self.request.query_params.get("date")

            if source:
                queryset = queryset.filter(route__source__name__icontains=source)
            if destination:
                queryset = queryset.filter(route__destination__name__icontains=destination)
            if date:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                queryset = queryset.filter(departure_time__date=date_obj)

            return queryset.distinct()

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("tickets__flight__route")
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

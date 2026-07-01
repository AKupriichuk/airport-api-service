from django.urls import path, include
from rest_framework.routers import DefaultRouter
from airport.views import (
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    RouteViewSet,
    CrewViewSet,
    FlightViewSet,
    OrderViewSet,
)

router = DefaultRouter()
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"

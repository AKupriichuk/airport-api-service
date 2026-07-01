from rest_framework import serializers
from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Crew,
    Flight,
    Order,
    Ticket,
)
from django.db import transaction
from rest_framework.exceptions import ValidationError


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class FlightListSerializer(FlightSerializer):
    route = serializers.StringRelatedField()
    airplane = serializers.StringRelatedField()
    crew = serializers.StringRelatedField(many=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


    def validate(self, attrs):
        data = super().validate(attrs)
        flight = attrs["flight"]
        airplane = flight.airplane


        if not (1 <= attrs["row"] <= airplane.rows):
            raise ValidationError(
                {"row": f"Row number must be in range from 1 to {airplane.rows}."}
            )
        if not (1 <= attrs["seat"] <= airplane.seats_in_row):
            raise ValidationError(
                {"seat": f"Seat number must be in range from 1 to {airplane.seats_in_row}."}
            )


        ticket_taken = Ticket.objects.filter(
            flight=flight, row=attrs["row"], seat=attrs["seat"]
        ).exists()
        if ticket_taken:
            raise ValidationError({"seat": "This seat is already taken for this flight."})

        return data


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")


    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(read_only=True)
    airplane = AirplaneSerializer(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)
    taken_places = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "taken_places"
        )


    def get_taken_places(self, obj):
        return [
            {"row": ticket.row, "seat": ticket.seat}
            for ticket in obj.tickets.all()
        ]

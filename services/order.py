from django.db import transaction
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model

User = get_user_model()


@transaction.atomic
def create_order(tickets, username, date=None):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError("User does not exist")

    order_kwargs = {"user": user}
    if date:
        parsed_date = parse_datetime(date)
        if not parsed_date:
            raise ValueError("Invalid date format")
        order_kwargs["created_at"] = parsed_date

    order = Order.objects.create(**order_kwargs)

    for ticket_data in tickets:
        movie_session_id = ticket_data["movie_session"]
        try:
            movie_session = MovieSession.objects.get(id=movie_session_id)
        except MovieSession.DoesNotExist:
            raise ValueError(f"Movie session {movie_session_id} does not exist")

        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order



def get_orders(username=None):
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()


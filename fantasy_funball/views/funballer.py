from typing import Union

from django.core.handlers.wsgi import WSGIRequest
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import FunballerNotFoundError
from fantasy_funball.models import Funballer


class FunballerViewMixin:
    @staticmethod
    def _get_funballer_by_id(id: int) -> Union[Funballer, None]:
        try:
            return Funballer.objects.get(id=id)
        except Funballer.DoesNotExist:
            raise FunballerNotFoundError(f"Funballer with id {id} not found")


class FunballerView(APIView, FunballerViewMixin):
    """Viewset to handle funballers"""

    def post(self, request: WSGIRequest) -> Response:
        """Add a funballer to postgres db"""
        funballer = Funballer(**request.data)
        funballer.save()

        # Convert to json for output
        formatted_funballer = model_to_dict(funballer)

        return Response(
            status=status.HTTP_201_CREATED,
            data=formatted_funballer,
        )

    def get(self, request: WSGIRequest) -> Response:
        """Retrieve all funballers from postgres db"""
        funballers = Funballer.objects.all()

        formatted_funballers = [model_to_dict(funballer) for funballer in funballers]

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_funballers,
        )


class SingleFunballerView(APIView, FunballerViewMixin):
    def get(self, request: WSGIRequest, id: int) -> Response:
        """Retrieve a funballer from postgres db"""
        funballer = self._get_funballer_by_id(id=id)

        # Convert to json for output
        formatted_funballer = model_to_dict(funballer)

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_funballer,
        )

    def patch(self, request: WSGIRequest, id: int) -> Response:
        """Update a funballer in postgres db"""
        funballer = self._get_funballer_by_id(id=id)

        # Parse update payload
        update_payload = [
            {"field": str(key), "value": str(value)}
            for key, value in request.data.items()
        ]

        # Update funballer attribute
        setattr(funballer, update_payload[0]["field"], update_payload[0]["value"])
        funballer.save()

        # Convert to json for output
        formatted_funballer = model_to_dict(funballer)

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_funballer,
        )

    def delete(self, request: WSGIRequest, id: int) -> Response:
        """Delete a funballer from postgres db"""
        funballer = self._get_funballer_by_id(id=id)
        funballer.delete()

        return Response(status=status.HTTP_200_OK)

import os

import django

# TODO: Use DJANGO_SETTINGS_MODULE env var to replace this
# These have to be set before any models are imported ¯\_(ツ)_/¯
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fantasy_funball.settings")
django.setup()

from fantasy_funball.models import Funballer


# TODO: Make this a FT
def test_db_crud():
    """Demo of database CRUD workflow"""
    # Create
    funballer_1 = Funballer(
        first_name="Test",
        surname="CRUD",
        points=0,
    )

    # Insert funballer
    funballer_1.save()

    # Retrieve funballer
    funballer_retrieved = Funballer.objects.get(
        first_name="Test", surname="CRUD"
    )

    funballer_id = funballer_retrieved.id

    assert funballer_retrieved.first_name == "Test"
    assert funballer_retrieved.surname == "CRUD"

    # Update funballer
    funballer_retrieved.surname = "UPDATE"
    funballer_retrieved.save()

    # Check was updated correctly
    funballer_updated = Funballer.objects.get(
        id=funballer_id,
    )

    assert funballer_updated.first_name == "Test"
    assert funballer_updated.surname == "UPDATE"

    # Delete funballer
    Funballer.objects.get(
        id=funballer_id,
    ).delete()


if __name__ == "__main__":
    test_db_crud()

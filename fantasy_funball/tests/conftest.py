def pytest_configure():
    import django

    django.setup()

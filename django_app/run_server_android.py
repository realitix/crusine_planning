#!/usr/bin/env python3

import sys


def main(android_data_dir):
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings_android")
    os.environ.setdefault("ANDROID_DATA_DIR", android_data_dir)
    print(android_data_dir)
    from django.core import management
    from django.core import wsgi
    wsgi.get_wsgi_application()

	# Migrate
    from django.core.management.commands import makemigrations, migrate, runserver
    management.call_command(makemigrations.Command(), "rawfood")
    management.call_command(migrate.Command())

    # Prepare database
    from rawfood.management.commands import update_aliments
    management.call_command(update_aliments.Command())

    # Run server
    management.call_command(runserver.Command(), addrport="127.0.0.1:18385", use_reloader=False)


if __name__ == "__main__":
    p = sys.argv[1]
    main(p)

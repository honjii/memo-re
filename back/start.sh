#!/bin/bash

cd app
python manage.py makemigrations
python manage.py migrate
# python manage.py collectstatic

cp -r /usr/local/lib/python3.9/site-packages/debug_toolbar/static/debug_toolbar /usr/src/app/app/static

# configアプリuWSGIに接続。「--py-autoreload 1」でファイル等に変更があった際は自動リロード
uwsgi --socket :8001 \
      --module config.wsgi \
      --py-autoreload 1 \
      --logto /var/log/uwsgi.log \
      --env DJANGO_SETTINGS_MODULE=config.settings.local

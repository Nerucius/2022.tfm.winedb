#!/bin/sh

alias python="python3"

echo "Running migrations..."
# Perform database migrations
# python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
# Load necessary fixtures
echo ""
echo "Loading Fixtures..."

# User and Group Fixtures
# python manage.py loaddata auth.permission.json
# python manage.py loaddata auth.group.json
# python manage.py loaddata auth.user.json

# NOTE: Reenable the next lines on database rebuild
# python manage.py loaddata backend.answer.json
# python manage.py loaddata backend.knowledgearea.json
# python manage.py loaddata backend.participationrole.json
# python manage.py loaddata backend.projectphase.json
# python manage.py loaddata backend.question.json
# python manage.py loaddata backend.question2.json


# Start Server
uwsgi --ini uwsgi.ini
# uwsgi --ini uwsgi.ini --py-autoreload 1

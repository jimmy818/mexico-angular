#!/bin/bash

echo ""
echo "Welcome installer Django..."

# EnvFile
ENVFILE="./.env"

if [ ! -f "$ENVFILE" ]; then
  echo "File not found!"
  cp -v .env.sample .env
fi

if [ -f "$ENVFILE" ]
then

  # START
  echo "Settings vars environment"
  read -p "Debug mode [default True] or (N): " is_debug
  if [[($is_debug == "")]];
  then
    DEBUG=True
  else
    DEBUG=False
  fi

  # SECRET_KEY
  SECRET_KEY=$(openssl rand -base64 32)
  echo "New secret key generated: ${SECRET_KEY}"

  read -p "Project Name [default Myapp]: " projectname
  if [[($projectname == "")]];
  then
    APPNAME="Myapp"
  else
    APPNAME=$projectname
  fi

  read -p "URL Website [default http://localhost:8000]: " urlwebsite
  if [[($urlwebsite == "")]];
  then
    URL_WEBSITE="http://localhost:8000"
  else
    URL_WEBSITE=$urlwebsite
  fi

  read -p "URL Server [default http://localhost:8000]: " urlserver
  if [[($urlserver == "")]];
  then
    URL_SERVER="http://localhost:8000"
  else
    URL_SERVER=$urlserver
  fi

  read -p "Time Zone [default UTC]: " timezone
  if [[($timezone == "")]];
  then
    TIME_ZONE="UTC"
  else
    TIME_ZONE=$timezone
  fi

  read -p "Pagination size [default 10]: " pagination
  if [[($pagination == "")]];
  then
    PAGE_SIZE="10"
  else
    PAGE_SIZE=$pagination
  fi

  read -p "Database HOST [default localhost]: " dbhost
  if [[($dbhost == "")]];
  then
    DB_HOST="localhost"
  else
    DB_HOST=$dbhost
  fi

  read -p "Database NAME [default empty]: " dbname
  if [[($dbname == "")]];
  then
    DB_NAME=""
  else
    DB_NAME=$dbname
  fi

  read -p "Database USER [default postgres]: " dbuser
  if [[($dbuser == "")]];
  then
    DB_USER="postgres"
  else
    DB_USER=$dbuser
  fi

  read -p "Database PASSWORD [default empty]: " dbpassword
  if [[($dbpassword == "")]];
  then
    DB_PASSWORD=""
  else
    DB_PASSWORD=$dbpassword
  fi

  read -p "Database PORT [default 5432]: " dbport
  if [[($dbport == "")]];
  then
    DB_PORT="5432"
  else
    DB_PORT=$dbport
  fi

  echo "DEBUG=$DEBUG" > "$ENVFILE"
  echo "SECRET_KEY=${SECRET_KEY}" >> "$ENVFILE"
  echo "APPNAME=${APPNAME}" >> "$ENVFILE"
  echo "URL_WEBSITE=${URL_WEBSITE}" >> "$ENVFILE"
  echo "URL_SERVER=${URL_SERVER}" >> "$ENVFILE"
  echo "TIME_ZONE=${TIME_ZONE}" >> "$ENVFILE"
  echo "PAGE_SIZE=${PAGE_SIZE}" >> "$ENVFILE"
  echo "FCM_SERVER_KEY=" >> "$ENVFILE"
  echo "CONEKTA_PRIVATE_KEY=" >> "$ENVFILE"
  echo "SMS_KEY=" >> "$ENVFILE"
  echo "AWS_ENABLE=False" >> "$ENVFILE"
  echo "AWS_REGION=" >> "$ENVFILE"
  echo "AWS_STORAGE_BUCKET_NAME=" >> "$ENVFILE"
  echo "AWS_CLOUD_FRONT_URL=" >> "$ENVFILE"
  echo "EMAIL_USE_TLS=True" >> "$ENVFILE"
  echo "DEFAULT_FROM_EMAIL=from@example.com" >> "$ENVFILE"
  echo "EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend" >> "$ENVFILE"
  echo "EMAIL_HOST=" >> "$ENVFILE"
  echo "EMAIL_HOST_USER=" >> "$ENVFILE"
  echo "EMAIL_HOST_PASSWORD=" >> "$ENVFILE"
  echo "EMAIL_PORT=587" >> "$ENVFILE"
  echo "DB_HOST=${DB_HOST}" >> "$ENVFILE"
  echo "DB_NAME=${DB_NAME}" >> "$ENVFILE"
  echo "DB_USER=${DB_USER}" >> "$ENVFILE"
  echo "DB_PASSWORD=${DB_PASSWORD}" >> "$ENVFILE"
  echo "DB_PORT=${DB_PORT}" >> "$ENVFILE"
fi

# Environment
ENVIRONMENT="./venv"

if [ ! -d "$ENVIRONMENT" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  echo ""
  read -p "Create ENVIRONMENT and install requeriments? (y/n): " activenv

  if [[($activenv == "y")]];
  then
    echo "Creating ENVIRONMENT..."
    virtualenv -p python3 venv
    echo "ENVIRONMENT created"

    source venv/bin/activate
    echo "env activated"

    echo "Installing packages..."
    pip install -r requeriments.txt
  fi
fi

echo ""
read -p "Run collectstatics? (y/n): " collectsta
if [[($collectsta == "y")]];
then
  echo "Creating collectstatics..."
  python manage.py collectstatic --noinput
fi


echo ""
echo "Installation complete."
echo ""

# Exit from the script with success (0)
exit 0

__ARCHIVE__

#!/usr/bin/env bash
set -euxo pipefail
apt install python3.13 python3.13-venv nginx openssl ssl-cert git

cd "$(dirname "$0")"
cp gunicorn.socket /etc/systemd/system/
cp gunicorn.service /etc/systemd/system/
cp gunicorn.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/gunicorn.conf /etc/nginx/sites-enabled/gunicorn.conf || true

cd /opt
#git clone "https://github.com/ProfessorSniff/4125doctor"
(git -C "4125doctor" reset --hard && git -C "4125doctor" pull) || git clone "https://github.com/ProfessorSniff/4125doctor"
git config --global --add safe.directory '/opt/4125doctor'
cd 4125doctor
python3 -m venv .venv
source .venv/bin/activate
pip3 install django gunicorn sendgrid google-cloud-secret-manager
cp /opt/deploy/settings.py ./doctors_office_4125/settings.py
python3 manage.py collectstatic --no-input
#export GOOGLE_VM_IP=$(curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip)
#export SENDGRID_API_KEY=$(gcloud secrets versions access latest --secret="sendgrid-key")
#export DJANGO_SECRET_KEY=$(gcloud secrets versions access latest --secret="django-secret")
#gunicorn doctors_office_4125.wsgi -b unix:/tmp/gunicorn.socket
chown -R www-data:www-data .
systemctl enable --now gunicorn.socket nginx
systemctl reload-or-restart nginx
systemctl stop gunicorn.service

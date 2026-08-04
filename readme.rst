Doctor's Office Appointment System
==================================

    KPU INFO 4125 

    2026-08-07

Manages appointments for a doctor's office. Handles the roles of patients and doctors. 
Appointments can be viewed and requested by patients, and doctors can create and modify (update, confirm/cancel) appointments.
Medical records (visit notes) can be written and modified by doctors, and viewed by patients.

Setup
-----

Prerequisites
*************

- Install Python 3.12 (or newer)
- Create a virtual environment: ``python3 -m venv .venv``
- Activate the virtual environment: ``source .venv/bin/activate``
- Install Django 6: ``pip install django``

Running
*******

Local development:

- Run the Django server: ``python3 manage.py runserver``

Depolyment:

- Install and configure a WSGI server (e.g., Gunicorn)
- Install and configure a web server (e.g., Nginx or Apache) as a reverse proxy
- Optionally, set up a database (e.g., PostgreSQL, MySQL) if usage is expected to exceed the capabilities of SQLite
- Install and configure any production dependencies (e.g. ``pip install sendgrid gunicorn psycopg[binary,pool]``)
- Configure the Django settings as appropriate for production (consult documentation at https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- Apply database migrations: ``python3 manage.py migrate``
- Run the Django self-check: ``python3 manage.py check --deploy``
- Create a superuser: ``python3 manage.py createsuperuser``
- Prepare static files: ``python3 manage.py collectstatic``
- Create (and start) services for the notification service, WSGI server, and/or web server (e.g. systemd)
- Verify functionality and create appropriate users
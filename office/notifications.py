from datetime import timedelta
from django.conf import settings
from django.utils import timezone
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_appointment_reminder(self, appointment, offset_hours, dry_run=False, verbose=False):
    patient = appointment.patient
    to_email = getattr(patient, 'email', None)
    if not to_email:
        if verbose:
            self.stdout.write(self.style.NOTICE(f"No email for user {patient.id}:{patient.display_name}"))
        return False

    appt_time = appointment.date_time
    doctor_name = appointment.doctor.display_name if appointment.doctor else 'No doctor assigned'
    subject = f"Appointment reminder for {patient.display_name}"
    message = (
        f"""
        Appointment for {patient.display_name}:
        
        Date & Time: {timezone.localtime(appt_time).strftime('%F %R %Z')}
        Doctor: {doctor_name}
        """
        
    )
    
    if verbose:
        self.stdout.write(f"Sending appointment '{appointment.id}': {{time='{timezone.localtime(appt_time).strftime('%F %R %Z')}', patient='{patient.display_name}' email='{to_email}', doctor='{doctor_name}', in='{round((appt_time-timezone.now()) / timedelta(hours=1), 2)}h', offset='{offset_hours}h'}}")

    if dry_run:
        return True

    try:
        #send_mail(subject, message, from_email, [to_email], fail_silently=False)
        sg = sendgrid.SendGridAPIClient(api_key=getattr(settings, 'SENDGRID_API_KEY', None))
        mail = Mail(Email(getattr(settings, 'SENDGRID_FROM_ADDRESS', None)), To(to_email), subject, Content("text/plain", message))
        response = sg.client.mail.send.post(request_body=mail.get())
        if response.status_code == 202:
            return True
        else:
            print(response.status_code)
            print(response.headers)
            response.raise_for_status()
            return False
    except Exception:
        return False

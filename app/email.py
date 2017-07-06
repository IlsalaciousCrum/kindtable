'''A function for sending emails asynchronously. Will use Celery or Redis
after initial deployment because this won't scale'''

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['KIND_MAIL_SUBJECT_PREFIX'] + " " + subject,
                  sender=app.config['KIND_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def approve_beta_access(to, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['KIND_MAIL_SUBJECT_PREFIX'] + " " + "Beta Testing Access Approved",
                  sender=app.config['KIND_MAIL_SENDER'], recipients=[to])
    msg.body = render_template("main/email/approved_beta_access" + '.txt', **kwargs)
    msg.html = render_template("main/email/approved_beta_access" + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

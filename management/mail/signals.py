import logging
from email.mime.image import MIMEImage
from smtplib import SMTPAuthenticationError

from bs4 import BeautifulSoup as BS
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rq import job

from management.models import Builder

from .models import Email, InlineAttachment, BuilderEmailInfo
from management.customencryption import *


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Email)
def send_email(sender, **kwargs):
    """
    Signal handler for Email Model
        Checks logic and passes to call to offloaded method.
    """
    print("Post Save")
    logger.info("Post Save")

    data = kwargs.get("instance")
    if kwargs.get("created"):
        add_to_que.delay(data)

@job
def add_to_que(data):
    """
    Offloader function uses redis server
    """
    # data = Email.objects.get(id=13)
    backend = None
    lead = data.mail_id.lead_set.last()

    datax = BuilderEmailInfo.objects.get(builder__id=lead.builder.id)

    try:
        backend = EmailBackend(
            host=datax.email_host,
            port=datax.email_port,
            username=datax.email_username,
            password=datax.email_password,
            use_tls=True,
            fail_silently=False)
    except SMTPAuthenticationError:
        logger.error("Couldn't connect to Email server")


    email_status = -1

    msg = EmailMultiAlternatives(
        data.subject, # SUBJECT
        '',  # TEXT CONTENT (writing html)
        datax.email_username, # FROM
        [str_decode(data.mail_id.mail_id)],  # TO
        datax.email_ccaddress.split(","),  # CC
        headers={'Message-ID': data.id},
        connection=backend)
    htmlcontent = data.message_content
    htmlsoup = BS(htmlcontent, "lxml")
    images = htmlsoup.find_all("img", src=True)
    # logger.info("Email Started added 2")

    images = [img.attrs.get("src") for img in images]
    if images:
        for img in images:
            filename = img.replace("/media/attachment/", "")
            try:
                image = InlineAttachment.objects.get(
                    file_object="attachment/{}".format(filename))
                imagex = MIMEImage(image.file_object.read())
                imagex.add_header(
                    'Content-ID', '<{}>'.format(image.file_name))
                htmlcontent = htmlcontent.replace(
                    img, "cid:{}".format(image.file_name))
                msg.attach(imagex)

            except ObjectDoesNotExist:
                pass
    ext_attachs = data.ext_attachments.all()
    for ext_atch in ext_attachs:
        msg.attach_file("media/{}".format(ext_atch.file_object))
    msg.mixed_subtype = 'related'
    msg.content_subtype = "html"  # Main content is now text/html
    msg.attach_alternative(htmlcontent, "text/html")

    try:
        msg.send()
        email_status = 1
    except Exception as e:
        logger.error("Email not sent: {}".format(e))
    data.status = email_status
    data.save()
    return email_status

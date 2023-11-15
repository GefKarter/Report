from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from Board.models import Responses
from BulletinBoard import settings


@shared_task
def send_response(response_text, ad_id, notification_user_email):

    html_context = render_to_string(
        'response_notification.html', {
            'text': response_text,
            'link': f'{settings.SITE_URL}/notification_detail/{ad_id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новый отклик на ваше объявление!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[notification_user_email],
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()

@shared_task
def send_response_accept(response_id):
    response = Responses.objects.get(id=response_id)  # получаем объект Response
    response_author_email = response.responses_user.email  # получаем email автора отклика Response
    advertising = response.responses_advertising  # получаем объект Notification (объявление), связанный с Response
    author = advertising.notification_user  # Получаем объект User (автор объявления)
    # подготавливаем и отправляем письмо
    html_context = render_to_string(
        'response_accepted_email.html', {
            'title': advertising.title,
            'author': author
        }
    )

    msg = EmailMultiAlternatives(
        subject='Ваш отклик был принят!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[response_author_email],
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()



@shared_task
def send_response_reject(response_id):
    response = Responses.objects.get(id=response_id)  # получаем объект Response
    response_author_email = response.responses_user.email  # получаем email автора отклика Response
    advertising = response.responses_advertising  # получаем объект Notification (объявление), связанный с Response
    # подготавливаем и отправляем письмо
    html_context = render_to_string(
        'response_rejectted_email.html', {
            'title': advertising.title,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Ваш отклик был отклонён',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[response_author_email],
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()

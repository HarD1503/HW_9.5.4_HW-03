from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
#from django.core.mail import mail_managers
from .models import *
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_post_created(sender, instance, **kwargs):
    #if created:
    post = Post.objects.get(pk=instance.pk)
    categories = post.post_category.all()
    title = post.post_title
    subscribers_emails = []

    for categ in categories:
        subscribers_users = categ.subscribers.all()
        for sub_users in subscribers_users:
            subscribers_emails.append(sub_users.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/{instance.pk}',
            }
        )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
        #to=['hardv81@gmail.com', 'skillfactory98@gmail.com'],
        )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

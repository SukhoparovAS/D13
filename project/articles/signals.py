from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Comment, Profile
from django.contrib.auth.models import User
import random


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        random.seed()
        code = random.randint(10000, 99999)
        Profile.objects.create(user=instance, confirmationCode=code)
        userEmail = [instance.email]
        emailTitle = 'Подтверждение регистрации'
        msg = EmailMultiAlternatives(
            subject=f'{emailTitle}',
            body=f'Код подтверждения: {code}',
            from_email='novikov.e.s@yandex.ru',
            to=userEmail,
        )
        msg.send()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Comment)
def CommentAlert(sender, instance, created, **kwargs):

    if instance.user != instance.article.user:
        if created:
            user = instance.article.user
            userEmail = [instance.article.user.email]
            emailTitle = 'Новый отклик на вашу статью'
            html_content = render_to_string(
                'emailTempalates/create_comment_alert.html',
                {
                    'comment': instance,
                    'user': user
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{emailTitle}',
                body=f'',
                from_email='novikov.e.s@yandex.ru',
                to=userEmail,
            )
            msg.attach_alternative(
                html_content, "text/html")
            msg.send()

        elif instance.status == 'accepted':
            user = instance.user
            userEmail = [instance.user.email]
            emailTitle = 'Ваш отклик принят'
            html_content = render_to_string(
                'emailTempalates/accept_comment_alert.html',
                {
                    'comment': instance,
                    'user': user
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{emailTitle}',
                body=f'',
                from_email='novikov.e.s@yandex.ru',
                to=userEmail,
            )
            msg.attach_alternative(
                html_content, "text/html")
            msg.send()

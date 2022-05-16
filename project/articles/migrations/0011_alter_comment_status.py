# Generated by Django 4.0.4 on 2022-05-15 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_alter_comment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('expects', 'Ожидает'), ('rejected', 'Отклонен'), ('accepted', 'Принят')], default='expects', max_length=10),
        ),
    ]

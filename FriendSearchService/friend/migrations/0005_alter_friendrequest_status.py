# Generated by Django 4.2.1 on 2023-05-10 16:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('friend', '0004_alter_friendrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='status',
            field=models.CharField(
                choices=[
                    ('sent', 'Заявка отправлена'),
                    ('incoming', 'Есть входящая заявка'),
                    ('rejected', 'Заявка отклонена'),
                    ('friend', 'Друзья'),
                ],
                default='sent',
                max_length=20,
            ),
        ),
    ]

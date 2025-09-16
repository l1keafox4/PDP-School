import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='important',
            field=models.BooleanField(default=False),
        ),
    ]

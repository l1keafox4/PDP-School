from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_created_at_task_important'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='important',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10),
        ),
    ]

# Generated by Django 2.2.5 on 2019-09-28 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190928_0853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weeklylog',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='drinking',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='smoking',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='clock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='user.Clock'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='MonthlyLog',
        ),
        migrations.DeleteModel(
            name='WeeklyLog',
        ),
    ]

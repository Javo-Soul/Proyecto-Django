# Generated by Django 4.1 on 2022-11-09 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpbd', '0005_alter_auditorias_diarias_resolucion_cd_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditorias_diarias',
            name='user',
            field=models.CharField(choices=[('j0c0af6', 'Auditor 1'), ('v0j0af6', 'Auditor 2'), ('C0j0a56', 'Auditor 3'), ('Z0j0a30', 'Auditor 4')], default='No Asign', max_length=8, verbose_name='Auditor'),
        ),
        migrations.AlterField(
            model_name='auditorias_diarias',
            name='user_supervisor_code',
            field=models.CharField(default='No Asign', max_length=8, verbose_name='Supervisor'),
        ),
    ]

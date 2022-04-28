# Generated by Django 2.2.24 on 2022-04-28 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_auto_20220331_1924"),
        ("management", "0037_auto_20220114_1822"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtRoleRelation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ext_tenant", models.CharField(max_length=10)),
                ("ext_id", models.CharField(max_length=20)),
                ("description", models.TextField()),
                ("role", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="management.Role")),
                (
                    "tenant",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="api.Tenant"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="extrolerelation",
            constraint=models.UniqueConstraint(
                fields=("ext_tenant", "ext_id"), name="unique external id per external tenant"
            ),
        ),
    ]

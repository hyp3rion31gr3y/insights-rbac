# Generated by JayZ 2.2.4 on 2020-06-11 14:57

from django.db import migrations, models


def replicate_permission(apps, schema_editor):
    # get access model
    Access = apps.get_model("management", "Access")

    # iterate through all Access
    for access in Access.objects.all():
        # get the permission context from the permission
        access.permission = access.perm
        access.save()


class Migration(migrations.Migration):

    dependencies = [("management", "0015_add_field_to_permission")]

    operations = [
        migrations.AlterField(
            model_name="access", name="permission", field=models.TextField(null=False, default="*:*:*")
        ),
        migrations.RunPython(replicate_permission),
    ]
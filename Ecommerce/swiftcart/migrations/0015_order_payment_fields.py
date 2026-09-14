from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("swiftcart", "0014_remove_order_created_at_remove_order_payment_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment_status",
            field=models.CharField(default="Pending", max_length=20),
        ),
        migrations.AddField(
            model_name="order",
            name="razorpay_order_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="razorpay_payment_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(default="Pending", max_length=20),
        ),
    ]
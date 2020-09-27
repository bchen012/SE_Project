# Generated by Django 3.1 on 2020-09-27 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0014_auto_20200927_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='town',
            field=models.CharField(choices=[('ANG MO KIO', 'ANG MO KIO'), ('BEDOK', 'BEDOK'), ('BISHAN', 'BISHAN'), ('BUKIT MERAH', 'BUKIT MERAH'), ('BUKIT BATOK', 'BUKIT BATOK'), ('CENTRAL AREA', 'CENTRAL AREA'), ('BUKIT PANJANG', 'BUKIT PANJANG'), ('GEYLANG', 'GEYLANG'), ('BUKIT TIMAH', 'BUKIT TIMAH'), ('CHOA CHU KANG', 'CHOA CHU KANG'), ('CLEMENTI', 'CLEMENTI'), ('HOUGANG', 'HOUGANG'), ('QUEENSTOWN', 'QUEENSTOWN'), ('JURONG EAST', 'JURONG EAST'), ('JURONG WEST', 'JURONG WEST'), ('KALLANG', 'KALLANG'), ('MARINE PARADE', 'MARINE PARADE'), ('PASIR RIS', 'PASIR RIS'), ('PUNGGOL', 'PUNGGOL'), ('SEMBAWANG', 'SEMBAWANG'), ('SENGKANG', 'SENGKANG'), ('SERANGOON', 'SERANGOON'), ('TAMPINES', 'TAMPINES'), ('TOA PAYOH', 'TOA PAYOH'), ('WOODLANDS', 'WOODLANDS'), ('YISHUN', 'YISHUN')], default='BEDOK', max_length=25),
        ),
    ]

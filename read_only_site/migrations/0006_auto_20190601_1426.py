# Generated by Django 2.2.1 on 2019-06-01 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_only_site', '0005_auto_20190531_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='match_identifier',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='match',
            name='played_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='player_1_trueskill_mu_after_match',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='match',
            name='player_1_trueskill_mu_before_match',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='match',
            name='player_1_trueskill_sigma_after_match',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='match',
            name='player_1_trueskill_sigma_before_match',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='match',
            name='player_2_trueskill_mu_after_match',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='match',
            name='player_2_trueskill_mu_before_match',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='match',
            name='player_2_trueskill_sigma_after_match',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='match',
            name='player_2_trueskill_sigma_before_match',
            field=models.FloatField(blank=True, default=0.0),
        ),
    ]

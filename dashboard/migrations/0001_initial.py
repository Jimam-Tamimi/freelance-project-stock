# Generated by Django 3.2.5 on 2021-07-17 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.TextField(blank=True, max_length=2000, null=True)),
                ('live_quotes', models.BooleanField(default=True)),
                ('update_every', models.IntegerField(default=10, null=True)),
                ('default_commission', models.FloatField(blank=True, default=0, null=True)),
                ('cash', models.FloatField(blank=True, default=0, null=True)),
                ('portfolio_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('days_held', models.IntegerField(default=0, null=True)),
                ('current_value', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('profit', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('profit_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('currency', models.CharField(default='INR', max_length=5)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('modified', models.DateField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=20, verbose_name='Symbol')),
                ('quantity', models.IntegerField(default=0, null=True, verbose_name='Shares')),
                ('purchase_date', models.DateField(auto_now_add=True, null=True, verbose_name='Purchase Date')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Buy Price')),
                ('adjusted_buy_price', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Adjusted Buy Price')),
                ('purchase_cost', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Purchase Cost')),
                ('comments', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Comments')),
                ('commissions', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Commissions')),
                ('fees', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Fees')),
                ('update_cash_balance', models.BooleanField(default=True, verbose_name='Update Cash')),
                ('transaction_type', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=10, verbose_name='Transaction Type')),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('modified', models.DateField(auto_now_add=True, null=True)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='dashboard.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField(default=0, null=True)),
                ('symbol', models.CharField(max_length=20, verbose_name='Symbol')),
                ('longName', models.CharField(max_length=150, null=True, verbose_name='Name')),
                ('regularMarketPrice', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Current Price')),
                ('regularMarketTime', models.DateField(null=True, verbose_name='Last Price Update Date and Time')),
                ('regularMarketChange', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Day Change')),
                ('regularMarketChangePercent', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Day Change %')),
                ('regularMarketDayLow', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Day Lo')),
                ('regularMarketDayHigh', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Day Hi')),
                ('fiftyTwoWeekLow', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='52 Week Lo')),
                ('fiftyTwoWeekHigh', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='52 Week Hi')),
                ('regularMarketVolume', models.PositiveBigIntegerField(default=0, null=True, verbose_name='Volume')),
                ('averageDailyVolume10Day', models.PositiveBigIntegerField(default=0, null=True, verbose_name='Volume Average 10 days')),
                ('averageDailyVolume3Month', models.PositiveBigIntegerField(default=0, null=True, verbose_name='Volume Average 3M')),
                ('marketCap', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Mkt Cap')),
                ('epsTrailingTwelveMonths', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='EPS')),
                ('trailingPE', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='P/E')),
                ('priceToBook', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='P/B')),
                ('enterpriseToEbitda', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='EV/ EBITDA')),
                ('trailingAnnualDividendYield', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Dividend Yield')),
                ('debtToEquity', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='D/E')),
                ('returnOnEquity', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='ROE')),
                ('returnOnAssets', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='ROA')),
                ('totalRevenue', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Revenues')),
                ('ebitda', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True, verbose_name='EBITDA')),
                ('sector', models.CharField(blank=True, max_length=250, null=True, verbose_name='Sector')),
                ('industry', models.CharField(blank=True, max_length=250, null=True, verbose_name='Industry')),
                ('website', models.CharField(blank=True, max_length=250, null=True, verbose_name='Website')),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('modified', models.DateField(auto_now_add=True, null=True)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='dashboard.portfolio')),
            ],
        ),
    ]

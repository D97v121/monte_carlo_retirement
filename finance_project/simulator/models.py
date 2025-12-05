from django.db import models

class Scenario(models.Model):
    name = models.CharField(max_length=100, default="My Scenario")
    initial_balance = models.FloatField()
    mean_return = models.FloatField()
    volatility = models.FloatField()
    annual_withdrawal = models.FloatField()
    inflation = models.FloatField()
    years = models.IntegerField()
    n_sims = models.IntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scenario: {self.name}"

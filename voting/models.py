from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='candidates/')
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} for {self.portfolio.name}"

class Voter(models.Model):
    password = models.CharField(max_length=50)
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return self.password

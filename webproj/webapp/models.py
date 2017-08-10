from django.db import models

class Info(models.Model):
    fname=models.CharField(max_length=200)
    lname=models.CharField(max_length=200)
    date=models.DateTimeField()

    def __Info__(self):
        return self.fname

from django.db import models

class Content(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100)

    class Meta:
        app_label = 'adminpanel'
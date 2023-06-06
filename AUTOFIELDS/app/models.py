from django.db import models


class Forms(models.Model):
    form = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.form


class Details(models.Model):
    details = models.ForeignKey(Forms, on_delete=models.CASCADE, default=None, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    worker_id = models.CharField(max_length=10, blank=True)
    additional = models.JSONField(blank=True)

    def __str__(self):
        return self.details.form


class DynamicField(models.Model):
    details = models.ForeignKey(Forms, on_delete=models.CASCADE, default=None, null=True, blank=True)
    fields = models.JSONField(blank=True)

    def __str__(self):
        return self.details.form

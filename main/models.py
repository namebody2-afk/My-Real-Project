from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Shahar nomi")
    img = models.ImageField(
        upload_to='cities/', blank=True, null=True, default=None,
        verbose_name="Rasm"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shahar"
        verbose_name_plural = "Shaharlar"
        ordering = ['name']

    def __str__(self):
        return self.name


class House(models.Model):
    img = models.ImageField(upload_to='houses/', verbose_name="Uy rasmi")
    type = models.CharField(max_length=15, verbose_name="Turi", help_text="Sale yoki Rent")
    price = models.FloatField(verbose_name="Narxi ($)")
    address = models.CharField(max_length=100, verbose_name="Manzil")
    description = models.TextField(verbose_name="Tavsif")
    room_count = models.IntegerField(verbose_name="Xonalar soni")
    floor = models.IntegerField(verbose_name="Qavat")
    floor_count = models.IntegerField(verbose_name="Jami qavatlar")
    area = models.FloatField(verbose_name="Maydon (sqm)")
    title = models.CharField(max_length=100, verbose_name="Sarlavha")
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, blank=True, null=True, default=None,
        verbose_name="Shahar", related_name="houses"
    )
    broker = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, blank=True, null=True, default=None,
        verbose_name="Agent", related_name="broker_houses"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'houses'
        verbose_name = 'Uy'
        verbose_name_plural = 'Uylar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.city.name if self.city else '—'} (${self.price})"
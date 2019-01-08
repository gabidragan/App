from django.contrib import admin
from .models import Post

# Here you can register your models here so they will be available on the admin page.
admin.site.register(Post)

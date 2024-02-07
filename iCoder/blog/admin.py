from django.contrib import admin

# Register your models here.
from blog.models import Post,BlogComment

admin.site.register((Post,BlogComment))


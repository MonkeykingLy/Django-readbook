from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Collection)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(LikeIt)
admin.site.register(Goal)
admin.site.register(Collection_Book)

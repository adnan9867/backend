from django.contrib import admin

from user_module.models import *

admin.site.register(User)
admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(UserHolidayInfo)

from timecard.models import User, UserTime, UserDepartament, UserPost, UserPostComment
from django.contrib import admin

admin.site.register(User)
admin.site.register(UserTime)
admin.site.register(UserDepartament)
admin.site.register(UserPost)
admin.site.register(UserPostComment)
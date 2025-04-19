from django.contrib import admin
from . models import Course, Lesson, Profile, Enrollment, User, Category, Comment, AdditionalResoursesUrl

# Registeration My models .
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Profile)
admin.site.register(Enrollment)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(AdditionalResoursesUrl)
from django.contrib import admin
from core.models import *
admin.site.register(PurpleWigUser)
admin.site.register(VerificationToken)
admin.site.register(PasswordResetToken)
admin.site.register(Course)
admin.site.register(CourseRegistration)
admin.site.register(Service)
admin.site.register(ServiceRegistration)
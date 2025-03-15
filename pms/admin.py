from django.contrib import admin
from . import models

admin.site.register((
    models.User, 
    models.Project,
    models.ProjectMember,
    models.Task,
    models.Comment))


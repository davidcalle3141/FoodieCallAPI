from django.contrib import admin

from Authentication.models import Account as MyModel

admin.site.register(MyModel)
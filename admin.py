from django.contrib import admin

from servicecatalog.models import *

class hardware_depending_on_instanceInline(admin.TabularInline):
    model = hardware_depending_on_instance
    fk_name = 'from_hardware'
    extra = 1

class hardware_depending_on_hardwareInline(admin.TabularInline):
    model = hardware_depending_on_hardware
    fk_name = 'hardware_from'
    extra = 1

class ContactAdmin(admin.ModelAdmin):
    pass
admin.site.register(Contact, ContactAdmin)

class ContactMethodAdmin(admin.ModelAdmin):
    pass
admin.site.register(ContactMethod, ContactMethodAdmin)

class ModuleAdmin(admin.ModelAdmin):
    prepopulated_fields = { "slug": ("name",) }
    pass
admin.site.register(Module, ModuleAdmin)

class InstanceAdmin(admin.ModelAdmin):
    prepopulated_fields = { "slug": ("name",) }
    pass
admin.site.register(Instance, InstanceAdmin)

class HardwareAdmin(admin.ModelAdmin):
    inlines = (hardware_depending_on_hardwareInline, hardware_depending_on_instanceInline, )
    pass
admin.site.register(Hardware, HardwareAdmin)

class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Location, LocationAdmin)
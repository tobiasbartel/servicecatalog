from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.core.validators import validate_comma_separated_integer_list

class Contact(models.Model):

    TEAM = 'team'
    PERSON = 'person'
    TYPE_OPTIONS = (
        (TEAM, 'Team'),
        (PERSON, 'Person'),
    )

    type = models.CharField(max_length=10, choices=TYPE_OPTIONS)
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return str("%s: %s" % (self.get_type_display(), self.name))

class ContactMethod(models.Model):

    LYNC = 'lync'
    EMAIL = 'email'
    PHONE = 'phone'
    MOBILE = 'mobile'
    WEB = 'web'
    OCD = 'ocd'
    TICKET = 'ticket'
    METHOD_OPTIONS = (
        (LYNC, 'Lync'),
        (EMAIL, 'EMail'),
        (PHONE, 'Office Phone'),
        (MOBILE, 'Mobile Phone'),
        (WEB, 'Web'),
        (OCD, 'On Call'),
        (TICKET, 'Ticketing (Web)'),

    )

    method = models.CharField(max_length=10, choices=METHOD_OPTIONS)
    value = models.CharField(max_length=200)
    contact = models.ForeignKey(Contact, related_name='contact_to_method')

    def __unicode__(self):
        return str("%s: %s" % (self.get_method_display(), self.value))

class Module(models.Model):

    DEV = 'dev'
    LIVE = 'live'
    DEPRICATED = 'depricated'
    MODULE_STATE = (
        (DEV, 'In development'),
        (LIVE, 'Live'),
        (DEPRICATED, 'Depricated'),
    )
    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    owners = models.ManyToManyField(Contact, blank=True)
    description = models.TextField(blank=True, null=True)
    documentation = models.URLField(blank=True, null=True)
    tickets = models.URLField(blank=True, null=True)
    depending_on = models.ManyToManyField('self', blank=True, symmetrical=False, default=None)
    customer_facing = models.BooleanField(default=False)
    state = models.CharField(max_length=10, choices=MODULE_STATE, default=LIVE, blank=False)


    def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Module, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.name)

class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return str(self.name)

class Instance(models.Model):

    DEV = 'dev'
    INTE = 'inte'
    QA = 'qa'
    CTEST = 'ctest'
    PROD = 'prod'
    ENVIRONMENT_OPTIONS = (
        (DEV, 'Development'),
        (INTE, 'Integration'),
        (QA, 'Quality Assurance'),
        (CTEST, 'Customer Test'),
        (PROD, 'Production'),
    )

    DEV = 'dev'
    LIVE = 'live'
    DEPRICATED = 'depricated'
    MODULE_STATE = (
        (DEV, 'In development'),
        (LIVE, 'Live'),
        (DEPRICATED, 'Depricated'),
    )

    name = models.CharField(max_length=200, unique=False, blank=True, default='')
    slug = models.SlugField(unique=True, null=True, blank=True)
    module = models.ForeignKey(Module, related_name='instance_to_module')
    environment = models.CharField(max_length=10, choices=ENVIRONMENT_OPTIONS, default=None, blank=False, null=False)
    location = models.ForeignKey('Location', unique=False)
    service_delivery = models.ForeignKey(Contact, blank=True, null=True)
    depending_on = models.ManyToManyField('self', symmetrical=False, default=None, blank=True, related_name='instance_on_instance')
    customer_accesable = models.BooleanField(default=False)
    state = models.CharField(max_length=10, choices=MODULE_STATE, default=LIVE, blank=False)

    class Meta:
        unique_together = ('name', 'module', 'environment', 'location')

    def __unicode__(self):
        if self.name is not '':
            return str("%s - %s (%s, %s)" % (self.name, self.module.name, self.location.name, self.get_environment_display()))
        else:
            return str("%s (%s, %s)" % (self.module.name, self.get_environment_display(), self.location.name))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__unicode__())
        super(Instance, self).save(*args, **kwargs)


class Hardware(models.Model):

    LB = 'lb'
    WEB = 'web'
    APP = 'app'
    DB = 'db'
    FILE = 'file'
    TOKEN = 'token'
    TYPE_OPTIONS = (
        (LB, 'Loadbalancer'),
        (WEB, 'Web Server'),
        (APP, 'Application Server'),
        (DB, 'Database Server'),
        (FILE, 'File Server'),
        (TOKEN, 'Tokenizer')
    )

    name = models.CharField(max_length=200, unique=True, db_index=True, blank=False)
    instance = models.ForeignKey(Instance, blank=False, null=False, related_name='belongs_to_instance')
    type = models.CharField(max_length=10, choices=TYPE_OPTIONS, default=None, blank=False, null=False)
    ip = models.GenericIPAddressField(blank=True, null=True)
    depending_on_hardware = models.ManyToManyField('self', through='hardware_depending_on_hardware', through_fields=('hardware_from', 'hardware_to'), related_name='hardware_on_hardware', symmetrical=False, default=None, blank=True)
    depending_on_instance = models.ManyToManyField('Instance', through='hardware_depending_on_instance', through_fields=('from_hardware', 'to_instance'), related_name='hardware_on_instance', symmetrical=False, blank=True, null=True)

    def __unicode__(self)   :
        return str("%s - %s" % (self.name, self.instance))


class hardware_depending_on_hardware(models.Model):
    hardware_from = models.ForeignKey('Hardware', related_name='hardwareFrom')
    hardware_to = models.ForeignKey('Hardware', related_name='hardwareTo')
    port_numbers = models.CharField(max_length=200, validators=[validate_comma_separated_integer_list], null=True, blank=True)
    class Meta:
        unique_together = ('hardware_from', 'hardware_to')


class hardware_depending_on_instance(models.Model):
    from_hardware = models.ForeignKey('Hardware', related_name='fromHardware')
    to_instance = models.ForeignKey('Instance', related_name='toInstance')
    port_numbers = models.CharField(max_length=200, validators=[validate_comma_separated_integer_list], null=True, blank=True)
    class Meta:
        unique_together = ('from_hardware', 'to_instance')
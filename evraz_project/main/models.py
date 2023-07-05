from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now

class ActionType(models.Model):
    name = models.CharField('Тип действия', max_length=45)

    class Meta:
        managed = False
        db_table = 'action_type'

    def __str__(self):
        return self.name


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Fact(models.Model):
    production_plan = models.ForeignKey('Plan', models.DO_NOTHING)
    time = models.IntegerField()
    volume = models.FloatField()

    class Meta:
        managed = False
        db_table = 'fact'


class Plan(models.Model):
    work_shift = models.ForeignKey('WorkShift', models.DO_NOTHING)
    hour = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])
    action_type = models.ForeignKey(ActionType, models.DO_NOTHING)
    profile = models.ForeignKey('Profile', models.DO_NOTHING, blank=True, null=True)
    time = models.IntegerField(validators=[MaxValueValidator(60), MinValueValidator(1)])
    volume = models.FloatField(max_length=5)

    class Meta:
        managed = False
        db_table = 'plan'


class Profile(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'profile'

    def __str__(self):
        return self.name


class Standart(models.Model):
    profile = models.OneToOneField(Profile, models.DO_NOTHING)
    volume_in_hour = models.FloatField()

    class Meta:
        managed = False
        db_table = 'standart'


class WorkShift(models.Model):
    type = models.ForeignKey('WorkShiftType', models.DO_NOTHING)
    date = models.DateField(default=now)

    class Meta:
        managed = False
        db_table = 'work_shift'

    def __str__(self):
        return f"{self.type} {self.date}"

    def save(self, *args, **kwargs):
        super(WorkShift, self).save(*args, **kwargs)
        return self

class WorkShiftType(models.Model):
    name = models.CharField('Тип смены', max_length=45)

    class Meta:
        managed = False
        db_table = 'work_shift_type'

    def __str__(self):
        return self.name

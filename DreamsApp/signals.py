# coding=utf-8
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save, post_init, post_delete
from django.dispatch import receiver

from DreamsApp.middlewares.CurrentUserMiddleware import get_current_user
from DreamsApp.models import Audit, AuditTrail


@receiver(post_init, )
def set_original_data(sender, instance, *args, **kwargs):
    instance._original_data = instance.__dict__.copy()


@receiver(post_save, )
def create_audit_log(sender, instance, created, *args, **kwargs):
    action = "CREATE" if created else "UPDATE"
    user = get_current_user()

    if user is None or isinstance(instance, (Session, Audit, AuditTrail)):
        return

    audit = Audit()
    audit.user = user
    audit.table = instance._meta.db_table
    audit.row_id = instance.pk
    audit.action = action
    audit.search_text = None
    audit.save()

    exclude_fields = ["date_changed", "password"]
    for k, v in instance._original_data.iteritems():
        if v != instance.__dict__[k] and k not in exclude_fields:
            audit_trail = AuditTrail()
            audit_trail.audit = audit
            audit_trail.column = k
            audit_trail.old_value = instance._original_data[k]
            audit_trail.new_value = instance.__dict__[k]
            audit_trail.save()


@receiver(post_delete, )
def create_delete_audit_log(sender, instance, *args, **kwargs):
    action = "DELETE"
    user = get_current_user()

    if user is None or isinstance(instance, (Session, Audit, AuditTrail)):
        return

    audit = Audit()
    audit.user = user
    audit.table = instance._meta.db_table
    audit.row_id = instance.pk
    audit.action = action
    audit.search_text = None
    audit.save()

    for k, v in instance._original_data.iteritems():
        audit_trail = AuditTrail()
        audit_trail.audit = audit
        audit_trail.column = k
        audit_trail.old_value = instance._original_data[k]
        audit_trail.new_value = instance.__dict__[k]
        audit_trail.save()

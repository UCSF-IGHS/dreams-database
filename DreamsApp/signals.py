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
    user_id = get_current_user().id if get_current_user() is not None else None

    if user_id is None or isinstance(instance, Session) or isinstance(instance, Audit) or isinstance(instance,
                                                                                                     AuditTrail):
        return

    audit = Audit()
    audit.user_id = user_id
    audit.table = instance._meta.db_table
    audit.row_id = instance.pk
    audit.action = action
    audit.search_text = None
    audit.save()

    if not created:
        # If not created, it is an update
        exclude_fields = ["date_changed"]
        for k, v in instance._original_data.iteritems():
            if v != instance.__dict__[k] and k not in exclude_fields:
                audit_trail = AuditTrail()
                audit_trail.audit = audit
                audit_trail.column = k
                audit_trail.old_value = instance._original_data[k]
                audit_trail.new_value = instance.__dict__[k]
                audit_trail.save()


@receiver(post_delete, )
def create_delete_audit_log(sender, instance):
    action = "DELETE"
    user_id = get_current_user().id if get_current_user() is not None else None

    if user_id is None or isinstance(instance, Session) or isinstance(instance, Audit) or isinstance(instance,
                                                                                                     AuditTrail):
        return

    audit = Audit()
    audit.user_id = user_id
    audit.table = instance._meta.db_table
    audit.row_id = instance.pk
    audit.action = action
    audit.search_text = None
    audit.save()

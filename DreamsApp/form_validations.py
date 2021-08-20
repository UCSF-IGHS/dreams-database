from datetime import datetime

from django.core.exceptions import ValidationError


def validate_ips(validation_errors, ip_lists):
    if ip_lists is None or ip_lists == '':
        validation_errors['ips'] = 'IP list cannot be None'


def validate_from_date(form, validation_errors):
    from_date = form.get('from_date')
    to_date = form.get('to_date')
    if from_date and to_date:
        if datetime.strptime(from_date, '%Y-%m-%d') > datetime.strptime(to_date, '%Y-%m-%d'):
            validation_errors['from_date'] = 'From date cannot be greater than to date'
        if datetime.strptime(from_date, '%Y-%m-%d') > datetime.today():
            validation_errors['from_date'] = 'From date cannot be greater than today'
    if from_date and not to_date:
        if datetime.strptime(from_date, '%Y-%m-%d') > datetime.today():
            validation_errors['from_date'] = 'From date cannot be greater than today'


def validate_to_date(form, validation_errors):
    from_date = form.get('from_date')
    to_date = form.get('to_date')

    if from_date and to_date:
        if datetime.strptime(from_date, '%Y-%m-%d') > datetime.strptime(to_date, '%Y-%m-%d'):
            validation_errors['to_date'] = 'To date cannot be greater than from date'
        if datetime.strptime(to_date, '%Y-%m-%d') > datetime.today():
            validation_errors['to_date'] = 'To date cannot be greater than today'

    if (to_date and not from_date):
        if datetime.strptime(to_date, '%Y-%m-%d') > datetime.today():
            validation_errors['to_date'] = 'To date cannot be greater than today'
    return datetime.strptime(to_date, '%Y-%m-%d') if to_date else None


def validate_export_form(form):
    validation_errors = {}
    try:
        validate_ips(validation_errors, form)
        validate_from_date(validation_errors, form)
        validate_to_date(validation_errors, form)
        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)

    except ValidationError as e:
        raise Exception(e)

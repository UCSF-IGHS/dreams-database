# coding=utf-8
from django.forms import ModelForm

# DreamsApp imports
from DreamsApp.models import Grievance, ImplementingPartner, ClientCashTransferDetails


class GrievanceModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(GrievanceModelForm, self).__init__(*args, **kwargs)
        if current_user is not None and not current_user.has_perm('auth.can_view_cross_ip'):
            self.fields['implementing_partner'].queryset = ImplementingPartner.objects.filter(id=current_user.implementingpartneruser.implementing_partner.id)

    class Meta(object):
            model = Grievance
            fields = '__all__'
            exclude = ['created_by', 'created_at', 'modified_by', 'modified_at']


class ClientCashTransferDetailsForm(ModelForm):

    class Meta(object):
        model = ClientCashTransferDetails
        fields = '__all__'
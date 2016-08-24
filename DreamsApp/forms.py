# coding=utf-8
from django.forms import ModelForm

# DreamsApp imports
from DreamsApp.models import Grievance, ImplementingPartner, ClientCashTransferDetails, Client


class GrievanceModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(GrievanceModelForm, self).__init__(*args, **kwargs)

    class Meta(object):
            model = Grievance
            fields = '__all__'
            exclude = ['created_by', 'created_at', 'modified_by', 'modified_at']


class ClientCashTransferDetailsForm(ModelForm):

    def __init__(self, *args, **kwargs):
        current_AGYW = kwargs.pop('current_AGYW', None)
        super(ClientCashTransferDetailsForm, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = \
            Client.objects.filter(id=current_AGYW.id) \
                if current_AGYW is not None \
                else Client.objects.all()

    class Meta(object):
        model = ClientCashTransferDetails
        fields = '__all__'
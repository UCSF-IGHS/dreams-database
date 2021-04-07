import uuid
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.test import TestCase

from DreamsApp.models import User, Client, Intervention, InterventionType, ServiceDelegation, ImplementingPartner, \
    ImplementingPartnerUser


class InterventionDelegationTestCase(TestCase):
    fixtures = ['test_verification_document', 'test_marital_status', 'test_user', 'test_intervention_category',
                'test_intervention_type', 'test_county',
                'implementing_partner_funder', 'test_implementing_partner', 'external_organisation_type',
                'external_organisation', 'test_sub_county', 'test_ward', 'test_client', 'test_hts_result',
                'test_pregnancy_test_result']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = cls.generate_test_data()
        cls.ip_a = cls.test_data['ip_a']
        cls.ip_b = cls.test_data['ip_b']
        cls.ip_a_user = cls.test_data['ip_a_user']
        cls.ip_b_user = cls.test_data['ip_b_user']
        cls.ip_c_user = cls.test_data['ip_c_user']

    @classmethod
    def generate_test_data(cls):
        test_data = {}
        test_data['ip_a'] = cls.get_ip_by_code(code=1)
        test_data['ip_b'] = cls.get_ip_by_code(code=2)
        test_data['ip_c'] = cls.get_ip_by_code(code=3)
        test_data['ip_a_user'] = cls.get_implementing_partner_user(implementing_partner=test_data['ip_a'])
        test_data['ip_b_user'] = cls.get_implementing_partner_user(implementing_partner=cls.get_ip_by_code(code=2))
        test_data['ip_c_user'] = cls.get_implementing_partner_user(implementing_partner=test_data['ip_c'])
        test_data['ip_a_client'] = cls.create_client_for_implementing_partner(test_data['ip_a'])
        test_data['ip_b_client'] = cls.create_client_for_implementing_partner(test_data['ip_b'])
        test_data['ip_c_client'] = cls.create_client_for_implementing_partner(test_data['ip_c'])
        test_data[
            'intervention_by_ip_a_to_ip_a_client'] = cls.get_intervention_by_ip_to_ip_client(test_data['ip_a_user'],
                                                                                             test_data['ip_a_client'])
        test_data[
            'intervention_by_ip_a_to_ip_b_client'] = cls.get_intervention_by_ip_to_ip_client(test_data['ip_a_user'],
                                                                                             test_data['ip_b_client'])
        test_data[
            'intervention_by_ip_b_to_ip_a_client'] = cls.get_intervention_by_ip_to_ip_client(test_data['ip_b_user'],
                                                                                             test_data['ip_a_client'])
        test_data[
            'intervention_by_ip_b_to_ip_b_client'] = cls.get_intervention_by_ip_to_ip_client(test_data['ip_b_user'],
                                                                                             test_data['ip_b_client'])
        test_data[
            'intervention_by_ip_b_to_ip_c_client'] = cls.get_intervention_by_ip_to_ip_client(test_data['ip_b_user'],
                                                                                             test_data['ip_c_client'])
        test_data[
            'intervention_by_ip_a_to_ip_c_client'] = cls.get_intervention_by_ip_to_ip_client(test_data['ip_a_user'],
                                                                                             test_data['ip_c_client'])
        test_data[
            'intervention_by_ip_c_to_ip_a_client'] = cls.get_intervention_by_ip_to_ip_client(test_data['ip_c_user'],
                                                                                             test_data['ip_a_client'])
        test_data[
            'intervention_by_ip_c_to_ip_b_client'] = cls.get_intervention_by_ip_to_ip_client(test_data['ip_c_user'],
                                                                                             test_data['ip_b_client'])
        test_data[
            'intervention_by_ip_c_to_ip_c_client'] = cls.get_intervention_by_ip_to_ip_client(test_data['ip_c_user'],
                                                                                             test_data['ip_c_client'])
        return test_data

    @classmethod
    def register_user(cls):
        user = User.objects.create_user(
            username=str(uuid.uuid4()),
            email=None,
            password='empty',
            first_name="first",
            last_name="last",
        )
        return user

    @classmethod
    def get_implementing_partner_user(cls, implementing_partner):
        user = cls.register_user()
        implementing_partner_user = ImplementingPartnerUser(user=user, implementing_partner=implementing_partner)
        return implementing_partner_user

    @classmethod
    def get_intervention_type_1003(cls):
        return InterventionType.objects.get(code=1003)

    @classmethod
    def create_active_delegation(cls, delegating_implementing_partner, delegated_implementing_partner):
        delegating_implementing_partner.save()
        delegated_implementing_partner.save()
        delegation = ServiceDelegation.objects.create(main_implementing_partner=delegating_implementing_partner,
                                                      delegated_implementing_partner=delegated_implementing_partner,
                                                      start_date=datetime.now().date(),
                                                      end_date=datetime.now() + timedelta(weeks=26),
                                                      financial_year='2020/2021',
                                                      intervention_type=cls.get_intervention_type_1003(),
                                                      created_by=User.objects.get(username='admin'),
                                                      date_created=datetime.now(),
                                                      updated_by=User.objects.get(username='admin'),
                                                      date_updated=datetime.now()
                                                      )
        return delegation

    @classmethod
    def get_intervention_by_ip_to_ip_client(cls, implementing_partner_user, client, save=None):
        intervention = None
        if save is None:
            intervention = Intervention(client=client,
                                        intervention_type=cls.get_intervention_type_1003(),
                                        intervention_date=datetime.now(), voided=False,
                                        created_by=implementing_partner_user.user, date_created=datetime.now(),
                                        implementing_partner=implementing_partner_user.implementing_partner)
        elif save and save is True:
            client.save()
            intervention = Intervention(client=client,
                                        intervention_type=cls.get_intervention_type_1003(),
                                        intervention_date=datetime.now(), voided=False,
                                        created_by=implementing_partner_user.user, date_created=datetime.now(),
                                        implementing_partner=implementing_partner_user.implementing_partner)
            intervention.save()
        return intervention

    @classmethod
    def create_expired_delegation(cls, delegating_implementing_partner, delegated_implementing_partner):
        delegating_implementing_partner.save()
        delegated_implementing_partner.save()
        delegation = ServiceDelegation.objects.create(main_implementing_partner=delegating_implementing_partner,
                                                      delegated_implementing_partner=delegated_implementing_partner,
                                                      start_date=datetime.now() - timedelta(weeks=26),
                                                      end_date=datetime.now() - timedelta(weeks=1),
                                                      financial_year='2020/2021',
                                                      intervention_type=cls.get_intervention_type_1003(),
                                                      created_by=User.objects.get(username='admin'),
                                                      date_created=datetime.now(),
                                                      updated_by=User.objects.get(username='admin'),
                                                      date_updated=datetime.now()
                                                      )
        return delegation

    @classmethod
    def get_ip_by_code(cls, code, save=False):
        implementing_partner = None
        try:
            implementing_partner = get_object_or_404(ImplementingPartner, code=code)
        except:
            implementing_partner = ImplementingPartner(name=f"IP of CODE {code}", code=code)
            if save:
                implementing_partner.save()
        return implementing_partner

    @classmethod
    def get_single_ip_client(cls, implementing_partner):
        return Client.objects.filter(implementing_partner=implementing_partner).first()

    @classmethod
    def get_user_by_username(cls, username):
        user = None
        try:
            user = get_object_or_404(User, username=username)
        except:
            user = User(username=username, password="goal@1234")
        return user

    @classmethod
    def create_client_for_implementing_partner(cls, implementing_partner, save=False):
        client = Client(first_name="Jane", last_name="Doe", implementing_partner=implementing_partner,
                        date_of_enrollment=(datetime.now() - timedelta(weeks=56)).date())
        if save:
            client.save()
        return client

    @classmethod
    def get_client_interventions_by_ip(cls, client, implementing_partner):
        return Intervention.objects.filter(client=client, implementing_partner=implementing_partner)

    @classmethod
    def get_client_interventions(cls, client):
        return Intervention.objects.filter(client=client)

    @classmethod
    def create_test_data_for_ip_clients(cls):
        test_data_for_ip_clients = {}

        test_data_for_ip_clients['ip_x'] = cls.get_ip_by_code(code=100)
        test_data_for_ip_clients['ip_y'] = cls.get_ip_by_code(code=101)
        test_data_for_ip_clients['ip_z'] = cls.get_ip_by_code(code=102)
        test_data_for_ip_clients['ip_x_user'] = cls.get_implementing_partner_user(
            implementing_partner=test_data_for_ip_clients['ip_x'])
        test_data_for_ip_clients['ip_y_user'] = cls.get_implementing_partner_user(
            implementing_partner=test_data_for_ip_clients['ip_y'])
        test_data_for_ip_clients['ip_z_user'] = cls.get_implementing_partner_user(
            implementing_partner=test_data_for_ip_clients['ip_z'])
        test_data_for_ip_clients['client_x_1'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_x'])
        test_data_for_ip_clients['client_x_2'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_x'])
        test_data_for_ip_clients['client_x_3'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_x'])
        test_data_for_ip_clients['client_y_1'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_y'])
        test_data_for_ip_clients['client_y_2'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_y'])
        test_data_for_ip_clients['client_z_1'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_z'])
        test_data_for_ip_clients['client_z_2'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_z'])
        test_data_for_ip_clients['client_z_3'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_z'])

        test_data_for_ip_clients[
            'intervention_by_ip_z_to_ip_y_client_1'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_y_user'],
            test_data_for_ip_clients['client_z_1'],
            save=True
        )
        test_data_for_ip_clients[
            'intervention_by_ip_z_to_ip_y_client_2'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_y_user'],
            test_data_for_ip_clients['client_z_2'],
            save=True
        )
        return test_data_for_ip_clients

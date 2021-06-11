import random
import uuid
from datetime import datetime, timedelta

from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.shortcuts import get_object_or_404
from django.test import TestCase, RequestFactory

from DreamsApp.models import User, Client, Intervention, InterventionType, ServiceDelegation, ImplementingPartner, \
    ImplementingPartnerUser, County, SubCounty, Ward


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
        cls.random_ip = cls.test_data['random_ip']
        cls.ip_a_user = cls.test_data['ip_a_user']
        cls.ip_b_user = cls.test_data['ip_b_user']
        cls.ip_c_user = cls.test_data['ip_c_user']
        cls.random_ip_user = cls.test_data['random_ip_user']

    @classmethod
    def generate_test_data(cls):
        test_data = {}
        test_data['ip_a'] = cls.get_ip_by_code(code=1)
        test_data['ip_b'] = cls.get_ip_by_code(code=2)
        test_data['ip_c'] = cls.get_ip_by_code(code=3)
        test_data['random_ip'] = cls.get_ip_by_code(random.randint(100, 140))
        test_data['second_random_ip'] = cls.get_ip_by_code(random.randint(500, 600))
        test_data['ip_a_user'] = cls.get_implementing_partner_user(implementing_partner=test_data['ip_a'])
        test_data['ip_b_user'] = cls.get_implementing_partner_user(implementing_partner=cls.get_ip_by_code(code=2))
        test_data['ip_c_user'] = cls.get_implementing_partner_user(implementing_partner=test_data['ip_c'])
        test_data['random_ip_user'] = cls.get_implementing_partner_user(implementing_partner=test_data['random_ip'])
        test_data['second_random_ip_user'] = cls.get_implementing_partner_user(
            implementing_partner=test_data['second_random_ip'])
        test_data['ip_a_client'] = cls.create_client_for_implementing_partner(test_data['ip_a'])
        test_data['ip_b_client'] = cls.create_client_for_implementing_partner(test_data['ip_b'])
        test_data['ip_c_client'] = cls.create_client_for_implementing_partner(test_data['ip_c'])
        test_data['second_random_ip_client'] = cls.create_client_for_implementing_partner(test_data['second_random_ip'])
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
        test_data['random_intervention'] = cls.get_intervention_by_ip_to_ip_client(test_data['second_random_ip_user'],
                                                                                   test_data['second_random_ip_client'])
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
    def get_implementing_partner_user(cls, implementing_partner, save=False):
        user = cls.register_user()
        implementing_partner_user = ImplementingPartnerUser(user=user, implementing_partner=implementing_partner)
        if save:
            implementing_partner_user.save()
        return implementing_partner_user

    @classmethod
    def get_intervention_type_1003(cls):
        return InterventionType.objects.get(code=1003)

    @classmethod
    def create_delegation(cls, delegating_implementing_partner, delegated_implementing_partner, active=True):
        delegating_implementing_partner.save()
        delegated_implementing_partner.save()
        start_date = datetime.now().date()
        end_date = datetime.now() + timedelta(weeks=26)
        if not active:
            start_date = datetime.now() - timedelta(weeks=26)
            end_date = datetime.now() - timedelta(days=1)

        delegation = ServiceDelegation.objects.create(main_implementing_partner=delegating_implementing_partner,
                                                      delegated_implementing_partner=delegated_implementing_partner,
                                                      start_date=start_date,
                                                      end_date=end_date,
                                                      intervention_type=cls.get_intervention_type_1003(),
                                                      created_by=User.objects.get(username='admin'),
                                                      date_created=datetime.now(),
                                                      updated_by=User.objects.get(username='admin'),
                                                      date_updated=datetime.now()
                                                      )
        return delegation

    @classmethod
    def get_intervention_by_ip_to_ip_client(cls, implementing_partner_user, client, voided=False,
                                            intervention_date=datetime.now(), save=None):
        intervention = None
        if save is None:
            intervention = Intervention(client=client,
                                        intervention_type=cls.get_intervention_type_1003(),
                                        intervention_date=intervention_date, voided=voided,
                                        created_by=implementing_partner_user.user, date_created=datetime.now(),
                                        implementing_partner=implementing_partner_user.implementing_partner)
        elif save and save is True:
            client.save()
            intervention = Intervention(client=client,
                                        intervention_type=cls.get_intervention_type_1003(),
                                        intervention_date=intervention_date, voided=voided,
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
    def create_client_for_implementing_partner(cls, implementing_partner, middle_name=None, first_name="Jane",
                                               last_name="Doe",
                                               dreams_id=None, voided=False,
                                               save=False, enrolled_weeks_ago=56, ward=None):
        voided_by = None
        if voided:
            voided_by = User.objects.first()

        client = Client(first_name=first_name, last_name=last_name, implementing_partner=implementing_partner,
                        middle_name=middle_name,
                        date_of_enrollment=(datetime.now() - timedelta(weeks=enrolled_weeks_ago)).date(),
                        dreams_id=dreams_id,
                        voided=voided, voided_by=voided_by)
        if middle_name is not None:
            client.middle_name = middle_name

        if ward is not None:
            client.ward = ward

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
    def create_county(cls, code='199', save=False):
        county = County.objects.create(code=code)
        if save:
            county.save()
        return county

    @classmethod
    def create_sub_county(cls, county, code='299', save=False):
        sub_county = SubCounty.objects.create(code=code, county=county)
        if save:
            sub_county.save()
        return sub_county

    @classmethod
    def create_ward(cls, sub_county, code='399', save=False):
        ward = Ward.objects.create(code=code, sub_county=sub_county)
        if save:
            ward.save()
        return ward

    @classmethod
    def create_test_data_for_ip_clients(cls):
        '''
            ip_x
                ip_user_x
                client_x_1
                    voided_intervention_by_ip_x_to_ip_x_client_1
                client_x_2
                    intervention_by_ip_x_to_ip_x_client_2
                client_x_3
                    intervention_by_ip_x_to_ip_x_client_3
                client_x_4 (voided)
            ip_y
                ip_user_y
                client_y_1
                    intervention_by_ip_z_to_ip_y_client_1
                    voided_intervention_by_ip_y_to_ip_y_client_1
                    intervention_1_by_ip_y_to_ip_y_client_1
                    intervention_2_by_ip_y_to_ip_y_client_1
                    intervention_1_by_ip_x_to_ip_y_client_1
                client_y_2
                    intervention_by_ip_z_to_ip_y_client_2
                client_y_3
                    intervention_by_ip_y_to_ip_y_client_3
                client_y_4 (voided)
                client_y_5
                    intervention_by_ip_z_to_ip_y_client_5 (voided)
                service_delegation from ip_x(active)
                service_delegation from ip_z(inactive)
            ip_z
                ip_user_z
                client_z_1
                    intervention_1_by_ip_z_to_ip_z_client_1
                    voided_intervention_1_by_ip_z_to_ip_z_client_1
                client_z_2
                    intervention_1_by_ip_z_to_ip_z_client_2
                client_z_3
                    intervention_1_by_ip_z_to_ip_z_client_3
                client_z_4 (voided)
                    voided_intervention_1_by_ip_z_to_ip_z_client_4


            Wards

            County X
                sub_county_x_1
                    sub_county_x_1_ward_1
                    sub_county_x_1_ward_2
                sub_county_x_2
                    sub_county_x_2_ward_1
                    sub_county_x_2_ward_2
            County Y
                sub_county_y_1
                    sub_county_y_1_ward_1
                    sub_county_y_1_ward_2
                sub_county_y_2
                    sub_county_y_2_ward_1
                    sub_county_y_2_ward_2
        '''
        test_data_for_ip_clients = {}
        # counties
        test_data_for_ip_clients['county_x'] = cls.create_county(code=200, save=True)
        test_data_for_ip_clients['county_y'] = cls.create_county(code=201, save=True)
        # sub counties
        test_data_for_ip_clients['sub_county_x_1'] = cls.create_sub_county(code=300,
                                                                           county=test_data_for_ip_clients['county_x'],
                                                                           save=True)
        test_data_for_ip_clients['sub_county_x_2'] = cls.create_sub_county(code=301,
                                                                           county=test_data_for_ip_clients['county_x'],
                                                                           save=True)

        test_data_for_ip_clients['sub_county_y_1'] = cls.create_sub_county(code=305,
                                                                           county=test_data_for_ip_clients['county_y'],
                                                                           save=True)
        test_data_for_ip_clients['sub_county_y_2'] = cls.create_sub_county(code=306,
                                                                           county=test_data_for_ip_clients['county_y'],
                                                                           save=True)

        # wards
        test_data_for_ip_clients['sub_county_x_1_ward_1'] = cls.create_ward(code=400,
                                                                            sub_county=test_data_for_ip_clients[
                                                                                'sub_county_x_1'],
                                                                            save=True)
        test_data_for_ip_clients['sub_county_x_1_ward_2'] = cls.create_ward(code=401,
                                                                            sub_county=test_data_for_ip_clients[
                                                                                'sub_county_x_1'],
                                                                            save=True)
        test_data_for_ip_clients['sub_county_x_2_ward_2'] = cls.create_ward(code=402,
                                                                            sub_county=test_data_for_ip_clients[
                                                                                'sub_county_x_2'],
                                                                            save=True)
        test_data_for_ip_clients['sub_county_x_2_ward_2'] = cls.create_ward(code=403,
                                                                            sub_county=test_data_for_ip_clients[
                                                                                'sub_county_x_2'],
                                                                            save=True)

        test_data_for_ip_clients['sub_county_y_1_ward_1'] = cls.create_ward(code=404,
                                                                            sub_county=test_data_for_ip_clients[
                                                                                'sub_county_y_1'],
                                                                            save=True)
        test_data_for_ip_clients['sub_county_y_1_ward_2'] = cls.create_ward(code=405,
                                                                            sub_county=test_data_for_ip_clients[
                                                                                'sub_county_y_1'],
                                                                            save=True)
        test_data_for_ip_clients['sub_county_y_2_ward_1'] = cls.create_ward(code=406,
                                                                            sub_county=test_data_for_ip_clients[
                                                                                'sub_county_y_2'],
                                                                            save=True)
        test_data_for_ip_clients['sub_county_y_2_ward_2'] = cls.create_ward(code=407,
                                                                            sub_county=test_data_for_ip_clients[
                                                                                'sub_county_y_2'],
                                                                            save=True)

        #  ips
        test_data_for_ip_clients['ip_x'] = cls.get_ip_by_code(code=100, save=True)
        test_data_for_ip_clients['ip_y'] = cls.get_ip_by_code(code=101, save=True)
        test_data_for_ip_clients['ip_z'] = cls.get_ip_by_code(code=102, save=True)
        # ip users
        test_data_for_ip_clients['ip_x_user'] = cls.get_implementing_partner_user(
            implementing_partner=test_data_for_ip_clients['ip_x'], save=True)
        test_data_for_ip_clients['ip_y_user'] = cls.get_implementing_partner_user(
            implementing_partner=test_data_for_ip_clients['ip_y'], save=True)
        test_data_for_ip_clients['ip_z_user'] = cls.get_implementing_partner_user(
            implementing_partner=test_data_for_ip_clients['ip_z'], save=True)
        # ip clients
        test_data_for_ip_clients['client_x_1'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_x'], first_name='Client X', middle_name='Doe', last_name='One',
            dreams_id='100/1232/1', save=True,
            enrolled_weeks_ago=60, ward=test_data_for_ip_clients['sub_county_x_1_ward_1'])
        test_data_for_ip_clients['client_x_2'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_x'], first_name='Client X', middle_name='Doe', last_name='2',
            dreams_id='100/1232/2', save=True,
            ward=test_data_for_ip_clients['sub_county_x_1_ward_1'])
        test_data_for_ip_clients['client_x_3'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_x'], first_name='Client X', last_name='3', dreams_id='100/1232/3', save=True,
            ward=test_data_for_ip_clients['sub_county_x_1_ward_2'])
        test_data_for_ip_clients['client_x_4'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_x'], first_name='Client X', last_name='4', dreams_id='100/1232/4', voided=True,
            save=True, ward=test_data_for_ip_clients['sub_county_x_1_ward_1'])
        test_data_for_ip_clients['client_y_1'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_y'], first_name='Client Y', last_name='One', dreams_id='101/1232/1', save=True,
            ward=test_data_for_ip_clients['sub_county_y_2_ward_1'])
        test_data_for_ip_clients['client_y_2'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_y'], first_name='Client Y', middle_name='Doe', last_name='2',
            dreams_id='101/1232/2', save=True,
            ward=test_data_for_ip_clients['sub_county_y_2_ward_1'])
        test_data_for_ip_clients['client_y_3'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_y'], first_name='Client Y', last_name='3', dreams_id='101/1232/3', save=True,
            ward=test_data_for_ip_clients['sub_county_y_2_ward_2'])
        test_data_for_ip_clients['client_y_4'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_y'], first_name='Client Y', last_name='4', dreams_id='101/1232/4', voided=True,
            save=True, ward=test_data_for_ip_clients['sub_county_y_2_ward_1'])
        test_data_for_ip_clients['client_y_5'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_y'], first_name='Client Y', last_name='5', dreams_id='101/1232/5', save=True)
        test_data_for_ip_clients['client_z_1'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_z'], first_name='ClientZ', last_name='One', dreams_id='102/1232/1', save=True)
        test_data_for_ip_clients['client_z_2'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_z'], first_name='Client Z', last_name='2', dreams_id='102/1232/2', save=True)
        test_data_for_ip_clients['client_z_3'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_z'], first_name='Client Z', last_name='3', dreams_id='102/1232/3', save=True)
        test_data_for_ip_clients['client_z_4'] = cls.create_client_for_implementing_partner(
            test_data_for_ip_clients['ip_z'], first_name='Client Z', last_name='4', dreams_id='102/1232/4', voided=True,
            save=True)

        # ip client interventions
        test_data_for_ip_clients[
            'intervention_by_ip_z_to_ip_y_client_1'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_z_user'],
            test_data_for_ip_clients['client_y_1'],
            save=True
        )
        test_data_for_ip_clients[
            'intervention_by_ip_z_to_ip_y_client_2'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_z_user'],
            test_data_for_ip_clients['client_y_2'],
            save=True
        )
        test_data_for_ip_clients[
            'voided_intervention_by_ip_z_to_ip_y_client_5'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_z_user'],
            test_data_for_ip_clients['client_y_5'],
            voided=True,
            save=True
        )

        test_data_for_ip_clients[
            'voided_intervention_by_ip_x_to_ip_x_client_1'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_x_user'],
            test_data_for_ip_clients['client_x_1'],
            voided=True,
            save=True
        )

        test_data_for_ip_clients[
            'voided_intervention_by_ip_x_to_ip_x_client_2'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_x_user'],
            test_data_for_ip_clients['client_x_2'],
            save=True
        )

        test_data_for_ip_clients[
            'voided_intervention_by_ip_x_to_ip_x_client_3'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_x_user'],
            test_data_for_ip_clients['client_x_3'],
            save=True
        )

        test_data_for_ip_clients[
            'intervention_by_ip_z_to_ip_z_client_1'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_z_user'],
            test_data_for_ip_clients['client_z_1'],
            save=True
        )
        test_data_for_ip_clients[
            'intervention_by_ip_z_to_ip_z_client_2'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_z_user'],
            test_data_for_ip_clients['client_z_2'],
            save=True
        )

        test_data_for_ip_clients[
            'intervention_by_ip_z_to_ip_z_client_3'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_z_user'],
            test_data_for_ip_clients['client_z_3'],
            save=True
        )

        test_data_for_ip_clients[
            'intervention_by_ip_z_to_ip_z_client_4'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_z_user'],
            test_data_for_ip_clients['client_z_4'],
            voided=True,
            save=True
        )

        test_data_for_ip_clients[
            'intervention_by_ip_y_to_ip_y_client_3'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_y_user'],
            test_data_for_ip_clients['client_y_3'],
            save=True
        )

        test_data_for_ip_clients[
            'intervention_by_ip_y_to_ip_y_client_1'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_y_user'],
            test_data_for_ip_clients['client_y_1'],
            save=True
        )

        test_data_for_ip_clients[
            'intervention_2_by_ip_y_to_ip_y_client_1'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_y_user'],
            test_data_for_ip_clients['client_y_1'],
            intervention_date=datetime.now().date() - timedelta(days=4),
            save=True
        )

        test_data_for_ip_clients[
            'voided_intervention_by_ip_y_to_ip_y_client_1'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_y_user'],
            test_data_for_ip_clients['client_y_1'],
            intervention_date=datetime.now().date() - timedelta(days=7),
            voided=True,
            save=True
        )

        test_data_for_ip_clients[
            'intervention_1_by_ip_x_to_ip_y_client_1'] = cls.get_intervention_by_ip_to_ip_client(
            test_data_for_ip_clients['ip_x_user'],
            test_data_for_ip_clients['client_y_1'],
            save=True
        )

        return test_data_for_ip_clients

    def _generate_dummy_request(self, user=None):
        factory = RequestFactory()
        request = factory.get('/')
        if user:
            request.user = user
        return request

    def setup_request(self, request, user):

        request.user = user

        """Annotate a request object with a session"""
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        """Annotate a request object with a messages"""
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        return request

import unittest

from django.test import RequestFactory

#from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
#    InterventionDelegationTestCase
from DreamsApp.views import get_search_criteria, get_delegated_intervention_type_codes


class ViewTestCase(): #(InterventionDelegationTestCase):

    def test_get_search_criteria(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_user = test_data['ip_x_user']
        request_data = {'ward': 1, 'sub_county': 3, 'county': 2}
        dummy_request = self._generate_dummy_post_request(ip_user.user, request_data)
        request = self.setup_request(dummy_request, ip_user.user)
        expected_search_criteria = {'search_text': 'Mary', 'ward': 1}
        search_creteria = get_search_criteria('Mary', True, request)
        for key in expected_search_criteria.keys():
           self.assertEquals(search_creteria[key], expected_search_criteria[key])
    """
    def test_get_delegated_intervention_types(self):

        ip_a_client = self.test_data['ip_a_client']
        intervention_type_1003 = self.get_intervention_type(code=1003)
        delegating_ip = ip_a_client.implementing_partner
        delegated_ip = self.ip_b_user.implementing_partner
        self.create_delegation(delegating_implementing_partner=self.ip_a,
                               delegated_implementing_partner=self.ip_b)
        delegated_intervention_type_ids = get_delegated_intervention_type_codes(ip_a_client.implementing_partner, self.ip_b_user.implementing_partner)
        self.assertEquals([intervention_type_1003.code], delegated_intervention_type_ids,
                      'Expected only intervention code 1003 to be delegated')

        delegated_intervention_type_ids = get_delegated_intervention_type_codes(ip_a_client.implementing_partner,
                                                                                ip_a_client.implementing_partner)
        self.assertEquals([], delegated_intervention_type_ids,
                          'Expected no delegated interventions for the same client')

        delegated_intervention_type_ids = get_delegated_intervention_type_codes(self.ip_b,
                                                                                self.ip_a)
        self.assertEquals([], delegated_intervention_type_ids,
                          'Expected no delegated interventions from ip b to ip a')
    """
    def _generate_dummy_post_request(self, user=None, request_data={}):
        factory = RequestFactory()
        request = factory.post('/', request_data)
        if user:
            request.user = user
        return request




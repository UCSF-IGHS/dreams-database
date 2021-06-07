import unittest

from django.test import RequestFactory

from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase
from DreamsApp.views import get_search_criteria


class ViewTestCase(InterventionDelegationTestCase):

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

    def _generate_dummy_post_request(self, user=None, request_data={}):
        factory = RequestFactory()
        request = factory.post('/', request_data)
        if user:
            request.user = user
        return request




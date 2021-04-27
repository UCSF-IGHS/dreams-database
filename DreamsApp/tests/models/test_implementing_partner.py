from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class ImplementingPartnerTestCase(InterventionDelegationTestCase):

    def test_get_active_delegating_implementing_partners(self):
        test_data = self.create_test_data_for_ip_clients()
        active_delegation = self.create_delegation(delegating_implementing_partner=test_data['ip_x'],
                               delegated_implementing_partner=test_data['ip_y'])
        active_delegation_2 = self.create_delegation(delegating_implementing_partner=test_data['ip_x'],
                                                   delegated_implementing_partner=test_data['ip_z'])
        inactive_delegation = self.create_delegation(delegating_implementing_partner=test_data['ip_z'],
                               delegated_implementing_partner=test_data['ip_y'], active=False)
        delegated_ip = test_data['ip_y']
        active_delegating_ips = delegated_ip.get_active_delegating_implementing_partners
        self.assertEquals(active_delegating_ips, [test_data['ip_x']])

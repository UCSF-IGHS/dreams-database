
# Transfer constants
TRANSFER_INITIATED_STATUS = 1
TRANSFER_ACCEPTED_STATUS = 2
TRANSFER_REJECTED_STATUS = 3

# Enrolment constants
MINIMUM_ENROLMENT_AGE = 9
MAXIMUM_ENROLMENT_AGE = 24

# Referral constants
REFERRAL_PENDING_STATUS = 1
REFERRAL_COMPLETED_STATUS = 2
REFERRAL_REJECTED_STATUS = 3
REFERRAL_EXPIRED_STATUS = 4

INTERVENTION_BY_REFERRAL = '1'
INTERVENTION_NOT_BY_REFERRAL = '0'

RAW_ENROLMENT_EXPORT_COLUMNS = """*"""

RAW_INTERVENTION_EXPORT_COLUMNS = """i.client_id,
                                        i.dreams_id,
                                        CONCAT_WS(" ",i.first_name, i.middle_name, i.last_name) AS client_name,
                                        i.date_of_birth,
                                        i.implementing_partner,
                                        i.implementing_partner_id,
                                        i.county_of_residence,
                                        i.sub_county,
                                        i.ward,
                                        i.village,
                                        i.date_of_enrollment as date_of_enrollment,
                                        DATE(i.intervention_date) date_of_intervention,
                                        DATE(i.date_created) date_created,
                                        i.intervention as intervention_type,
                                        i.intervention_category,
                                        i.hts_result,
                                        i.pregnancy_test_result,
                                        i.client_ccc_number,
                                        i.date_linked_to_ccc,
                                        i.no_of_sessions_attended,
                                        i.comment,
                                        i.current_age,
                                        i.age_at_intervention,
                                        i.external_organisation,
                                        i.external_organisation_other,
                                        (CASE WHEN i.referred_client = 1 THEN 'Yes' ELSE 'No' END) AS referred_client,
                                        (SELECT name FROM DreamsApp_implementingpartner WHERE id=i.receiving_ip_id LIMIT 1) AS receiving_ip,
                                        i.referral_date,
                                        i.referral_status"""

INDIVIDUAL_CLIENT_SERVICE_LAYERING_COLUMNS = """*"""

INTERVENTION_TRANSFERRED_IN_COLUMNS = """i.client_id, i.dreams_id, CONCAT_WS(" ",i.first_name, i.middle_name, i.last_name) AS client_name, i.date_of_birth, 
          i.implementing_partner,  i.implementing_partner_id,i.county_of_residence,i.sub_county,
          i.ward, i.village, i.date_of_enrollment as date_of_enrollment, DATE(i.intervention_date) date_of_intervention, 
          DATE(i.date_created) date_created, i.intervention as intervention_type, i.intervention_category, i.hts_result,
          i.pregnancy_test_result, i.client_ccc_number, i.date_linked_to_ccc,
          i.no_of_sessions_attended, i.comment, i.current_age, i.age_at_intervention, i.external_organisation, i.external_organisation_other, 
          (CASE WHEN i.referred_client = 1 THEN 'Yes' ELSE 'No' END) AS referred_client, 
          (SELECT name FROM DreamsApp_implementingpartner WHERE id=i.receiving_ip_id LIMIT 1) AS receiving_ip, i.referral_date, i.referral_status"""
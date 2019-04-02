
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

RAW_ENROLMENT_EXPORT_COLUMNS = """client_id, first_name, middle_name, last_name, date_of_birth, verification_document_id,
        verification_document, verification_document_other, verification_doc_no, date_of_enrollment, phone_number, dss_id_number, informal_settlement,
        village, landmark, dreams_id, guardian_name, relationship_with_guardian, guardian_phone_number, guardian_national_id, county_of_residence_id,
        county_of_residence, implementing_partner_id, implementing_partner, marital_status_id, marital_status, sub_county_id, ward_id, ward_name, sub_county_code,
        sub_county_name, county_code, county_name, head_of_household_id, head_of_household, head_of_household_other, age_of_household_head, is_father_alive, father_alive,
        is_mother_alive, mother_alive, is_parent_chronically_ill, parent_chronically_ill, main_floor_material_id, main_floor_material, main_floor_material_other,
        main_roof_material_id, main_roof_material, main_roof_material_other, main_wall_material_id, main_wall_material, main_wall_material_other, source_of_drinking_water_id,
        source_of_drinking_water, source_of_drinking_water_other, no_of_adults, no_of_females, no_of_males, no_of_children, currently_in_ct_program_id, currently_in_ct_program,
        current_ct_program, ever_enrolled_in_ct_program_id, ever_enrolled_in_ct_program, ever_missed_full_day_food_in_4wks_id, ever_missed_full_day_food_in_4wks, has_disability_id,
        has_disability, no_of_days_missed_food_in_4wks_id, no_of_days_missed_food_in_4wks, disability_types, no_of_people_in_household, age_at_first_sexual_encounter,
        sex_partners_in_last_12months, age_of_last_partner_id, age_of_last_partner, age_of_second_last_partner_id, age_of_second_last_partner, age_of_third_last_partner_id,
        age_of_third_last_partner, ever_had_sex_id, ever_had_sex, has_sexual_partner_id, has_sexual_partner, know_last_partner_hiv_status_id, know_last_partner_hiv_status,
        know_second_last_partner_hiv_status_id, know_second_last_partner_hiv_status, know_third_last_partner_hiv_status_id, know_third_last_partner_hiv_status, last_partner_circumcised_id,
        last_partner_circumcised, received_money_gift_for_sex_id, received_money_gift_for_sex, second_last_partner_circumcised_id, second_last_partner_circumcised,
        third_last_partner_circumcised_id, third_last_partner_circumcised, used_condom_with_last_partner_id, used_condom_with_last_partner, used_condom_with_second_last_partner_id,
        used_condom_with_second_last_partner, used_condom_with_third_last_partner_id, used_condom_with_third_last_partner, no_of_biological_children, anc_facility_name,
        known_fp_method_other, current_fp_method_other, reason_not_using_fp_other, current_anc_enrollment_id, current_anc_enrollment, current_fp_method_id, current_fp_method,
        currently_pregnant_id, currently_pregnant, currently_use_modern_fp_id, currently_use_modern_fp, fp_methods_awareness_id, fp_methods_awareness, has_biological_children_id,
        has_biological_children, reason_not_using_fp_id, reason_not_using_fp, known_fp_methods, drug_abuse_last_12months_other, drug_used_last_12months_other, drug_abuse_last_12months_id,
        drug_abuse_last_12months, frequency_of_alcohol_last_12months_id, frequency_of_alcohol_last_12months, produced_alcohol_last_12months_id, produced_alcohol_last_12months,
        used_alcohol_last_12months_id, used_alcohol_last_12months, drugs_used_in_last_12_months, dreams_program_other, programmes_enrolled, gbv_help_provider_other,
        preferred_gbv_help_provider_other, economic_threat_ever_id, economic_threat_ever, economic_threat_last_3months_id, economic_threat_last_3months, humiliated_ever_id,
        humiliated_ever, humiliated_last_3months_id, humiliated_last_3months, insulted_ever_id, insulted_ever, insulted_last_3months_id, insulted_last_3months, knowledge_of_gbv_help_centres_id,
        knowledge_of_gbv_help_centres, physical_violence_ever_id, physical_violence_ever, physical_violence_last_3months_id, physical_violence_last_3months,
        physically_forced_other_sex_acts_ever_id, physically_forced_other_sex_acts_ever, physically_forced_other_sex_acts_last_3months_id, physically_forced_other_sex_acts_last_3months,
        physically_forced_sex_ever_id, physically_forced_sex_ever, physically_forced_sex_last_3months_id, physically_forced_sex_last_3months, seek_help_after_gbv_id, seek_help_after_gbv,
        threatened_for_sexual_acts_ever_id, threatened_for_sexual_acts_ever, threatened_for_sexual_acts_last_3months_id, threatened_for_sexual_acts_last_3months, threats_to_hurt_ever_id,
        threats_to_hurt_ever, threats_to_hurt_last_3months_id, threats_to_hurt_last_3months, providers_sought, preferred_providers, current_school_name, current_class, current_school_level_other,
        current_education_supporter_other, reason_not_in_school_other, dropout_class, life_wish_other, current_income_source_other, banking_place_other, banking_place_id, banking_place,
        current_income_source_id, current_income_source, current_school_level_id, current_school_level, current_school_type_id, current_school_type, currently_in_school_id, currently_in_school,
        dropout_school_level_id, dropout_school_level, has_savings_id, has_savings, last_time_in_school_id, last_time_in_school, life_wish_id, life_wish, reason_not_in_school_id,
        reason_not_in_school, current_edu_supporter_list, care_facility_enrolled, reason_not_in_hiv_care_other, reason_never_tested_for_hiv_other, enrolled_in_hiv_care_id,
        enrolled_in_hiv_care, ever_tested_for_hiv_id, ever_tested_for_hiv, knowledge_of_hiv_test_centres_id, knowledge_of_hiv_test_centres, last_test_result_id, last_test_result,
        period_last_tested_id, period_last_tested, reason_not_in_hiv_care_id, reason_not_in_hiv_care, reason_not_tested_for_hiv, voided, date_voided, exit_status, exit_date, exit_reason,
        age_at_enrollment, current_age, (CASE WHEN is_date_of_birth_estimated = 1 THEN 'Yes' ELSE 'No' END) AS is_date_of_birth_estimated, transfer_status_id, transfer_status_name, transfer_completion_date, date_created, date_changed"""

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
-- point of entry for sync stored procedures
-- gets called by event and calls other procedures
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_sync_odk_dreams_data$$
CREATE PROCEDURE sp_sync_odk_dreams_data()
BEGIN

  DECLARE no_more_rows BOOLEAN;
  DECLARE record_uuid VARCHAR(100);
  DECLARE record_type VARCHAR(100);
  DECLARE v_row_count INT(11);

  DECLARE odk_enrollment_records CURSOR FOR
    -- SELECT uuid FROM odk_dreams_sync WHERE synced=0 and form='enrollment' LIMIT 50;
    SELECT uuid, form FROM odk_dreams_sync WHERE synced=0 LIMIT 50;
  DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET no_more_rows = TRUE;

  OPEN odk_enrollment_records;
  SET v_row_count = FOUND_ROWS();

  IF v_row_count > 0 THEN
    get_enrollment_record: LOOP
    FETCH odk_enrollment_records INTO record_uuid, record_type;

    IF no_more_rows THEN
      CLOSE odk_enrollment_records;
      LEAVE get_enrollment_record;
    END IF;

    CALL sp_sync_client_data(record_uuid, record_type);

  END LOOP get_enrollment_record;
  ELSE
    SELECT "NO ROWS WERE FOUND";
  END IF;

END
$$
DELIMITER ;

-- --------------------------------------------------

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_sync_client_data$$
CREATE PROCEDURE sp_sync_client_data(IN recordUUID VARCHAR(100), IN recordType VARCHAR(100))
BEGIN
  DECLARE exec_status INT(11) DEFAULT 1;
  DECLARE client_id INT(11);
  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
      SET exec_status = -1;
      ROLLBACK;
    END;
  -- perform all procedure calls within a transaction
  START TRANSACTION;

  -- Call relevant procedures depending on record type
  IF recordType='enrollment' THEN
    CALL sp_demographic_data(recordUUID);
    SET client_id = LAST_INSERT_ID();
    CALL sp_individual_and_household_data(recordUUID, client_id);
    CALL sp_sexuality_data(recordUUID, client_id);
    CALL sp_reproductive_health_data(recordUUID, client_id);
    CALL sp_drug_use_data(recordUUID, client_id);
    CALL sp_program_participation_data(recordUUID, client_id);
    CALL sp_gbv_data(recordUUID, client_id);
    CALL sp_education_and_employment(recordUUID, client_id);
    CALL sp_hiv_testing(recordUUID, client_id);
  ELSE
    CALL sp_ct_home_visit_verification_data(recordUUID);
  END IF ;

  -- commit all inserts if all procedure calls are successful
  UPDATE odk_dreams_sync SET synced=exec_status WHERE uuid=recordUUID;
  COMMIT;

END;
  $$
DELIMITER ;

-- re-populate dreams_dev.odk_dreams_sync table
DELETE from dreams_dev.odk_dreams_sync;
INSERT INTO dreams_dev.odk_dreams_sync (uuid, form) select _PARENT_AURI, 'enrollment' from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE2;
INSERT INTO dreams_dev.odk_dreams_sync (uuid, form) select _URI, 'home_visit' from odk_aggregate.CT_HOME_VISIT_VERFICATION_FORM_CORE ;


-- ----------------------------------------------------- ------------------------------------
CREATE TEMPORARY TABLE IF NOT EXISTS odk_enrollment_dump AS (
SELECT
d.first_name,d.middle_name,d.last_name,d.date_of_birth, verification_document_id,d.verification_doc_no,d.date_of_enrollment,d.phone_number,
  d.dss_id_number,d.informal_settlement,d.village,d.landmark,d.dreams_id,d.guardian_name,d.relationship_with_guardian,d.guardian_phone_number,
  d.guardian_national_id,d.date_created,d.county_of_residence_id,d.implementing_partner_id,d.marital_status_id,d.sub_county_id,ward_id,
i.head_of_household_id, i.head_of_household_other,i.age_of_household_head, i.is_father_alive, i.is_mother_alive, i.is_parent_chronically_ill,
  i.main_floor_material_id, i.main_floor_material_other, i.main_roof_material_id, i.main_roof_material_other, i.main_wall_material_id, i.main_wall_material_other,
  i.source_of_drinking_water_id,i.source_of_drinking_water_other, i.no_of_adults, i.no_of_females, i.no_of_males, i.no_of_children,
  i.currently_in_ct_program_id, i.current_ct_program, i.ever_enrolled_in_ct_program_id, i.ever_missed_full_day_food_in_4wks_id, i.has_disability_id,
  i.no_of_days_missed_food_in_4wks_id,
s.age_at_first_sexual_encounter,s.sex_partners_in_last_12months,s.age_of_last_partner_id,s.age_of_second_last_partner_id,
  s.age_of_third_last_partner_id,s.ever_had_sex_id,s.has_sexual_partner_id,s.know_last_partner_hiv_status_id,
  s.know_second_last_partner_hiv_status_id,s.know_third_last_partner_hiv_status_id,s.last_partner_circumcised_id,
  s.received_money_gift_for_sex_id,s.second_last_partner_circumcised_id,s.third_last_partner_circumcised_id,s.used_condom_with_last_partner_id,
  s.used_condom_with_second_last_partner_id,s.used_condom_with_third_last_partner_id,
rh.no_of_biological_children,rh.anc_facility_name,rh.known_fp_method_other,rh.current_fp_method_other,rh.reason_not_using_fp_other,
rh.current_anc_enrollment_id,rh.current_fp_method_id,rh.currently_pregnant_id,rh.currently_use_modern_fp_id,rh.fp_methods_awareness_id,
rh.has_biological_children_id,rh.reason_not_using_fp_id, rh.known_fp_methods,
dr.drug_abuse_last_12months_other,dr.drug_used_last_12months_other,dr.drug_abuse_last_12months_id,dr.frequency_of_alcohol_last_12months_id,
  dr.produced_alcohol_last_12months_id,dr.used_alcohol_last_12months_id ,
 p.dreams_program_other,p.client_id ,
gbv.gbv_help_provider_other,gbv.preferred_gbv_help_provider_other,gbv.economic_threat_ever_id,gbv.economic_threat_last_3months_id,
gbv.humiliated_ever_id,gbv.humiliated_last_3months_id,gbv.insulted_ever_id,gbv.insulted_last_3months_id,
gbv.knowledge_of_gbv_help_centres_id,gbv.physical_violence_ever_id,gbv.physical_violence_last_3months_id,
gbv.physically_forced_other_sex_acts_ever_id,gbv.physically_forced_other_sex_acts_last_3months_id,
gbv.physically_forced_sex_ever_id,gbv.physically_forced_sex_last_3months_id,gbv.seek_help_after_gbv_id,
gbv.threatened_for_sexual_acts_ever_id,gbv.threatened_for_sexual_acts_last_3months_id,gbv.threats_to_hurt_ever_id,
gbv.threats_to_hurt_last_3months_id,
edu.current_school_name,edu.current_class,edu.current_school_level_other,edu.current_education_supporter_other,
edu.reason_not_in_school_other,edu.dropout_class,edu.life_wish_other,edu.current_income_source_other,
edu.banking_place_other,edu.banking_place_id,edu.current_income_source_id,edu.current_school_level_id,
edu.current_school_type_id,edu.currently_in_school_id,edu.dropout_school_level_id,edu.has_savings_id,edu.last_time_in_school_id,
edu.life_wish_id,edu.reason_not_in_school_id,
hiv.care_facility_enrolled,hiv.reason_not_in_hiv_care_other,hiv.reason_never_tested_for_hiv_other,hiv.enrolled_in_hiv_care_id,
hiv.ever_tested_for_hiv_id,hiv.knowledge_of_hiv_test_centres_id,hiv.last_test_result_id,hiv.period_last_tested_id,
hiv.reason_not_in_hiv_care_id
FROM
DreamsApp_client AS d
INNER JOIN DreamsApp_clientindividualandhouseholddata i ON i.client_id = d.id
INNER JOIN DreamsApp_clientsexualactivitydata s ON s.client_id = d.id
LEFT OUTER JOIN (
SELECT *
FROM DreamsApp_clientreproductivehealthdata rh
LEFT OUTER JOIN
(
SELECT
fp.clientreproductivehealthdata_id    AS rh_id,
group_concat(familyplanningmethod_id) AS known_fp_methods
FROM DreamsApp_clientreproductivehealthdata_known_fp_method fp
LEFT OUTER JOIN DreamsApp_clientreproductivehealthdata rh
ON fp.clientreproductivehealthdata_id = rh.id
GROUP BY fp.clientreproductivehealthdata_id
) fpm ON fpm.rh_id = rh.id) rh ON rh.client_id = d.id
LEFT OUTER JOIN (
SELECT *
FROM DreamsApp_clientdrugusedata dd
LEFT OUTER JOIN
(
SELECT
d.clientdrugusedata_id  AS dd_id,
group_concat(d.drug_id) AS drugs_used_in_last_12_months
FROM DreamsApp_clientdrugusedata_drug_used_last_12months d
LEFT OUTER JOIN DreamsApp_clientdrugusedata inner_dd ON d.clientdrugusedata_id = inner_dd.id
GROUP BY dd_id
) d ON d.dd_id = dd.id) dr ON dr.client_id = d.id
INNER JOIN (SELECT *
FROM DreamsApp_clientparticipationindreams pp
LEFT OUTER JOIN
(
SELECT
dp.clientparticipationindreams_id   AS pr_id,
group_concat(dp.dreamsprogramme_id) AS programmes_enrolled
FROM DreamsApp_clientparticipationindreams_dreams_program dp
LEFT OUTER JOIN DreamsApp_clientparticipationindreams inner_pp
ON dp.clientparticipationindreams_id = inner_pp.id
GROUP BY pr_id
) pr ON pr.pr_id = pp.id) p ON p.client_id = d.id
INNER JOIN (SELECT
gbv.*,
providers.provider_list   AS providers_sought,
p_providers.provider_list AS preferred_providers
FROM DreamsApp_clientgenderbasedviolencedata gbv
LEFT OUTER JOIN (
SELECT
  provider.clientgenderbasedviolencedata_id AS rec_id,
  group_concat(provider.gbvhelpprovider_id) AS provider_list
FROM DreamsApp_clientgenderbasedviolencedata_gbv_help_provider provider
GROUP BY rec_id
) providers ON providers.rec_id = gbv.id
LEFT OUTER JOIN (
SELECT
  provider.clientgenderbasedviolencedata_id AS rec_id,
  group_concat(provider.gbvhelpprovider_id) AS provider_list
FROM DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_p1bce provider
GROUP BY rec_id
) p_providers ON p_providers.rec_id = gbv.id
GROUP BY gbv.id) gbv ON gbv.client_id = d.id
INNER JOIN (SELECT
ed.*,
edu_sup.current_edu_supporter_list
FROM DreamsApp_clienteducationandemploymentdata ed
LEFT OUTER JOIN (
SELECT
  s.clienteducationandemploymentdata_id AS rec_id,
  group_concat(educationsupporter_id)   AS current_edu_supporter_list
FROM DreamsApp_clienteducationandemploymentdata_current_educationebf4 s
GROUP BY rec_id
) edu_sup ON edu_sup.rec_id = ed.id
GROUP BY ed.id) edu ON edu.client_id = d.id
INNER JOIN (SELECT
hiv_d.*,
rn_not_tested.reason_not_tested_for_hiv
FROM DreamsApp_clienthivtestingdata hiv_d
LEFT OUTER JOIN (
SELECT
  rn.clienthivtestingdata_id                AS rec_id,
  group_concat(rn.reasonnottestedforhiv_id) AS reason_not_tested_for_hiv
FROM DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv rn
GROUP BY rec_id
) rn_not_tested ON rn_not_tested.rec_id = hiv_d.id
GROUP BY hiv_d.id) hiv ON hiv.client_id = d.id
);

-- ------------------


call sp_ct_home_visit_verification_data('uuid:a17568e7-7136-46de-bf12-63a805d0d173');
call sp_ct_home_visit_verification_data('uuid:f4481035-bba0-4289-b631-0040b4e2beb1');


/*you must alter the permissions for user mysqld. start by running the following command sudo aa-status to check your user status and authorized directories.
if you want to change permissions, edit /etc/apparmor.d/usr.sbin.mysqld and insert the directories you want.

you must then restart apparmor sudo /etc/init.d/apparmor restart
This is legit. Thanks for posting! For the impatient, and/or those who want to do a quick command, mysqldump -T for instance, service apparmor teardown will turn it off. When done, you can service apparmor start and restore life back to normal


*/

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_ct_home_visit_verification_data$$
CREATE PROCEDURE sp_ct_home_visit_verification_data(IN recordUUID VARCHAR(100))
BEGIN
DECLARE ct_home_visit_recordID INT(11);

INSERT INTO dreams_dev.DreamsApp_homevisitverification
(
client_name,
dreams_id,
village,
physical_address,
visit_date,
staff_name,
source_of_livelihood_other,
main_floor_material_other,
main_roof_material_other,
main_wall_material_household_other,
main_wall_material_house_other,
source_of_drinking_water_other,
preferred_beneficiary_name,
preferred_beneficiary_relationship,
preferred_beneficiary_id_no,
household_description,
age_of_household_head_id,
caretaker_illness_id,
implementing_partner_id,
main_floor_material_id,
main_roof_material_id,
main_wall_material_house_id,
main_wall_material_household_id,
no_of_days_missed_food_in_4wks_id,
source_of_drinking_water_id,
ward_id
)
select
d.AGYWNAME as client_name,
d.DREAMSID as dreams_id,
d.VILLAGE as village,
d.PHYSICALADDRESS as physical_address,
DATE(d.DATE) as date_of_visit,
d.STAFFNAME as staff_name,
d.Q3SPECIFY as source_of_livelihood_other,
d.Q4SPECIFY as main_floor_material_other,
d.Q6SPECIFY as main_roof_material_other,
d.Q5SPECIFY AS main_wall_material_household_other,
d.Q7SPECIFY as main_wall_material_house_other,
d.Q8SPECIFY as source_of_drinking_water_other,
d.RECEIVERNAME as preferred_beneficiary_name,
d.RECEIVERRELATIONSHIP as preferred_beneficiary_relationship,
d.NATIONAL_ID as preferred_beneficiary_id_no,
d.MY_LONG_TEXT as household_description,
d.Q1 as age_of_household_head_id,
d.Q2 as caretaker_illness_id,
d.IPNAME as implementing_partner_id,
d.Q4 as main_floor_material_id,
d.Q6 as main_roof_material_id,
d.Q7 as main_wall_material_house_id,
d.Q5 as main_wall_material_household_id,
d.Q9 as no_of_days_missed_food_in_4wks_id,
d.Q8 as source_of_drinking_water_id,
d.WARD as ward_id
from odk_aggregate.CT_HOME_VISIT_VERFICATION_FORM_CORE d
where  d._URI=recordUUID;

SET ct_home_visit_recordID = LAST_INSERT_ID();
CALL sp_ct_source_of_livelihood(ct_home_visit_recordID, recordUUID);
END
$$
DELIMITER ;


-- --------------------------------------------

INSERT INTO dreams_dev.DreamsApp_homevisitverification
(
client_name,
dreams_id,
village,
physical_address,
visit_date,
staff_name,
source_of_livelihood_other,
main_floor_material_other,
main_roof_material_other,
main_wall_material_household_other,
main_wall_material_house_other,
source_of_drinking_water_other,
preferred_beneficiary_name,
preferred_beneficiary_relationship,
preferred_beneficiary_id_no,
household_description,
age_of_household_head_id,
caretaker_illness_id,
implementing_partner_id,
main_floor_material_id,
main_roof_material_id,
main_wall_material_house_id,
main_wall_material_household_id,
no_of_days_missed_food_in_4wks_id,
source_of_drinking_water_id,
ward_id
)
select
d.AGYWNAME as client_name,
d.DREAMSID as dreams_id,
d.VILLAGE as village,
d.PHYSICALADDRESS as physical_address,
DATE(d.DATE) as date_of_visit,
d.STAFFNAME as staff_name,
d.Q3SPECIFY as source_of_livelihood_other,
d.Q4SPECIFY as main_floor_material_other,
d.Q6SPECIFY as main_roof_material_other,
d.Q5SPECIFY AS main_wall_material_household_other,
d.Q7SPECIFY as main_wall_material_house_other,
d.Q8SPECIFY as source_of_drinking_water_other,
d.RECEIVERNAME as preferred_beneficiary_name,
d.RECEIVERRELATIONSHIP as preferred_beneficiary_relationship,
d.NATIONAL_ID as preferred_beneficiary_id_no,
d.MY_LONG_TEXT as household_description,
d.Q1 as age_of_household_head_id,
d.Q2 as caretaker_illness_id,
d.IPNAME as implementing_partner_id,
d.Q4 as main_floor_material_id,
d.Q6 as main_roof_material_id,
d.Q7 as main_wall_material_house_id,
d.Q5 as main_wall_material_household_id,
d.Q9 as no_of_days_missed_food_in_4wks_id,
d.Q8 as source_of_drinking_water_id,
d.WARD as ward_id
from odk_aggregate.CT_HOME_VISIT_VERFICATION_FORM_CORE d
where  d._URI='uuid:ae8ccdbe-f1bb-4387-ac73-4f3de7cae0b8';
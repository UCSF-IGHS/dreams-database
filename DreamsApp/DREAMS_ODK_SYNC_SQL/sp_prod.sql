-- Data Quality: Mass update of Wards
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_reassign_wards$$
CREATE PROCEDURE sp_reassign_wards(OUT rows_updated INT)
BEGIN

    DECLARE done BOOL DEFAULT FALSE;
    DECLARE dq_id, dq_implementing_partner_id, dq_old_ward_id, dq_new_ward_id INT;
    DECLARE dreams_id_cursor CURSOR FOR SELECT id, `implementing partner id`, `Ward id`, new_ward_id FROM dq_agyw_ward_correction WHERE status = 0;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    SET rows_updated = 0;
    OPEN dreams_id_cursor;

    read_loop: LOOP
      FETCH dreams_id_cursor INTO dq_id, dq_implementing_partner_id, dq_old_ward_id, dq_new_ward_id;
      IF done THEN

        LEAVE read_loop;

      ELSE

        UPDATE DreamsApp_client SET ward_id = dq_new_ward_id WHERE id = dq_id AND implementing_partner_id = dq_implementing_partner_id AND ward_id = dq_old_ward_id;
        UPDATE dq_agyw_ward_correction SET status = 1 WHERE id = dq_id and `Ward id` = dq_old_ward_id;
        SET rows_updated = rows_updated + 1;

      END IF;
    END LOOP;

    CLOSE dreams_id_cursor;
    SELECT @rows_updated;
END;
$$
DELIMITER ;
-- End of Mass update of Wards


-- setup first time setup tables

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_dreamsTablesSetup$$
CREATE PROCEDURE sp_dreamsTablesSetup()
BEGIN

-- defining table to be populated by odk enrollment trigger
# DROP TABLE IF EXISTS dreams_production.odk_dreams_sync;
# CREATE TABLE dreams_production.odk_dreams_sync (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `uuid` varchar(100) NOT NULL DEFAULT '',
#   `synced` int(11) NOT NULL DEFAULT '0',
#   `form` varchar(100) NOT NULL DEFAULT '',
#   date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# );
#
#
# -- defining table for sync log
# DROP TABLE IF EXISTS dreams_production.odk_dreams_sync_log;
# CREATE TABLE dreams_production.odk_dreams_sync_log (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `action` varchar(100) NOT NULL DEFAULT 'Scheduled Update',
#   `last_update` DATETIME,
#   PRIMARY KEY (`id`)
# );

-- create flat table for reporting

DROP TABLE IF EXISTS dreams_production.flat_dreams_enrollment;

CREATE TABLE dreams_production.flat_dreams_enrollment (
client_id INT(11) PRIMARY KEY NOT NULL,
first_name VARCHAR(100),
middle_name VARCHAR(100),
last_name VARCHAR(100),
date_of_birth DATE,
verification_document_id INT(11),
verification_document VARCHAR(50),
verification_document_other VARCHAR(100),
verification_doc_no VARCHAR(50),
date_of_enrollment DATE,
phone_number VARCHAR(15),
dss_id_number VARCHAR(20),
informal_settlement VARCHAR(50),
village VARCHAR(100),
landmark VARCHAR(255),
dreams_id VARCHAR(20),
guardian_name VARCHAR(50),
relationship_with_guardian VARCHAR(50),
guardian_phone_number VARCHAR(15),
guardian_national_id VARCHAR(20),
date_created DATE,
county_of_residence_id INT(11),
county_of_residence VARCHAR(50),
implementing_partner_id INT(11),
implementing_partner VARCHAR(50),
marital_status_id INT(11),
marital_status VARCHAR(50),
sub_county_id INT(11),
ward_id INT(11),
ward_name VARCHAR(50),
sub_county_code INT(11),
sub_county_name VARCHAR(100),
county_code INT(11),
county_name VARCHAR(30),
head_of_household_id INT(11),
head_of_household VARCHAR(50),
head_of_household_other VARCHAR(50),
age_of_household_head INT(11),
is_father_alive INT(11),
father_alive VARCHAR(50),
is_mother_alive INT(11),
mother_alive VARCHAR(50),
is_parent_chronically_ill INT(11),
parent_chronically_ill VARCHAR(50),
main_floor_material_id INT(11),
main_floor_material VARCHAR(50),
main_floor_material_other VARCHAR(50),
main_roof_material_id INT(11),
main_roof_material VARCHAR(50),
main_roof_material_other VARCHAR(50),
main_wall_material_id INT(11),
main_wall_material VARCHAR(50),
main_wall_material_other VARCHAR(50),
source_of_drinking_water_id INT(11),
source_of_drinking_water VARCHAR(50),
source_of_drinking_water_other VARCHAR(50),
no_of_adults INT(11),
no_of_females INT(11),
no_of_males INT(11),
no_of_children INT(11),
currently_in_ct_program_id INT(11),
currently_in_ct_program VARCHAR(50),
current_ct_program VARCHAR(50),
ever_enrolled_in_ct_program_id INT(11),
ever_enrolled_in_ct_program VARCHAR(50),
ever_missed_full_day_food_in_4wks_id INT(11),
ever_missed_full_day_food_in_4wks VARCHAR(50),
has_disability_id INT(11),
has_disability VARCHAR(20),
no_of_days_missed_food_in_4wks_id INT(11),
no_of_days_missed_food_in_4wks VARCHAR(50),
disability_types VARCHAR(20),
no_of_people_in_household INT(11),
age_at_first_sexual_encounter INT(11),
sex_partners_in_last_12months INT(11),
age_of_last_partner_id INT(11),
age_of_last_partner VARCHAR(50),
age_of_second_last_partner_id INT(11),
age_of_second_last_partner VARCHAR(50),
age_of_third_last_partner_id INT(11),
age_of_third_last_partner VARCHAR(50),
ever_had_sex_id INT(11),
ever_had_sex VARCHAR(50),
has_sexual_partner_id INT(11),
has_sexual_partner VARCHAR(50),
know_last_partner_hiv_status_id INT(11),
know_last_partner_hiv_status VARCHAR(50),
know_second_last_partner_hiv_status_id INT(11),
know_second_last_partner_hiv_status VARCHAR(50),
know_third_last_partner_hiv_status_id INT(11),
know_third_last_partner_hiv_status VARCHAR(50),
last_partner_circumcised_id INT(11),
last_partner_circumcised VARCHAR(50),
received_money_gift_for_sex_id INT(11),
received_money_gift_for_sex VARCHAR(50),
second_last_partner_circumcised_id INT(11),
second_last_partner_circumcised VARCHAR(50),
third_last_partner_circumcised_id INT(11),
third_last_partner_circumcised VARCHAR(50),
used_condom_with_last_partner_id INT(11),
used_condom_with_last_partner VARCHAR(50),
used_condom_with_second_last_partner_id INT(11),
used_condom_with_second_last_partner VARCHAR(50),
used_condom_with_third_last_partner_id INT(11),
used_condom_with_third_last_partner VARCHAR(50),
no_of_biological_children INT(11),
anc_facility_name VARCHAR(50),
known_fp_method_other VARCHAR(50),
current_fp_method_other VARCHAR(50),
reason_not_using_fp_other VARCHAR(50),
current_anc_enrollment_id INT(11),
current_anc_enrollment VARCHAR(50),
current_fp_method_id INT(11),
current_fp_method VARCHAR(50),
currently_pregnant_id INT(11),
currently_pregnant VARCHAR(50),
currently_use_modern_fp_id INT(11),
currently_use_modern_fp VARCHAR(50),
fp_methods_awareness_id INT(11),
fp_methods_awareness VARCHAR(50),
has_biological_children_id INT(11),
has_biological_children VARCHAR(50),
reason_not_using_fp_id INT(11),
reason_not_using_fp VARCHAR(50),
known_fp_methods VARCHAR(20),
drug_abuse_last_12months_other VARCHAR(50),
drug_used_last_12months_other VARCHAR(50),
drug_abuse_last_12months_id INT(11),
drug_abuse_last_12months VARCHAR(50),
frequency_of_alcohol_last_12months_id INT(11),
frequency_of_alcohol_last_12months VARCHAR(50),
produced_alcohol_last_12months_id INT(11),
produced_alcohol_last_12months VARCHAR(50),
used_alcohol_last_12months_id INT(11),
used_alcohol_last_12months VARCHAR(50),
drugs_used_in_last_12_months VARCHAR(20),
dreams_program_other VARCHAR(50),
programmes_enrolled VARCHAR(20),
gbv_help_provider_other VARCHAR(50),
preferred_gbv_help_provider_other VARCHAR(50),
economic_threat_ever_id INT(11),
economic_threat_ever VARCHAR(50),
economic_threat_last_3months_id INT(11),
economic_threat_last_3months VARCHAR(50),
humiliated_ever_id INT(11),
humiliated_ever VARCHAR(50),
humiliated_last_3months_id INT(11),
humiliated_last_3months VARCHAR(50),
insulted_ever_id INT(11),
insulted_ever VARCHAR(50),
insulted_last_3months_id INT(11),
insulted_last_3months VARCHAR(50),
knowledge_of_gbv_help_centres_id INT(11),
knowledge_of_gbv_help_centres VARCHAR(50),
physical_violence_ever_id INT(11),
physical_violence_ever VARCHAR(50),
physical_violence_last_3months_id INT(11),
physical_violence_last_3months VARCHAR(50),
physically_forced_other_sex_acts_ever_id INT(11),
physically_forced_other_sex_acts_ever VARCHAR(50),
physically_forced_other_sex_acts_last_3months_id INT(11),
physically_forced_other_sex_acts_last_3months VARCHAR(50),
physically_forced_sex_ever_id INT(11),
physically_forced_sex_ever VARCHAR(50),
physically_forced_sex_last_3months_id INT(11),
physically_forced_sex_last_3months VARCHAR(50),
seek_help_after_gbv_id INT(11),
seek_help_after_gbv VARCHAR(50),
threatened_for_sexual_acts_ever_id INT(11),
threatened_for_sexual_acts_ever VARCHAR(50),
threatened_for_sexual_acts_last_3months_id INT(11),
threatened_for_sexual_acts_last_3months VARCHAR(50),
threats_to_hurt_ever_id INT(11),
threats_to_hurt_ever VARCHAR(50),
threats_to_hurt_last_3months_id INT(11),
threats_to_hurt_last_3months VARCHAR(50),
providers_sought VARCHAR(20),
preferred_providers VARCHAR(20),
current_school_name VARCHAR(50),
current_class VARCHAR(15),
current_school_level_other VARCHAR(50),
current_education_supporter_other VARCHAR(50),
reason_not_in_school_other VARCHAR(50),
dropout_class VARCHAR(15),
life_wish_other VARCHAR(50),
current_income_source_other VARCHAR(50),
banking_place_other VARCHAR(50),
banking_place_id INT(11),
banking_place VARCHAR(50),
current_income_source_id INT(11),
current_income_source VARCHAR(50),
current_school_level_id INT(11),
current_school_level VARCHAR(50),
current_school_type_id INT(11),
current_school_type VARCHAR(50),
currently_in_school_id INT(11),
currently_in_school VARCHAR(50),
dropout_school_level_id INT(11),
dropout_school_level VARCHAR(50),
has_savings_id INT(11),
has_savings VARCHAR(50),
last_time_in_school_id INT(11),
last_time_in_school VARCHAR(50),
life_wish_id INT(11),
life_wish VARCHAR(50),
reason_not_in_school_id INT(11),
reason_not_in_school VARCHAR(50),
current_edu_supporter_list VARCHAR(20),
care_facility_enrolled VARCHAR(50),
reason_not_in_hiv_care_other VARCHAR(50),
reason_never_tested_for_hiv_other VARCHAR(50),
enrolled_in_hiv_care_id INT(11),
enrolled_in_hiv_care VARCHAR(50),
ever_tested_for_hiv_id INT(11),
ever_tested_for_hiv VARCHAR(100),
knowledge_of_hiv_test_centres_id INT(11),
knowledge_of_hiv_test_centres VARCHAR(50),
last_test_result_id INT(11),
last_test_result VARCHAR(50),
period_last_tested_id INT(11),
period_last_tested VARCHAR(50),
reason_not_in_hiv_care_id INT(11),
reason_not_in_hiv_care VARCHAR(50),
reason_not_tested_for_hiv VARCHAR(20),
voided INT(11),
date_voided DATETIME,
exit_status VARCHAR(10),
exit_date DATETIME,
exit_reason VARCHAR(200),
age_at_enrollment INT(11),
current_age INT(11)
);


ALTER DATABASE odk_aggregate CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE odk_aggregate.DREAMS_ENROLMENT_FORM_CORE CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE odk_aggregate.DREAMS_ENROLMENT_FORM_CORE2 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_Q113 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_2_Q204 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_3_Q307 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE odk_aggregate.DREAMS_ENROLMENT_FORM_Q507 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_6_Q610 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_6_Q612 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_7_Q704 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_8_Q801 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
-- ALTER TABLE odk_aggregate.CT_HOME_VISIT_VERFICATION_FORM_CORE CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
-- ALTER TABLE odk_aggregate.CT_HOME_VISIT_VERFICATION_FORM_Q3 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';

CALL sp_update_demographics_location();
CALL sp_populate_flat_enrollment_table();
CALL sp_initial_update_enrollment_staging_table();

END;
$$
DELIMITER ;

-- -----------------------------------------       event definition  ------------------------------------------------------
DELIMITER $$
DROP EVENT IF EXISTS event_odk_dreams_enrollment_sync$$
CREATE EVENT event_odk_dreams_enrollment_sync
ON SCHEDULE EVERY 5 MINUTE STARTS CURRENT_TIMESTAMP
DO
BEGIN
CALL sp_sync_odk_dreams_data();
CALL sp_update_demographics_location();
CALL sp_update_flat_enrollment_table();

END;
$$
DELIMITER ;

-- clear log: remove old successful entries

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_clear_log_table$$
CREATE PROCEDURE sp_clear_log_table()
BEGIN

DECLARE last_update_time DATETIME;
SELECT max(date_started) into last_update_time from dreams_production.DreamsApp_flatenrollmenttablelog;
DELETE FROM DreamsApp_flatenrollmenttablelog where date_started < last_update_time and activity IS NOT NULL;

END;
$$
DELIMITER ;
-- ------------------------------------------ stored procedures -------------------------------------------------------

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

-- entry point for sync process. The procedure in turn calls other procedures

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

DELIMITER $$
DROP FUNCTION IF EXISTS nextDreamsSerial$$
CREATE FUNCTION nextDreamsSerial(implementing_partner_id INT, ward INT) RETURNS VARCHAR(200)
	DETERMINISTIC
BEGIN
	DECLARE new_serial INT(11);
	SELECT
  (max(CONVERT(SUBSTRING_INDEX(dreams_id, '/', -1), UNSIGNED INTEGER )) + 1) INTO new_serial
from DreamsApp_client WHERE dreams_id is not null AND ward_id is not null AND DreamsApp_client.implementing_partner_id=implementing_partner_id and DreamsApp_client.ward_id=ward group by implementing_partner_id, ward_id;

  IF new_serial is NULL THEN
    SET new_serial = 1;
  END IF;

	return CONCAT(implementing_partner_id, '/', ward, '/',new_serial);
END$$
DELIMITER ;

-- Getting demographic data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_demographic_data$$
CREATE PROCEDURE sp_demographic_data(IN recordUUID VARCHAR(100))
	BEGIN

    INSERT INTO dreams_production.DreamsApp_client
    (
      first_name,
      middle_name,
      last_name,
      date_of_birth,
      date_of_enrollment,
      marital_status_id,
      phone_number,
      dss_id_number,
      dreams_id,
      guardian_name,
      relationship_with_guardian,
      guardian_phone_number,
      guardian_national_id,
      informal_settlement,
      landmark,
      village,
      verification_document_id,
      verification_document_other,
      verification_doc_no,
      implementing_partner_id,
      ward_id,
      odk_enrollment_uuid,
      date_created,
      voided
    )
    select
      d.DEMOGRAPHIC_FIRSTNAME_1 as f_name,
      d.DEMOGRAPHIC_MIDDLENAME_1 as m_name,
      d.DEMOGRAPHIC_LASTNAME_1 as l_name,
      date(d.DOB) as dob,
      date(d.DOE) as date_of_enrollment,
      d.DEMOGRAPHIC_MARITAL as marital_status,
      d.DEMOGRAPHIC_PHONENO as client_phone_no,
      d.DEMOGRAPHIC_DSSNO as dss_no,
      nextDreamsSerial(d.IPNAME, d.DEMOGRAPHIC_WARD) as Dreams_id,
      d.DEMOGRAPHIC_CAREGIVER AS caregiver_name,
      d.DEMOGRAPHIC_RELATIONSHIP as caregiver_relationship,
      d.DEMOGRAPHIC_PHONENUMBER as caregiver_phone_no,
      d.DEMOGRAPHIC_NATIONAL_ID as caregiver_ID_no,
      d.DEMOGRAPHIC_INFORMALSTTLEMENTT as informal_settlement,
      d.DEMOGRAPHIC_LANDMARK as landmark,
      d.DEMOGRAPHIC_VILLAGE as village,
      d.VERIFICATIONDOC as verification_doc,
      d.VERIFICATIONDOCSPECIFY as verification_doc_other,
      COALESCE(d.VERIFICATION_1, d.VERIFICATION_2, d.VERIFICATION_3) as verification_doc_no,
      d.IPNAME as ip_name,
      d.DEMOGRAPHIC_WARD,
      d._URI as uuid,
      now(),
      0
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE d
    where d.ENROLNOTENROLED = 1 and _URI=recordUUID ;
  END
		$$
DELIMITER ;

-- Getting individual and household data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_individual_and_household_data$$
CREATE PROCEDURE sp_individual_and_household_data(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN
    DECLARE individualRecordID INT(11);

    INSERT INTO dreams_production.DreamsApp_clientindividualandhouseholddata
    (
      client_id,
      head_of_household_id, -- q101
      head_of_household_other, --
      age_of_household_head,
      is_father_alive,
      is_mother_alive,
      is_parent_chronically_ill,
      main_floor_material_id,
      main_floor_material_other,
      main_roof_material_id,
      main_roof_material_other,
      main_wall_material_id,
      main_wall_material_other,
      source_of_drinking_water_id,
      source_of_drinking_water_other,
      ever_missed_full_day_food_in_4wks_id,
      no_of_days_missed_food_in_4wks_id,
      has_disability_id,
      disability_type_other,
      no_of_people_in_household,
      no_of_females,
      no_of_males,
      no_of_adults,
      no_of_children,
      ever_enrolled_in_ct_program_id,
      currently_in_ct_program_id,
      current_ct_program
    )
    select
      clientID,
      d.MODULE_Q101 as head_of_household,
      d.MODULE_Q101SPECIFY as head_of_household_other,
      d.MODULE_Q102 as age_of_household_head,
      d.MODULE_Q103 as is_father_alive,
      d.MODULE_Q104 as is_mother_alive,
      d.MODULE_Q105 as is_parent_chronically_ill,
      d.MODULE_Q_106 as main_floor_material,
      d.MODULE_Q106SPECIFY as main_floor_material_other,
      d.MODULE_Q_107 as main_roof_material,
      d.MODULE_Q107SPECIFY AS main_roof_material_other,
      d.MODULE_Q_108 as main_wall_material,
      d.MODULE_Q108SPECIFY as main_wall_material_other,
      d.MODULE_Q_109 as source_of_drinking_water,
      d.MODULE_Q109SPECIFY as source_of_drinking_water_other,
      d.MODULE_Q110 as ever_missed_full_day_food_in_4wks,
      d.MODULE_Q_111 as no_of_days_missed_food_in_4wks,
      d.MODULE_Q112 as has_disability,
      d.MODULE_Q113SPECIFY as disability_type_other,
      d.MODULE_Q114 as no_of_people_in_household,
      d.MODULE_Q114A as no_of_females,
      d.MODULE_Q114B as no_of_males,
      d.MODULE_Q114C as no_of_adults,
      d.MODULE_Q114D as no_of_children,
      d.MODULE_Q115 as ever_enrolled_in_ct_program,
      d.MODULE_Q116 as currently_in_ct_program,
      d.MODULE_Q117 as current_ct_program
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE2 d
    where d._PARENT_AURI = recordUUID;

     -- Get id of the inserted reproductive health data row
    SET individualRecordID = LAST_INSERT_ID();
    CALL sp_client_disability_type(individualRecordID, recordUUID);
  END
		$$
DELIMITER ;

-- django many to many relationship: Individual and household data - disability types
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_client_disability_type$$
CREATE PROCEDURE sp_client_disability_type(IN recordID INT(11), IN parentUUID VARCHAR(100))
  BEGIN
    INSERT INTO dreams_production.DreamsApp_clientindividualandhouseholddata_disability_type (clientindividualandhouseholddata_id, disabilitytype_id)
    SELECT recordID, c.VALUE
    FROM odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_Q113 c
    WHERE c._PARENT_AURI=parentUUID;
  END $$
DELIMITER ;

-- Getting sexuality data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_sexuality_data$$
CREATE PROCEDURE sp_sexuality_data(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN
    -- SELECT concat('UUID: ',recordUUID, ', clientID: ', clientID);
    INSERT INTO dreams_production.DreamsApp_clientsexualactivitydata
    (
      client_id,
      ever_had_sex_id,
      age_at_first_sexual_encounter,
      has_sexual_partner_id,
      sex_partners_in_last_12months,
      age_of_last_partner_id,
      age_of_second_last_partner_id,
      age_of_third_last_partner_id,
      last_partner_circumcised_id,
      second_last_partner_circumcised_id,
      third_last_partner_circumcised_id,
      know_last_partner_hiv_status_id,
      know_second_last_partner_hiv_status_id,
      know_third_last_partner_hiv_status_id,
      used_condom_with_last_partner_id,
      used_condom_with_second_last_partner_id,
      used_condom_with_third_last_partner_id,
      received_money_gift_for_sex_id
    )
    select
      clientID,
      d.MODULE_4_Q401 as ever_had_sex,
      d.MODULE_4_Q402 as age_at_first_sexual_encounter,
      d.MODULE_4_Q403 as has_sexual_partner,
      d.MODULE_4_Q404 as sex_partners_in_last_12months,
      d.MODULE_4_Q405_Q405_LAST as age_of_last_partner,
      d.MODULE_4_Q405_Q405_SECOND as age_of_second_last_partner,
      d.MODULE_4_Q405_Q405_THIRD as age_of_third_last_partner,
      d.MODULE_4_Q406_Q406_LAST as last_partner_circumcised,
      d.MODULE_4_Q406_Q406_SECOND as second_last_partner_circumcised,
      d.MODULE_4_Q406_Q406_THIRD AS third_last_partner_circumcised,
      d.MODULE_4_Q407_Q407_LAST as know_last_partner_hiv_status,
      d.MODULE_4_Q407_Q407_SECOND as know_second_last_partner_hiv_status,
      d.MODULE_4_Q407_Q407_THIRD as know_third_last_partner_hiv_status,
      d.MODULE_4_Q408_Q408_LAST as used_condom_with_last_partner,
      d.MODULE_4_Q408_Q408_SECOND as used_condom_with_second_last_partner,
      d.MODULE_4_Q408_Q408_THIRD as used_condom_with_third_last_partner,
      d.MODULE_4_Q409 as received_money_gift_for_sex
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE2 d
    where d._PARENT_AURI = recordUUID;
  END
		$$
DELIMITER ;


-- Getting reproductive health data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_reproductive_health_data$$
CREATE PROCEDURE sp_reproductive_health_data(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN
    DECLARE repHealthRecordID INT(11);

    INSERT INTO dreams_production.DreamsApp_clientreproductivehealthdata
    (
      client_id,
      has_biological_children_id,
      no_of_biological_children,
      currently_pregnant_id,
      current_anc_enrollment_id,
      anc_facility_name,
      fp_methods_awareness_id,
      known_fp_method_other,
      currently_use_modern_fp_id,
      current_fp_method_id,
      current_fp_method_other,
      reason_not_using_fp_id,
      reason_not_using_fp_other
    )
    select
      clientID,
      d.Q501 as has_biological_children,
      d.Q502 as no_of_biological_children,
      d.Q503 as currently_pregnant,
      d.Q504 as current_anc_enrollment,
      d.Q505 as anc_facility_name,
      d.Q506 as fp_methods_awareness,
      d.Q507SPECIFY as known_fp_method_other,
      d.Q508 AS currently_use_modern_fp,
      d.Q509 as current_fp_method,
      d.Q509SPECIFY as current_fp_method_other,
      d.Q510 as reason_not_using_fp,
      d.Q510SPECIFY as reason_not_using_fp_other
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE d
    where d._URI = recordUUID;

    -- Get id of the inserted reproductive health data row
    SET repHealthRecordID = LAST_INSERT_ID();
    CALL sp_client_rep_health_known_fp_method(repHealthRecordID, recordUUID);

  END
		$$
DELIMITER ;

-- django many to many relationship: reproductive health - known family planning methods
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_client_rep_health_known_fp_method$$
CREATE PROCEDURE sp_client_rep_health_known_fp_method(IN recordID INT(11), IN parentUUID VARCHAR(100))
  BEGIN
    INSERT INTO dreams_production.DreamsApp_clientreproductivehealthdata_known_fp_method (clientreproductivehealthdata_id, familyplanningmethod_id)
    SELECT recordID, c.VALUE
    FROM odk_aggregate.DREAMS_ENROLMENT_FORM_Q507 c
    WHERE c._PARENT_AURI=parentUUID;

  END $$
DELIMITER ;


-- Getting Drug Use data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_drug_use_data$$
CREATE PROCEDURE sp_drug_use_data(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN
    DECLARE drugUseRecordID INT(11);

    INSERT INTO dreams_production.DreamsApp_clientdrugusedata
    (
      client_id,
      used_alcohol_last_12months_id,
      frequency_of_alcohol_last_12months_id,
      drug_abuse_last_12months_id,
      drug_used_last_12months_other,
      produced_alcohol_last_12months_id
    )
    select
      clientID,
      d.MODULE_7_Q701 as used_alcohol_last_12months,
      d.MODULE_7_Q702 as frequency_of_alcohol_last_12months,
      d.MODULE_7_Q703 as drug_abuse_last_12months,
      d.MODULE_7_Q704SPECIFY as drug_used_last_12months_other,
      d.MODULE_7_Q705 AS produced_alcohol_last_12months
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE d
    where d._URI = recordUUID;

    -- Get id of the inserted Drug Use data row
    SET drugUseRecordID = LAST_INSERT_ID();
    CALL sp_client_drug_used_in_last_12_months(drugUseRecordID, recordUUID);

  END
		$$
DELIMITER ;

-- django many to many relationship: Drugs used in the last 12 months
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_client_drug_used_in_last_12_months$$
CREATE PROCEDURE sp_client_drug_used_in_last_12_months(IN recordID INT(11), IN parentUUID VARCHAR(100))
  BEGIN
    INSERT INTO dreams_production.DreamsApp_clientdrugusedata_drug_used_last_12months (clientdrugusedata_id, drug_id)
    SELECT recordID, c.VALUE
    FROM odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_7_Q704 c
    WHERE c._PARENT_AURI=parentUUID;

  END $$
DELIMITER ;


-- Getting Dreams Programme participation
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_program_participation_data$$
CREATE PROCEDURE sp_program_participation_data(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN
    DECLARE programParticipationRecordID INT(11);

    INSERT INTO dreams_production.DreamsApp_clientparticipationindreams
    (
      client_id,
      dreams_program_other
    )
    select
      clientID,
      d.MODULE_8_Q801SPECIFY as dreams_program_other
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE d
    where d._URI = recordUUID;

    -- Get id of the inserted Program participation data row
    SET programParticipationRecordID = LAST_INSERT_ID();
    CALL sp_client_programs_enrolled(programParticipationRecordID, recordUUID);
  END
		$$
DELIMITER ;

-- django many to many relationship: Dreams programs enrolled in
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_client_programs_enrolled$$
CREATE PROCEDURE sp_client_programs_enrolled(IN recordID INT(11), IN parentUUID VARCHAR(100))
  BEGIN
    INSERT INTO dreams_production.DreamsApp_clientparticipationindreams_dreams_program (clientparticipationindreams_id, dreamsprogramme_id)
    SELECT recordID, c.VALUE
    FROM odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_8_Q801 c
    WHERE c._PARENT_AURI=parentUUID;

  END $$
DELIMITER ;



-- Getting GBV data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_gbv_data$$
CREATE PROCEDURE sp_gbv_data(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN
    DECLARE gbvRecordID INT(11);

    INSERT INTO dreams_production.DreamsApp_clientgenderbasedviolencedata
    (
      client_id,
      humiliated_ever_id,
      humiliated_last_3months_id,
      threats_to_hurt_ever_id,
      threats_to_hurt_last_3months_id,
      insulted_ever_id,
      insulted_last_3months_id,
      economic_threat_ever_id,
      economic_threat_last_3months_id,
      physical_violence_ever_id,
      physical_violence_last_3months_id,
      physically_forced_sex_ever_id,
      physically_forced_sex_last_3months_id,
      physically_forced_other_sex_acts_ever_id,
      physically_forced_other_sex_acts_last_3months_id,
      threatened_for_sexual_acts_ever_id,
      threatened_for_sexual_acts_last_3months_id,
      seek_help_after_gbv_id,
      gbv_help_provider_other,
      knowledge_of_gbv_help_centres_id,
      preferred_gbv_help_provider_other
    )
    select
      clientID,
      d.MODULE_6_Q_601_GROUP_Q_601_EVER as humiliated_ever,
      d.MODULE_6_Q_601_GROUP_Q_601_LAST_3_MONTHS as humiliated_last_3months,
      d.MODULE_6_Q_602_GROUP_Q_602_EVER as threats_to_hurt_ever,
      d.MODULE_6_Q_602_GROUP_Q_602_LAST_3_MONTHS as threats_to_hurt_last_3months,
      d.MODULE_6_Q_603_GROUP_Q_603_EVER as insulted_ever,
      d.MODULE_6_Q_603_GROUP_Q_603_LAST_3_MONTHS as insulted_last_3months,
      d.MODULE_6_Q_604_Q_604_EVER as economic_threat_ever,
      d.MODULE_6_Q_604_Q_604_LAST_3_MONTHS as economic_threat_last_3months,
      d.MODULE_6_Q_605_Q_605_EVER as physical_violence_ever,
      d.MODULE_6_Q_605_Q_605_LAST_3_MONTHS AS physical_violence_last_3months,
      d.MODULE_6_Q_606_Q_606_EVER as physically_forced_sex_ever,
      d.MODULE_6_Q_606_Q_606_LAST_3_MONTHS as physically_forced_sex_last_3months,
      d.MODULE_6_Q_607_Q_607_EVER as physically_forced_other_sex_acts_ever,
      d.MODULE_6_Q_607_Q_607_LAST_3_MONTHS as physically_forced_other_sex_acts_last_3months,
      d.MODULE_6_Q_608_Q_608_EVER as threatened_for_sexual_acts_ever,
      d.MODULE_6_Q_608_Q_608_LAST_3_MONTHS as threatened_for_sexual_acts_last_3months,
      d.MODULE_6_Q609 as seek_help_after_gbv,
      d.MODULE_6_Q610SPECIFY as gbv_help_provider_other,
      d.MODULE_6_Q611 as knowledge_of_gbv_help_centres,
      d.MODULE_6_Q612SPECIFY as preferred_gbv_help_provider_other
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE2 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where d._PARENT_AURI = recordUUID;

    -- Get id of the inserted GBV data row
    SET gbvRecordID = LAST_INSERT_ID();
    CALL sp_client_gbv_help_provider(gbvRecordID, recordUUID);
    CALL sp_client_gbv_preferred_provider(gbvRecordID, recordUUID);

  END
		$$
DELIMITER ;

-- django many to many relationship: provider where client sought help after GBV
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_client_gbv_help_provider$$
CREATE PROCEDURE sp_client_gbv_help_provider(IN recordID INT(11), IN parentUUID VARCHAR(100))
  BEGIN
    INSERT INTO dreams_production.DreamsApp_clientgenderbasedviolencedata_gbv_help_provider (clientgenderbasedviolencedata_id, gbvhelpprovider_id)
    SELECT recordID, c.VALUE
    FROM odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_6_Q610 c
    WHERE c._PARENT_AURI=parentUUID;

  END $$
DELIMITER ;

-- django many to many relationship: preferred GBV provider
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_client_gbv_preferred_provider$$
CREATE PROCEDURE sp_client_gbv_preferred_provider(IN recordID INT(11), IN parentUUID VARCHAR(100))
  BEGIN
    INSERT INTO dreams_production.DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_p1bce (clientgenderbasedviolencedata_id, gbvhelpprovider_id)
    SELECT recordID, c.VALUE
    FROM odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_6_Q612 c
    WHERE c._PARENT_AURI=parentUUID;

  END $$
DELIMITER ;


-- Getting Education and employment data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_education_and_employment$$
CREATE PROCEDURE sp_education_and_employment(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN
    DECLARE eduRecordID INT(11);

    INSERT INTO dreams_production.DreamsApp_clienteducationandemploymentdata
    (
      client_id,
      currently_in_school_id,
      current_school_name,
      current_school_type_id,
      current_school_level_id,
      current_school_level_other,
      current_class,
      current_education_supporter_other,
      reason_not_in_school_id,
      reason_not_in_school_other,
      last_time_in_school_id,
      dropout_school_level_id,
      dropout_class,
      life_wish_id,
      life_wish_other,
      current_income_source_id,
      current_income_source_other,
      has_savings_id,
      banking_place_id,
      banking_place_other
    )
    select
      clientID,
      d.MODULE_2_Q201 as currently_in_school,
      d.MODULE_2_Q202 as current_school_name,
      d.MODULE_2_FORMALINFORMAL as current_school_type,
      d.MODULE_2_Q203 as current_school_level,
      d.MODULE_2_Q203SPECIFY as current_school_level_other,
      COALESCE(d.MODULE_2_Q203_PRIMARY, d.MODULE_2_Q203_SECONDARY) as current_class,
      d.MODULE_2_Q204SPECIFY as current_education_supporter_other,
      d.MODULE_2_Q205 as reason_not_in_school,
      d.MODULE_2_Q205SPECIFY AS reason_not_in_school_other,
      d.MODULE_2_Q206 as last_time_in_school,
      d.MODULE_2_Q207 as dropout_school_level,
      COALESCE(d.MODULE_2_Q207_PRIMARY, d.MODULE_2_Q207_SECONDARY) as dropout_class,
      d.MODULE_2_Q208 as life_wish,
      d.MODULE_2_Q208SPECIFY as life_wish_other,
      d.MODULE_2_Q209 as current_income_source,
      d.MODULE_2_Q209SPECIFY as current_income_source_other,
      d.MODULE_2_Q210 as has_savings,
      d.MODULE_2_Q211 as banking_place,
      d.MODULE_2_Q211SPECIFY as banking_place_other
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE2 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where d._PARENT_AURI = recordUUID;

    -- Get id of the inserted education data row
    SET eduRecordID = LAST_INSERT_ID();
    -- SELECT CONCAT('Education supporter: ', eduRecordID);
    CALL sp_client_current_education_supporter(eduRecordID, recordUUID);

  END
		$$
DELIMITER ;
-- education and employment many to many relationship: current education supporter
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_client_current_education_supporter$$
CREATE PROCEDURE sp_client_current_education_supporter(IN recordID INT(11), IN parentUUID VARCHAR(100))
  BEGIN
    INSERT INTO dreams_production.DreamsApp_clienteducationandemploymentdata_current_educationebf4 (clienteducationandemploymentdata_id, educationsupporter_id)
    SELECT recordID, c.VALUE
    FROM odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_2_Q204 c
    WHERE c._PARENT_AURI=parentUUID;

  END $$
DELIMITER ;


-- Getting HIV testing
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_hiv_testing$$
CREATE PROCEDURE sp_hiv_testing(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN
    DECLARE hivtestingRecordID INT(11);

    INSERT INTO dreams_production.DreamsApp_clienthivtestingdata
    (
      client_id,
      ever_tested_for_hiv_id,
      period_last_tested_id,
      last_test_result_id,
      enrolled_in_hiv_care_id,
      care_facility_enrolled,
      reason_not_in_hiv_care_id,
      reason_not_in_hiv_care_other,
      reason_never_tested_for_hiv_other,
      knowledge_of_hiv_test_centres_id
    )
    select
      clientID,
      d.MODULE_3_Q301 as ever_tested_for_hiv,
      d.MODULE_3_Q302 as period_last_tested,
      d.MODULE_3_Q303 as last_test_result,
      d.MODULE_3_Q304 as enrolled_in_hiv_care,
      d.MODULE_3_Q305 as care_facility_enrolled,
      d.MODULE_3_Q306 as reason_not_in_hiv_care,
      d.MODULE_3_Q306SPECIFY as reason_not_in_hiv_care_other,
      d.MODULE_3_Q307SPECIFY as reason_never_tested_for_hiv_other,
      d.MODULE_3_Q308 AS knowledge_of_hiv_test_centres
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE d
    where d._URI = recordUUID;

    -- Get id of the inserted education data row
    SET hivtestingRecordID = LAST_INSERT_ID();
    CALL sp_client_hiv_reason_never_tested(hivtestingRecordID, recordUUID);

  END
		$$
DELIMITER ;

-- get reason one has never tested for hiv: django many to many relationship

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_client_hiv_reason_never_tested$$
CREATE PROCEDURE sp_client_hiv_reason_never_tested(IN recordID INT(11), IN parentUUID VARCHAR(100))
  BEGIN
    INSERT INTO dreams_production.DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv (clienthivtestingdata_id, reasonnottestedforhiv_id)
    SELECT recordID, c.VALUE
    FROM odk_aggregate.DREAMS_ENROLMENT_FORM_MODULE_3_Q307 c
    WHERE c._PARENT_AURI=parentUUID;

  END $$
DELIMITER ;


-- ----------------------------------------- sync CT home visit verification -------------------------------------------

-- Getting demographic data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_ct_home_visit_verification_data$$
CREATE PROCEDURE sp_ct_home_visit_verification_data(IN recordUUID VARCHAR(100))
	BEGIN
    DECLARE ct_home_visit_recordID INT(11);

    INSERT INTO dreams_production.DreamsApp_homevisitverification
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

-- get reason one has never tested for hiv: django many to many relationship

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_ct_source_of_livelihood$$
CREATE PROCEDURE sp_ct_source_of_livelihood(IN recordID INT(11), IN parentUUID VARCHAR(100))
  BEGIN
    INSERT INTO dreams_production.DreamsApp_homevisitverification_source_of_livelihood (homevisitverification_id, sourceofincome_id)
    SELECT recordID, c.VALUE
    FROM odk_aggregate.CT_HOME_VISIT_VERFICATION_FORM_Q3 c
    WHERE c._PARENT_AURI=parentUUID;

  END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_demographics_location$$
CREATE PROCEDURE sp_update_demographics_location()
  BEGIN
    UPDATE dreams_production.DreamsApp_client cl
    INNER JOIN (
      SELECT
      w.code ward_code,
      sc.id subcounty_id,
      c.id county_id
    from dreams_production.DreamsApp_ward w
    INNER JOIN dreams_production.DreamsApp_subcounty sc ON sc.id = w.sub_county_id
    INNER JOIN dreams_production.DreamsApp_county c ON c.id=sc.county_id
    ) location ON location.ward_code = cl.ward_id
    SET cl.sub_county_id = location.subcounty_id, cl.county_of_residence_id = location.county_id
    WHERE (cl.sub_county_id is NULL OR cl.county_of_residence_id is NULL)

;
  END $$
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_enrollment_staging_table$$
CREATE PROCEDURE sp_update_enrollment_staging_table()
  BEGIN
    /*Update implementing partner*/
    UPDATE dreams_production.DreamsApp_client cl
    INNER JOIN (
      select code, name from DreamsApp_implementingpartner
    ) ip ON ip.code = cl.implementing_partner_id
    SET cl.implementing_partner = ip.name
    WHERE cl.implementing_partner is NULL

;
  END $$
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS sp_initial_update_enrollment_staging_table$$
CREATE PROCEDURE sp_initial_update_enrollment_staging_table()
  BEGIN
    /*Update implementing partner*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_implementingpartner
    ) ip ON ip.code = cl.implementing_partner_id
    SET cl.implementing_partner = ip.name
    WHERE cl.implementing_partner is NULL and voided=0;

    /*Update verification document*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_verificationdocument
    ) v ON v.code = cl.verification_document_id
    SET cl.verification_document = v.name
    WHERE cl.verification_document is NULL and voided=0;

    /*Update marital status*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_maritalstatus
    ) m ON m.code = cl.marital_status_id
    SET cl.marital_status = m.name
    WHERE cl.marital_status is NULL and voided=0;


    /*Update head of household*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_householdhead
    ) m ON m.code = cl.head_of_household_id
    SET cl.head_of_household = m.name
    WHERE cl.head_of_household is NULL and voided=0;

    /*Update parent status*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.is_father_alive
    SET cl.father_alive = m.name
    WHERE cl.father_alive is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.is_mother_alive
    SET cl.mother_alive = m.name
    WHERE cl.mother_alive is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.is_parent_chronically_ill
    SET cl.parent_chronically_ill = m.name
    WHERE cl.parent_chronically_ill is NULL and voided=0;

    /* Wall, floor, roof, drinking water */
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_floormaterial
    ) m ON m.code = cl.main_floor_material_id
    SET cl.main_floor_material = m.name
    WHERE cl.main_floor_material is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_roofingmaterial
    ) m ON m.code = cl.main_roof_material_id
    SET cl.main_roof_material = m.name
    WHERE cl.main_roof_material is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_wallmaterial
    ) m ON m.code = cl.main_wall_material_id
    SET cl.main_wall_material = m.name
    WHERE cl.main_wall_material is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_drinkingwater
    ) m ON m.code = cl.source_of_drinking_water_id
    SET cl.source_of_drinking_water = m.name
    WHERE cl.source_of_drinking_water is NULL and voided=0;

    /* ct enrollment, disability, hunger*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_in_ct_program_id
    SET cl.currently_in_ct_program = m.name
    WHERE cl.currently_in_ct_program is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_enrolled_in_ct_program_id
    SET cl.ever_enrolled_in_ct_program = m.name
    WHERE cl.ever_enrolled_in_ct_program is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_missed_full_day_food_in_4wks_id
    SET cl.ever_missed_full_day_food_in_4wks = m.name
    WHERE cl.ever_missed_full_day_food_in_4wks is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_disability_id
    SET cl.has_disability = m.name
    WHERE cl.has_disability is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.no_of_days_missed_food_in_4wks_id
    SET cl.no_of_days_missed_food_in_4wks = m.name
    WHERE cl.no_of_days_missed_food_in_4wks is NULL and voided=0;

    /* ------------------------------------------ sexuality -------------------------------------------------*/

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_ageofsexualpartner
    ) m ON m.code = cl.age_of_last_partner_id
    SET cl.age_of_last_partner = m.name
    WHERE cl.age_of_last_partner is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_ageofsexualpartner
    ) m ON m.code = cl.age_of_second_last_partner_id
    SET cl.age_of_second_last_partner = m.name
    WHERE cl.age_of_second_last_partner is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_ageofsexualpartner
    ) m ON m.code = cl.age_of_third_last_partner_id
    SET cl.age_of_third_last_partner = m.name
    WHERE cl.age_of_third_last_partner is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_had_sex_id
    SET cl.ever_had_sex = m.name
    WHERE cl.ever_had_sex is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_sexual_partner_id
    SET cl.has_sexual_partner = m.name
    WHERE cl.has_sexual_partner is NULL and voided=0;

  /* partner hiv status*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.know_last_partner_hiv_status_id
    SET cl.know_last_partner_hiv_status = m.name
    WHERE cl.know_last_partner_hiv_status is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.know_second_last_partner_hiv_status_id
    SET cl.know_second_last_partner_hiv_status = m.name
    WHERE cl.know_second_last_partner_hiv_status is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.know_third_last_partner_hiv_status_id
    SET cl.know_third_last_partner_hiv_status = m.name
    WHERE cl.know_third_last_partner_hiv_status is NULL and voided=0;

    /* ------------partner circumcision-------------*/

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.last_partner_circumcised_id
    SET cl.last_partner_circumcised = m.name
    WHERE cl.last_partner_circumcised is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.second_last_partner_circumcised_id
    SET cl.second_last_partner_circumcised = m.name
    WHERE cl.second_last_partner_circumcised is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.third_last_partner_circumcised_id
    SET cl.third_last_partner_circumcised = m.name
    WHERE cl.third_last_partner_circumcised is NULL and voided=0;

    /*------------ condom use --------------------*/

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.used_condom_with_last_partner_id
    SET cl.used_condom_with_last_partner = m.name
    WHERE cl.used_condom_with_last_partner is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.used_condom_with_second_last_partner_id
    SET cl.used_condom_with_second_last_partner = m.name
    WHERE cl.used_condom_with_second_last_partner is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.used_condom_with_third_last_partner_id
    SET cl.used_condom_with_third_last_partner = m.name
    WHERE cl.used_condom_with_third_last_partner is NULL and voided=0;

/*--------------- Reproductive Health ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.current_anc_enrollment_id
    SET cl.current_anc_enrollment = m.name
    WHERE cl.current_anc_enrollment is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_familyplanningmethod
    ) m ON m.code = cl.current_fp_method_id
    SET cl.current_fp_method = m.name
    WHERE cl.current_fp_method is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_pregnant_id
    SET cl.currently_pregnant = m.name
    WHERE cl.currently_pregnant is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_use_modern_fp_id
    SET cl.currently_use_modern_fp = m.name
    WHERE cl.currently_use_modern_fp is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.fp_methods_awareness_id
    SET cl.fp_methods_awareness = m.name
    WHERE cl.fp_methods_awareness is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_biological_children_id
    SET cl.has_biological_children = m.name
    WHERE cl.has_biological_children is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_reasonnotusingfamilyplanning
    ) m ON m.code = cl.reason_not_using_fp_id
    SET cl.reason_not_using_fp = m.name
    WHERE cl.reason_not_using_fp is NULL and voided=0;

/*------------------------------- Drug Use ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.drug_abuse_last_12months_id
    SET cl.drug_abuse_last_12months = m.name
    WHERE cl.drug_abuse_last_12months is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.frequency_of_alcohol_last_12months_id
    SET cl.frequency_of_alcohol_last_12months = m.name
    WHERE cl.frequency_of_alcohol_last_12months is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.produced_alcohol_last_12months_id
    SET cl.produced_alcohol_last_12months = m.name
    WHERE cl.produced_alcohol_last_12months is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.used_alcohol_last_12months_id
    SET cl.used_alcohol_last_12months = m.name
    WHERE cl.used_alcohol_last_12months is NULL and voided=0;

/*------------------------------- GBV ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.economic_threat_ever_id
    SET cl.economic_threat_ever = m.name
    WHERE cl.economic_threat_ever is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.economic_threat_last_3months_id
    SET cl.economic_threat_last_3months = m.name
    WHERE cl.economic_threat_last_3months is NULL and voided=0;
/*-------------------------------------------------------------*/

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.humiliated_ever_id
    SET cl.humiliated_ever = m.name
    WHERE cl.humiliated_ever is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.humiliated_last_3months_id
    SET cl.humiliated_last_3months = m.name
    WHERE cl.humiliated_last_3months is NULL and voided=0;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.insulted_ever_id
    SET cl.insulted_ever = m.name
    WHERE cl.insulted_ever is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.insulted_last_3months_id
    SET cl.insulted_last_3months = m.name
    WHERE cl.insulted_last_3months is NULL and voided=0;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.knowledge_of_gbv_help_centres_id
    SET cl.knowledge_of_gbv_help_centres = m.name
    WHERE cl.knowledge_of_gbv_help_centres is NULL and voided=0;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.physical_violence_ever_id
    SET cl.physical_violence_ever = m.name
    WHERE cl.physical_violence_ever is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.physical_violence_last_3months_id
    SET cl.physical_violence_last_3months = m.name
    WHERE cl.physical_violence_last_3months is NULL and voided=0;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.physically_forced_other_sex_acts_ever_id
    SET cl.physically_forced_other_sex_acts_ever = m.name
    WHERE cl.physically_forced_other_sex_acts_ever is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.physically_forced_other_sex_acts_last_3months_id
    SET cl.physically_forced_other_sex_acts_last_3months = m.name
    WHERE cl.physically_forced_other_sex_acts_last_3months is NULL and voided=0;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.physically_forced_sex_ever_id
    SET cl.physically_forced_sex_ever = m.name
    WHERE cl.physically_forced_sex_ever is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.physically_forced_sex_last_3months_id
    SET cl.physically_forced_sex_last_3months = m.name
    WHERE cl.physically_forced_sex_last_3months is NULL and voided=0;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.seek_help_after_gbv_id
    SET cl.seek_help_after_gbv = m.name
    WHERE cl.seek_help_after_gbv_id is NULL and voided=0;

/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_ever_id
    SET cl.threatened_for_sexual_acts_ever = m.name
    WHERE cl.threatened_for_sexual_acts_ever is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_last_3months_id
    SET cl.threatened_for_sexual_acts_last_3months = m.name
    WHERE cl.threatened_for_sexual_acts_last_3months is NULL and voided=0;

/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_ever_id
    SET cl.threatened_for_sexual_acts_ever = m.name
    WHERE cl.threatened_for_sexual_acts_ever is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_last_3months_id
    SET cl.threatened_for_sexual_acts_last_3months = m.name
    WHERE cl.threatened_for_sexual_acts_last_3months is NULL and voided=0;

/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.threats_to_hurt_ever_id
    SET cl.threats_to_hurt_ever = m.name
    WHERE cl.threats_to_hurt_ever is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.threats_to_hurt_last_3months_id
    SET cl.threats_to_hurt_last_3months = m.name
    WHERE cl.threats_to_hurt_last_3months is NULL and voided=0;

    /*------------------------------- Education and Employment ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_bankingplace
    ) m ON m.code = cl.banking_place_id
    SET cl.banking_place = m.name
    WHERE cl.banking_place is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_sourceofincome
    ) m ON m.code = cl.current_income_source_id
    SET cl.current_income_source = m.name
    WHERE cl.current_income_source is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_schoollevel
    ) m ON m.code = cl.current_school_level_id
    SET cl.current_school_level = m.name
    WHERE cl.current_school_level is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_schooltype
    ) m ON m.code = cl.current_school_type_id
    SET cl.current_school_type = m.name
    WHERE cl.current_school_type is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_in_school_id
    SET cl.currently_in_school = m.name
    WHERE cl.currently_in_school is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_schoollevel
    ) m ON m.code = cl.dropout_school_level_id
    SET cl.dropout_school_level = m.name
    WHERE cl.dropout_school_level is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_savings_id
    SET cl.has_savings = m.name
    WHERE cl.has_savings is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_periodresponse
    ) m ON m.code = cl.last_time_in_school_id
    SET cl.last_time_in_school = m.name
    WHERE cl.last_time_in_school is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_lifewish
    ) m ON m.code = cl.life_wish_id
    SET cl.life_wish = m.name
    WHERE cl.life_wish is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_reasonnotinschool
    ) m ON m.code = cl.reason_not_in_school_id
    SET cl.reason_not_in_school = m.name
    WHERE cl.reason_not_in_school is NULL and voided=0;

    /*------------------------------- HIV Testing ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.enrolled_in_hiv_care_id
    SET cl.enrolled_in_hiv_care = m.name
    WHERE cl.enrolled_in_hiv_care is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_tested_for_hiv_id
    SET cl.ever_tested_for_hiv = m.name
    WHERE cl.ever_tested_for_hiv is NULL and voided=0;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.knowledge_of_hiv_test_centres_id
    SET cl.knowledge_of_hiv_test_centres = m.name
    WHERE cl.knowledge_of_hiv_test_centres is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_hivtestresultresponse
    ) m ON m.code = cl.last_test_result_id
    SET cl.last_test_result = m.name
    WHERE cl.last_test_result is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_periodresponse
    ) m ON m.code = cl.period_last_tested_id
    SET cl.period_last_tested = m.name
    WHERE cl.period_last_tested is NULL and voided=0;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_reasonnotinhivcare
    ) m ON m.code = cl.reason_not_in_hiv_care_id
    SET cl.reason_not_in_hiv_care = m.name
    WHERE cl.reason_not_in_hiv_care is NULL and voided=0;

  END $$
DELIMITER ;


-- ---------------------------------------------- update flat table derived columns -------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_enrollment_table_derived_columns$$
CREATE PROCEDURE sp_update_enrollment_table_derived_columns(IN last_update_time DATETIME)
  BEGIN

  /*DECLARE last_update_time DATETIME;
  SELECT max(date_started) into last_update_time from dreams_production.DreamsApp_flatenrollmenttablelog;*/
    /*Update implementing partner*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_implementingpartner
    ) ip ON ip.code = cl.implementing_partner_id
    INNER JOIN (SELECT id from DreamsApp_client d where (d.date_created >= last_update_time or d.date_changed >= last_update_time)) client on client.id = cl.client_id
    SET cl.implementing_partner = ip.name;

    /*Update verification document*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_verificationdocument
    ) v ON v.code = cl.verification_document_id
    INNER JOIN (SELECT id from DreamsApp_client d where (d.date_created >= last_update_time or d.date_changed >= last_update_time)) client on client.id = cl.client_id
    SET cl.verification_document = v.name;

    /*Update marital status*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_maritalstatus
    ) m ON m.code = cl.marital_status_id
    INNER JOIN (SELECT id from DreamsApp_client d where (d.date_created >= last_update_time or d.date_changed >= last_update_time)) client on client.id = cl.client_id
    SET cl.marital_status = m.name;

-- -------------------------------------- individual and household ----------------------------------------------------
    /*Update head of household*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_householdhead
    ) m ON m.code = cl.head_of_household_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.head_of_household = m.name;

    /*Update parent status*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.is_father_alive
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.father_alive = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.is_mother_alive
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.mother_alive = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.is_parent_chronically_ill
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.parent_chronically_ill = m.name;

    /* Wall, floor, roof, drinking water */
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_floormaterial
    ) m ON m.code = cl.main_floor_material_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.main_floor_material = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_roofingmaterial
    ) m ON m.code = cl.main_roof_material_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.main_roof_material = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_wallmaterial
    ) m ON m.code = cl.main_wall_material_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.main_wall_material = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_drinkingwater
    ) m ON m.code = cl.source_of_drinking_water_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.source_of_drinking_water = m.name;

    /* ct enrollment, disability, hunger*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_in_ct_program_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.currently_in_ct_program = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_enrolled_in_ct_program_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.ever_enrolled_in_ct_program = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_missed_full_day_food_in_4wks_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.ever_missed_full_day_food_in_4wks = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_disability_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.has_disability = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.no_of_days_missed_food_in_4wks_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.no_of_days_missed_food_in_4wks = m.name;

    /* ------------------------------------------ sexuality -------------------------------------------------*/


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_ageofsexualpartner
    ) m ON m.code = cl.age_of_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.age_of_last_partner = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_ageofsexualpartner
    ) m ON m.code = cl.age_of_second_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.age_of_second_last_partner = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_ageofsexualpartner
    ) m ON m.code = cl.age_of_third_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.age_of_third_last_partner = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_had_sex_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.ever_had_sex = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_sexual_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.has_sexual_partner = m.name;

  /* partner hiv status*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.know_last_partner_hiv_status_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.know_last_partner_hiv_status = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.know_second_last_partner_hiv_status_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.know_second_last_partner_hiv_status = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.know_third_last_partner_hiv_status_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.know_third_last_partner_hiv_status = m.name;

    /* ------------partner circumcision-------------*/

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.last_partner_circumcised_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.last_partner_circumcised = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.second_last_partner_circumcised_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.second_last_partner_circumcised = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.third_last_partner_circumcised_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.third_last_partner_circumcised = m.name;

    /*------------ condom use --------------------*/

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.used_condom_with_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.used_condom_with_last_partner = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.used_condom_with_second_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.used_condom_with_second_last_partner = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.used_condom_with_third_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.used_condom_with_third_last_partner = m.name;

/*--------------- Reproductive Health ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.current_anc_enrollment_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.current_anc_enrollment = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_familyplanningmethod
    ) m ON m.code = cl.current_fp_method_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.current_fp_method = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_pregnant_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.currently_pregnant = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_use_modern_fp_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.currently_use_modern_fp = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.fp_methods_awareness_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.fp_methods_awareness = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_biological_children_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.has_biological_children = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_reasonnotusingfamilyplanning
    ) m ON m.code = cl.reason_not_using_fp_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.reason_not_using_fp = m.name;

/*------------------------------- Drug Use ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.drug_abuse_last_12months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientdrugusedata dr  where (dr.date_created >= last_update_time or dr.date_changed >= last_update_time)) dr on dr.client_id = cl.client_id
    SET cl.drug_abuse_last_12months = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.frequency_of_alcohol_last_12months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientdrugusedata dr  where (dr.date_created >= last_update_time or dr.date_changed >= last_update_time)) dr on dr.client_id = cl.client_id
    SET cl.frequency_of_alcohol_last_12months = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.produced_alcohol_last_12months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientdrugusedata dr  where (dr.date_created >= last_update_time or dr.date_changed >= last_update_time)) dr on dr.client_id = cl.client_id
    SET cl.produced_alcohol_last_12months = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.used_alcohol_last_12months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientdrugusedata dr  where (dr.date_created >= last_update_time or dr.date_changed >= last_update_time)) dr on dr.client_id = cl.client_id
    SET cl.used_alcohol_last_12months = m.name;

/*------------------------------- GBV ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.economic_threat_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.economic_threat_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.economic_threat_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.economic_threat_last_3months = m.name;
/*-------------------------------------------------------------*/

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.humiliated_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.humiliated_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.humiliated_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.humiliated_last_3months = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.insulted_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.insulted_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.insulted_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.insulted_last_3months = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.knowledge_of_gbv_help_centres_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.knowledge_of_gbv_help_centres = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.physical_violence_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physical_violence_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.physical_violence_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physical_violence_last_3months = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.physically_forced_other_sex_acts_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physically_forced_other_sex_acts_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.physically_forced_other_sex_acts_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physically_forced_other_sex_acts_last_3months = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.physically_forced_sex_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physically_forced_sex_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.physically_forced_sex_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physically_forced_sex_last_3months = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.seek_help_after_gbv_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.seek_help_after_gbv = m.name;

/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threatened_for_sexual_acts_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threatened_for_sexual_acts_last_3months = m.name;

/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threatened_for_sexual_acts_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threatened_for_sexual_acts_last_3months = m.name;

/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.threats_to_hurt_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threats_to_hurt_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.threats_to_hurt_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threats_to_hurt_last_3months = m.name;

    /*------------------------------- Education and Employment ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_bankingplace
    ) m ON m.code = cl.banking_place_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.banking_place = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_sourceofincome
    ) m ON m.code = cl.current_income_source_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.current_income_source = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_schoollevel
    ) m ON m.code = cl.current_school_level_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.current_school_level = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_schooltype
    ) m ON m.code = cl.current_school_type_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.current_school_type = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_in_school_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.currently_in_school = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_schoollevel
    ) m ON m.code = cl.dropout_school_level_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.dropout_school_level = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_savings_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.has_savings = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_periodresponse
    ) m ON m.code = cl.last_time_in_school_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.last_time_in_school = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_lifewish
    ) m ON m.code = cl.life_wish_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.life_wish = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_reasonnotinschool
    ) m ON m.code = cl.reason_not_in_school_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.reason_not_in_school = m.name;

    /*------------------------------- HIV Testing ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.enrolled_in_hiv_care_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.enrolled_in_hiv_care = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_tested_for_hiv_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.ever_tested_for_hiv = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.knowledge_of_hiv_test_centres_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.knowledge_of_hiv_test_centres = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_hivtestresultresponse
    ) m ON m.code = cl.last_test_result_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.last_test_result = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_periodresponse
    ) m ON m.code = cl.period_last_tested_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.period_last_tested = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_reasonnotinhivcare
    ) m ON m.code = cl.reason_not_in_hiv_care_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.reason_not_in_hiv_care = m.name;


  END $$
DELIMITER ;

-- ------------------------------------- insert into flat table ---------

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_populate_flat_enrollment_table$$
CREATE PROCEDURE sp_populate_flat_enrollment_table()
BEGIN

DECLARE record_id INT(11);
INSERT INTO dreams_production.DreamsApp_flatenrollmenttablelog(date_started, activity) VALUES(NOW(), 'First time population of table');
SET record_id = LAST_INSERT_ID();

INSERT INTO dreams_production.flat_dreams_enrollment(
client_id,
first_name,
middle_name,
last_name,
date_of_birth,
verification_document_id,
verification_document_other,
verification_doc_no,
date_of_enrollment,
phone_number,
dss_id_number,
informal_settlement,
village,
landmark,
dreams_id,
guardian_name,
relationship_with_guardian,
guardian_phone_number,
guardian_national_id,
county_of_residence_id,
implementing_partner_id,
marital_status_id,
sub_county_id,
ward_id,
ward_name,
sub_county_code,
sub_county_name,
county_code,
county_name,
head_of_household_id,
head_of_household_other,
age_of_household_head,
is_father_alive,
is_mother_alive,
is_parent_chronically_ill,
main_floor_material_id,
main_floor_material_other,
main_roof_material_id,
main_roof_material_other,
main_wall_material_id,
main_wall_material_other,
source_of_drinking_water_id,
source_of_drinking_water_other,
no_of_adults,
no_of_females,
no_of_males,
no_of_children,
currently_in_ct_program_id,
current_ct_program,
ever_enrolled_in_ct_program_id,
ever_missed_full_day_food_in_4wks_id,
has_disability_id,
no_of_days_missed_food_in_4wks_id,
no_of_people_in_household,
age_at_first_sexual_encounter,
sex_partners_in_last_12months,
age_of_last_partner_id,
age_of_second_last_partner_id,
age_of_third_last_partner_id,
ever_had_sex_id,
has_sexual_partner_id,
know_last_partner_hiv_status_id,
know_second_last_partner_hiv_status_id,
know_third_last_partner_hiv_status_id,
last_partner_circumcised_id,
received_money_gift_for_sex_id,
second_last_partner_circumcised_id,
third_last_partner_circumcised_id,
used_condom_with_last_partner_id,
used_condom_with_second_last_partner_id,
used_condom_with_third_last_partner_id,
no_of_biological_children,
anc_facility_name,
known_fp_method_other,
current_fp_method_other,
reason_not_using_fp_other,
current_anc_enrollment_id,
current_fp_method_id,
currently_pregnant_id,
currently_use_modern_fp_id,
fp_methods_awareness_id,
has_biological_children_id,
reason_not_using_fp_id,
drug_abuse_last_12months_other,
drug_used_last_12months_other,
drug_abuse_last_12months_id,
frequency_of_alcohol_last_12months_id,
produced_alcohol_last_12months_id,
used_alcohol_last_12months_id,
dreams_program_other,
gbv_help_provider_other,
preferred_gbv_help_provider_other,
economic_threat_ever_id,
economic_threat_last_3months_id,
humiliated_ever_id,
humiliated_last_3months_id,
insulted_ever_id,
insulted_last_3months_id,
knowledge_of_gbv_help_centres_id,
physical_violence_ever_id,
physical_violence_last_3months_id,
physically_forced_other_sex_acts_ever_id,
physically_forced_other_sex_acts_last_3months_id,
physically_forced_sex_ever_id,
physically_forced_sex_last_3months_id,
seek_help_after_gbv_id,
threatened_for_sexual_acts_ever_id,
threatened_for_sexual_acts_last_3months_id,
threats_to_hurt_ever_id,
threats_to_hurt_last_3months_id,
current_school_name,
current_class,
current_school_level_other,
current_education_supporter_other,
reason_not_in_school_other,
dropout_class,
life_wish_other,
current_income_source_other,
banking_place_other,
banking_place_id,
current_income_source_id,
current_school_level_id,
current_school_type_id,
currently_in_school_id,
dropout_school_level_id,
has_savings_id,
last_time_in_school_id,
life_wish_id,
reason_not_in_school_id,
care_facility_enrolled,
reason_not_in_hiv_care_other,
reason_never_tested_for_hiv_other,
enrolled_in_hiv_care_id,
ever_tested_for_hiv_id,
knowledge_of_hiv_test_centres_id,
last_test_result_id,
period_last_tested_id,
reason_not_in_hiv_care_id,
voided,
date_voided,
exit_status,
exit_date,
exit_reason,
age_at_enrollment,
current_age
)
select
d.id,
d.first_name,
d.middle_name,
d.last_name,
d.date_of_birth,
d.verification_document_id,
d.verification_document_other,
d.verification_doc_no,
d.date_of_enrollment,d.phone_number,
  d.dss_id_number,d.informal_settlement,d.village,d.landmark,d.dreams_id,d.guardian_name,d.relationship_with_guardian,d.guardian_phone_number,
  d.guardian_national_id,d.county_of_residence_id, d.implementing_partner_id,d.marital_status_id,d.sub_county_id,d.ward_id,l.ward_name,l.sub_county_code,
  l.sub_county_name,l.county_code,l.county_name,
i.head_of_household_id, i.head_of_household_other,i.age_of_household_head, i.is_father_alive, i.is_mother_alive, i.is_parent_chronically_ill,
  i.main_floor_material_id, i.main_floor_material_other, i.main_roof_material_id, i.main_roof_material_other, i.main_wall_material_id, i.main_wall_material_other,
  i.source_of_drinking_water_id,i.source_of_drinking_water_other, i.no_of_adults, i.no_of_females, i.no_of_males, i.no_of_children,
  i.currently_in_ct_program_id, i.current_ct_program, i.ever_enrolled_in_ct_program_id, i.ever_missed_full_day_food_in_4wks_id, i.has_disability_id,
  i.no_of_days_missed_food_in_4wks_id, i.no_of_people_in_household,
s.age_at_first_sexual_encounter,s.sex_partners_in_last_12months,s.age_of_last_partner_id,s.age_of_second_last_partner_id,
  s.age_of_third_last_partner_id,s.ever_had_sex_id,s.has_sexual_partner_id,s.know_last_partner_hiv_status_id,
  s.know_second_last_partner_hiv_status_id,s.know_third_last_partner_hiv_status_id,s.last_partner_circumcised_id,
  s.received_money_gift_for_sex_id,s.second_last_partner_circumcised_id,s.third_last_partner_circumcised_id,s.used_condom_with_last_partner_id,
  s.used_condom_with_second_last_partner_id,s.used_condom_with_third_last_partner_id,
rh.no_of_biological_children,rh.anc_facility_name,rh.known_fp_method_other,rh.current_fp_method_other,rh.reason_not_using_fp_other,
rh.current_anc_enrollment_id,rh.current_fp_method_id,rh.currently_pregnant_id,rh.currently_use_modern_fp_id,rh.fp_methods_awareness_id,
rh.has_biological_children_id,rh.reason_not_using_fp_id,
dr.drug_abuse_last_12months_other,dr.drug_used_last_12months_other,dr.drug_abuse_last_12months_id,dr.frequency_of_alcohol_last_12months_id,
  dr.produced_alcohol_last_12months_id,dr.used_alcohol_last_12months_id ,
 p.dreams_program_other,
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
hiv.reason_not_in_hiv_care_id,
d.voided,
d.date_voided,
(CASE d.exited WHEN 1 THEN "Yes" ELSE "" END) AS exited ,
DATE(d.date_exited) AS date_exited,
d.reason_exited,
DATEDIFF(d.date_of_enrollment, d.date_of_birth) DIV 365.25 as age_at_enrollment,
DATEDIFF(CURDATE(), d.date_of_birth) DIV 365.25 as current_age
from
dreams_production.DreamsApp_client AS d
LEFT OUTER JOIN dreams_production.DreamsApp_clientindividualandhouseholddata i on i.client_id=d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clientsexualactivitydata s ON s.client_id = d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clientreproductivehealthdata rh ON rh.client_id=d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clientdrugusedata dr on dr.client_id=d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clientparticipationindreams p on p.client_id=d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clientgenderbasedviolencedata gbv ON gbv.client_id=d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clienteducationandemploymentdata edu ON edu.client_id = d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clienthivtestingdata hiv ON hiv.client_id=d.id
LEFT OUTER JOIN (
SELECT
w.id as ward_code,
w.name as ward_name,
w.sub_county_id as sub_county_code,
s.name as sub_county_name,
s.county_id as county_code,
c.name as county_name
from dreams_production.DreamsApp_ward w
INNER JOIN dreams_production.DreamsApp_subcounty s ON s.id = w.sub_county_id
INNER JOIN dreams_production.DreamsApp_county c ON s.county_id = c.id
) l ON l.ward_code = d.ward_id
group by d.id
;

-- update many to many fields
UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      i_data.client_id,
      group_concat(disabilitytype_id) AS disability_types
      from dreams_production.DreamsApp_clientindividualandhouseholddata i_data
      INNER JOIN dreams_production.DreamsApp_clientindividualandhouseholddata_disability_type dt ON dt.clientindividualandhouseholddata_id = i_data.id
      GROUP BY i_data.client_id
  ) ind_data on ind_data.client_id = e.client_id
SET e.disability_types = ind_data.disability_types;

-- reproductive data: know fp methods

UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      rh.client_id,
      group_concat(familyplanningmethod_id) AS known_fp_methods
      FROM dreams_production.DreamsApp_clientreproductivehealthdata_known_fp_method fp
      INNER JOIN dreams_production.DreamsApp_clientreproductivehealthdata rh
      ON fp.clientreproductivehealthdata_id = rh.id
      GROUP BY rh.client_id
  ) rpr_data on rpr_data.client_id = e.client_id
SET e.known_fp_methods = rpr_data.known_fp_methods;

-- drugs used in past one year
UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      dd.client_id,
      group_concat(d.drug_id) AS drugs_used_in_last_12_months
      FROM dreams_production.DreamsApp_clientdrugusedata_drug_used_last_12months d
      INNER JOIN dreams_production.DreamsApp_clientdrugusedata dd ON d.clientdrugusedata_id = dd.id
      GROUP BY dd.client_id
  ) d_data on d_data.client_id = e.client_id
SET e.drugs_used_in_last_12_months = d_data.drugs_used_in_last_12_months;

-- dreams programs enrolled

UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      cpd.client_id   AS client_id,
      group_concat(dp.dreamsprogramme_id) AS programmes_enrolled
      FROM dreams_production.DreamsApp_clientparticipationindreams_dreams_program dp
      INNER JOIN dreams_production.DreamsApp_clientparticipationindreams cpd
      ON dp.clientparticipationindreams_id = cpd.id
      GROUP BY client_id
  ) p on p.client_id = e.client_id
SET e.programmes_enrolled = p.programmes_enrolled;

-- gbv sought provider
UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      gbv.client_id,
      group_concat(provider.gbvhelpprovider_id) AS provider_list
      FROM dreams_production.DreamsApp_clientgenderbasedviolencedata_gbv_help_provider provider
      INNER JOIN dreams_production.DreamsApp_clientgenderbasedviolencedata gbv on gbv.id = provider.clientgenderbasedviolencedata_id
      GROUP BY gbv.client_id
  ) gbv on gbv.client_id = e.client_id
SET e.providers_sought = gbv.provider_list;

-- gbv preferred provider

UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      gbv.client_id,
      group_concat(provider.gbvhelpprovider_id) AS provider_list
      FROM dreams_production.DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_p1bce provider -- DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_provider
      INNER JOIN dreams_production.DreamsApp_clientgenderbasedviolencedata gbv on gbv.id = provider.clientgenderbasedviolencedata_id
      GROUP BY gbv.client_id
  ) gbv on gbv.client_id = e.client_id
SET e.preferred_providers = gbv.provider_list;

-- current education supporter

UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      ed.client_id,
      group_concat(educationsupporter_id)   AS current_edu_supporter_list
      FROM dreams_production.DreamsApp_clienteducationandemploymentdata_current_educationebf4 s -- DreamsApp_clienteducationandemploymentdata_current_education_supporter s
      INNER JOIN dreams_production.DreamsApp_clienteducationandemploymentdata ed ON ed.id = s.clienteducationandemploymentdata_id
      GROUP BY ed.client_id
  ) ed on ed.client_id = e.client_id
SET e.current_edu_supporter_list = ed.current_edu_supporter_list;

-- reason never tested for hiv

UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      hiv_d.client_id,
      group_concat(rn.reasonnottestedforhiv_id) AS reason_not_tested_for_hiv
      FROM dreams_production.DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv rn
      INNER JOIN dreams_production.DreamsApp_clienthivtestingdata hiv_d ON hiv_d.id=rn.clienthivtestingdata_id
      GROUP BY hiv_d.client_id
  ) hiv on hiv.client_id = e.client_id
SET e.reason_not_tested_for_hiv = hiv.reason_not_tested_for_hiv;

UPDATE dreams_production.DreamsApp_flatenrollmenttablelog SET date_completed = NOW() WHERE id=record_id;

END$$
DELIMITER ;


-- ------------------------------------------- pick changes after initial setup and population      -------------------------------------

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_flat_enrollment_table$$
CREATE PROCEDURE sp_update_flat_enrollment_table()
BEGIN

DECLARE record_id INT(11);
DECLARE last_update_time DATETIME;
SELECT max(date_started) into last_update_time from dreams_production.DreamsApp_flatenrollmenttablelog;
INSERT INTO dreams_production.DreamsApp_flatenrollmenttablelog(date_started, activity) VALUES(NOW(), 'Table Updates');
SET record_id = LAST_INSERT_ID();

INSERT INTO dreams_production.flat_dreams_enrollment(
client_id,
first_name,
middle_name,
last_name,
date_of_birth,
verification_document_id,
verification_document_other,
verification_doc_no,
date_of_enrollment,
phone_number,
dss_id_number,
informal_settlement,
village,
landmark,
dreams_id,
guardian_name,
relationship_with_guardian,
guardian_phone_number,
guardian_national_id,
county_of_residence_id,
implementing_partner_id,
marital_status_id,
sub_county_id,
ward_id,
ward_name,
sub_county_code,
sub_county_name,
county_code,
county_name,
head_of_household_id,
head_of_household_other,
age_of_household_head,
is_father_alive,
is_mother_alive,
is_parent_chronically_ill,
main_floor_material_id,
main_floor_material_other,
main_roof_material_id,
main_roof_material_other,
main_wall_material_id,
main_wall_material_other,
source_of_drinking_water_id,
source_of_drinking_water_other,
no_of_adults,
no_of_females,
no_of_males,
no_of_children,
currently_in_ct_program_id,
current_ct_program,
ever_enrolled_in_ct_program_id,
ever_missed_full_day_food_in_4wks_id,
has_disability_id,
no_of_days_missed_food_in_4wks_id,
no_of_people_in_household,
age_at_first_sexual_encounter,
sex_partners_in_last_12months,
age_of_last_partner_id,
age_of_second_last_partner_id,
age_of_third_last_partner_id,
ever_had_sex_id,
has_sexual_partner_id,
know_last_partner_hiv_status_id,
know_second_last_partner_hiv_status_id,
know_third_last_partner_hiv_status_id,
last_partner_circumcised_id,
received_money_gift_for_sex_id,
second_last_partner_circumcised_id,
third_last_partner_circumcised_id,
used_condom_with_last_partner_id,
used_condom_with_second_last_partner_id,
used_condom_with_third_last_partner_id,
no_of_biological_children,
anc_facility_name,
known_fp_method_other,
current_fp_method_other,
reason_not_using_fp_other,
current_anc_enrollment_id,
current_fp_method_id,
currently_pregnant_id,
currently_use_modern_fp_id,
fp_methods_awareness_id,
has_biological_children_id,
reason_not_using_fp_id,
drug_abuse_last_12months_other,
drug_used_last_12months_other,
drug_abuse_last_12months_id,
frequency_of_alcohol_last_12months_id,
produced_alcohol_last_12months_id,
used_alcohol_last_12months_id,
dreams_program_other,
gbv_help_provider_other,
preferred_gbv_help_provider_other,
economic_threat_ever_id,
economic_threat_last_3months_id,
humiliated_ever_id,
humiliated_last_3months_id,
insulted_ever_id,
insulted_last_3months_id,
knowledge_of_gbv_help_centres_id,
physical_violence_ever_id,
physical_violence_last_3months_id,
physically_forced_other_sex_acts_ever_id,
physically_forced_other_sex_acts_last_3months_id,
physically_forced_sex_ever_id,
physically_forced_sex_last_3months_id,
seek_help_after_gbv_id,
threatened_for_sexual_acts_ever_id,
threatened_for_sexual_acts_last_3months_id,
threats_to_hurt_ever_id,
threats_to_hurt_last_3months_id,
current_school_name,
current_class,
current_school_level_other,
current_education_supporter_other,
reason_not_in_school_other,
dropout_class,
life_wish_other,
current_income_source_other,
banking_place_other,
banking_place_id,
current_income_source_id,
current_school_level_id,
current_school_type_id,
currently_in_school_id,
dropout_school_level_id,
has_savings_id,
last_time_in_school_id,
life_wish_id,
reason_not_in_school_id,
care_facility_enrolled,
reason_not_in_hiv_care_other,
reason_never_tested_for_hiv_other,
enrolled_in_hiv_care_id,
ever_tested_for_hiv_id,
knowledge_of_hiv_test_centres_id,
last_test_result_id,
period_last_tested_id,
reason_not_in_hiv_care_id,
voided,
date_voided,
exit_status,
exit_date,
exit_reason,
age_at_enrollment,
current_age
)
select
d.id,
d.first_name,
d.middle_name,
d.last_name,
d.date_of_birth,
d.verification_document_id,
d.verification_document_other,
d.verification_doc_no,
d.date_of_enrollment,d.phone_number,
  d.dss_id_number,d.informal_settlement,d.village,d.landmark,d.dreams_id,d.guardian_name,d.relationship_with_guardian,d.guardian_phone_number,
  d.guardian_national_id,d.county_of_residence_id, d.implementing_partner_id,d.marital_status_id,d.sub_county_id,d.ward_id,l.ward_name,l.sub_county_code,
  l.sub_county_name,l.county_code,l.county_name,
i.head_of_household_id, i.head_of_household_other,i.age_of_household_head, i.is_father_alive, i.is_mother_alive, i.is_parent_chronically_ill,
  i.main_floor_material_id, i.main_floor_material_other, i.main_roof_material_id, i.main_roof_material_other, i.main_wall_material_id, i.main_wall_material_other,
  i.source_of_drinking_water_id,i.source_of_drinking_water_other, i.no_of_adults, i.no_of_females, i.no_of_males, i.no_of_children,
  i.currently_in_ct_program_id, i.current_ct_program, i.ever_enrolled_in_ct_program_id, i.ever_missed_full_day_food_in_4wks_id, i.has_disability_id,
  i.no_of_days_missed_food_in_4wks_id, i.no_of_people_in_household,
s.age_at_first_sexual_encounter,s.sex_partners_in_last_12months,s.age_of_last_partner_id,s.age_of_second_last_partner_id,
  s.age_of_third_last_partner_id,s.ever_had_sex_id,s.has_sexual_partner_id,s.know_last_partner_hiv_status_id,
  s.know_second_last_partner_hiv_status_id,s.know_third_last_partner_hiv_status_id,s.last_partner_circumcised_id,
  s.received_money_gift_for_sex_id,s.second_last_partner_circumcised_id,s.third_last_partner_circumcised_id,s.used_condom_with_last_partner_id,
  s.used_condom_with_second_last_partner_id,s.used_condom_with_third_last_partner_id,
rh.no_of_biological_children,rh.anc_facility_name,rh.known_fp_method_other,rh.current_fp_method_other,rh.reason_not_using_fp_other,
rh.current_anc_enrollment_id,rh.current_fp_method_id,rh.currently_pregnant_id,rh.currently_use_modern_fp_id,rh.fp_methods_awareness_id,
rh.has_biological_children_id,rh.reason_not_using_fp_id,
dr.drug_abuse_last_12months_other,dr.drug_used_last_12months_other,dr.drug_abuse_last_12months_id,dr.frequency_of_alcohol_last_12months_id,
  dr.produced_alcohol_last_12months_id,dr.used_alcohol_last_12months_id ,
 p.dreams_program_other,
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
hiv.reason_not_in_hiv_care_id,
d.voided,
d.date_voided,
(CASE d.exited WHEN 1 THEN "Yes" ELSE "" END) AS exited ,
DATE(d.date_exited) AS date_exited,
d.reason_exited,
DATEDIFF(d.date_of_enrollment, d.date_of_birth) DIV 365.25 as age_at_enrollment,
DATEDIFF(CURDATE(), d.date_of_birth) DIV 365.25 as current_age
from
dreams_production.DreamsApp_client AS d
LEFT OUTER JOIN dreams_production.DreamsApp_clientindividualandhouseholddata i on i.client_id=d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clientsexualactivitydata s ON s.client_id = d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clientreproductivehealthdata rh ON rh.client_id=d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clientdrugusedata dr on dr.client_id=d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clientparticipationindreams p on p.client_id=d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clientgenderbasedviolencedata gbv ON gbv.client_id=d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clienteducationandemploymentdata edu ON edu.client_id = d.id
LEFT OUTER JOIN dreams_production.DreamsApp_clienthivtestingdata hiv ON hiv.client_id=d.id
LEFT OUTER JOIN (
SELECT
w.id as ward_code,
w.name as ward_name,
w.sub_county_id as sub_county_code,
s.name as sub_county_name,
s.county_id as county_code,
c.name as county_name
from dreams_production.DreamsApp_ward w
INNER JOIN dreams_production.DreamsApp_subcounty s ON s.id = w.sub_county_id
INNER JOIN dreams_production.DreamsApp_county c ON s.county_id = c.id
) l ON l.ward_code = d.ward_id
where (d.date_created >= last_update_time or d.date_changed >= last_update_time)
  or (i.date_created >= last_update_time or i.date_changed >= last_update_time)
  or (s.date_created >= last_update_time or s.date_changed >= last_update_time)
  or (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)
  or (dr.date_created >= last_update_time or dr.date_changed >= last_update_time)
  or (p.date_created >= last_update_time or p.date_changed >= last_update_time)
  or (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)
  or (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)
  or (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)
group by d.id
ON DUPLICATE KEY UPDATE
first_name=VALUES(first_name),
middle_name=VALUES(middle_name),
last_name=VALUES(last_name),
date_of_birth=VALUES(date_of_birth),
verification_document_id=VALUES(verification_document_id),
verification_document_other=VALUES(verification_document_other),
verification_doc_no=VALUES(verification_doc_no),
date_of_enrollment=VALUES(date_of_enrollment),
phone_number=VALUES(phone_number),
dss_id_number=VALUES(dss_id_number),
informal_settlement=VALUES(informal_settlement),
village=VALUES(village),
landmark=VALUES(landmark),
dreams_id=VALUES(dreams_id),
guardian_name=VALUES(guardian_name),
relationship_with_guardian=VALUES(relationship_with_guardian),
guardian_phone_number=VALUES(guardian_phone_number),
guardian_national_id=VALUES(guardian_national_id),
county_of_residence_id=VALUES(county_of_residence_id),
implementing_partner_id=VALUES(implementing_partner_id),
marital_status_id=VALUES(marital_status_id),
sub_county_id=VALUES(sub_county_id),
ward_id=VALUES(ward_id),
ward_name=VALUES(ward_name),
sub_county_code=VALUES(sub_county_code),
sub_county_name=VALUES(sub_county_name),
county_code=VALUES(county_code),
county_name=VALUES(county_name),
head_of_household_id=VALUES(head_of_household_id),
head_of_household_other=VALUES(head_of_household_other),
age_of_household_head=VALUES(age_of_household_head),
is_father_alive=VALUES(is_father_alive),
is_mother_alive=VALUES(is_mother_alive),
is_parent_chronically_ill=VALUES(is_parent_chronically_ill),
main_floor_material_id=VALUES(main_floor_material_id),
main_floor_material_other=VALUES(main_floor_material_other),
main_roof_material_id=VALUES(main_roof_material_id),
main_roof_material_other=VALUES(main_roof_material_other),
main_wall_material_id=VALUES(main_wall_material_id),
main_wall_material_other=VALUES(main_wall_material_other),
source_of_drinking_water_id=VALUES(source_of_drinking_water_id),
source_of_drinking_water_other=VALUES(source_of_drinking_water_other),
no_of_adults=VALUES(no_of_adults),
no_of_females=VALUES(no_of_females),
no_of_males=VALUES(no_of_males),
no_of_children=VALUES(no_of_children),
currently_in_ct_program_id=VALUES(currently_in_ct_program_id),
current_ct_program=VALUES(current_ct_program),
ever_enrolled_in_ct_program_id=VALUES(ever_enrolled_in_ct_program_id),
ever_missed_full_day_food_in_4wks_id=VALUES(ever_missed_full_day_food_in_4wks_id),
has_disability_id=VALUES(has_disability_id),
no_of_days_missed_food_in_4wks_id=VALUES(no_of_days_missed_food_in_4wks_id),
no_of_people_in_household=VALUES(no_of_people_in_household),
age_at_first_sexual_encounter=VALUES(age_at_first_sexual_encounter),
sex_partners_in_last_12months=VALUES(sex_partners_in_last_12months),
age_of_last_partner_id=VALUES(age_of_last_partner_id),
age_of_second_last_partner_id=VALUES(age_of_second_last_partner_id),
age_of_third_last_partner_id=VALUES(age_of_third_last_partner_id),
ever_had_sex_id=VALUES(ever_had_sex_id),
has_sexual_partner_id=VALUES(has_sexual_partner_id),
know_last_partner_hiv_status_id=VALUES(know_last_partner_hiv_status_id),
know_second_last_partner_hiv_status_id=VALUES(know_second_last_partner_hiv_status_id),
know_third_last_partner_hiv_status_id=VALUES(know_third_last_partner_hiv_status_id),
last_partner_circumcised_id=VALUES(last_partner_circumcised_id),
received_money_gift_for_sex_id=VALUES(received_money_gift_for_sex_id),
second_last_partner_circumcised_id=VALUES(second_last_partner_circumcised_id),
third_last_partner_circumcised_id=VALUES(third_last_partner_circumcised_id),
used_condom_with_last_partner_id=VALUES(used_condom_with_last_partner_id),
used_condom_with_second_last_partner_id=VALUES(used_condom_with_second_last_partner_id),
used_condom_with_third_last_partner_id=VALUES(used_condom_with_third_last_partner_id),
no_of_biological_children=VALUES(no_of_biological_children),
anc_facility_name=VALUES(anc_facility_name),
known_fp_method_other=VALUES(known_fp_method_other),
current_fp_method_other=VALUES(current_fp_method_other),
reason_not_using_fp_other=VALUES(reason_not_using_fp_other),
current_anc_enrollment_id=VALUES(current_anc_enrollment_id),
current_fp_method_id=VALUES(current_fp_method_id),
currently_pregnant_id=VALUES(currently_pregnant_id),
currently_use_modern_fp_id=VALUES(currently_use_modern_fp_id),
fp_methods_awareness_id=VALUES(fp_methods_awareness_id),
has_biological_children_id=VALUES(has_biological_children_id),
reason_not_using_fp_id=VALUES(reason_not_using_fp_id),
drug_abuse_last_12months_other=VALUES(drug_abuse_last_12months_other),
drug_used_last_12months_other=VALUES(drug_used_last_12months_other),
drug_abuse_last_12months_id=VALUES(drug_abuse_last_12months_id),
frequency_of_alcohol_last_12months_id=VALUES(frequency_of_alcohol_last_12months_id),
produced_alcohol_last_12months_id=VALUES(produced_alcohol_last_12months_id),
used_alcohol_last_12months_id=VALUES(used_alcohol_last_12months_id),
dreams_program_other=VALUES(dreams_program_other),
gbv_help_provider_other=VALUES(gbv_help_provider_other),
preferred_gbv_help_provider_other=VALUES(preferred_gbv_help_provider_other),
economic_threat_ever_id=VALUES(economic_threat_ever_id),
economic_threat_last_3months_id=VALUES(economic_threat_last_3months_id),
humiliated_ever_id=VALUES(humiliated_ever_id),
humiliated_last_3months_id=VALUES(humiliated_last_3months_id),
insulted_ever_id=VALUES(insulted_ever_id),
insulted_last_3months_id=VALUES(insulted_last_3months_id),
knowledge_of_gbv_help_centres_id=VALUES(knowledge_of_gbv_help_centres_id),
physical_violence_ever_id=VALUES(physical_violence_ever_id),
physical_violence_last_3months_id=VALUES(physical_violence_last_3months_id),
physically_forced_other_sex_acts_ever_id=VALUES(physically_forced_other_sex_acts_ever_id),
physically_forced_other_sex_acts_last_3months_id=VALUES(physically_forced_other_sex_acts_last_3months_id),
physically_forced_sex_ever_id=VALUES(physically_forced_sex_ever_id),
physically_forced_sex_last_3months_id=VALUES(physically_forced_sex_last_3months_id),
seek_help_after_gbv_id=VALUES(seek_help_after_gbv_id),
threatened_for_sexual_acts_ever_id=VALUES(threatened_for_sexual_acts_ever_id),
threatened_for_sexual_acts_last_3months_id=VALUES(threatened_for_sexual_acts_last_3months_id),
threats_to_hurt_ever_id=VALUES(threats_to_hurt_ever_id),
threats_to_hurt_last_3months_id=VALUES(threats_to_hurt_last_3months_id),
current_school_name=VALUES(current_school_name),
current_class=VALUES(current_class),
current_school_level_other=VALUES(current_school_level_other),
current_education_supporter_other=VALUES(current_education_supporter_other),
reason_not_in_school_other=VALUES(reason_not_in_school_other),
dropout_class=VALUES(dropout_class),
life_wish_other=VALUES(life_wish_other),
current_income_source_other=VALUES(current_income_source_other),
banking_place_other=VALUES(banking_place_other),
banking_place_id=VALUES(banking_place_id),
current_income_source_id=VALUES(current_income_source_id),
current_school_level_id=VALUES(current_school_level_id),
current_school_type_id=VALUES(current_school_type_id),
currently_in_school_id=VALUES(currently_in_school_id),
dropout_school_level_id=VALUES(dropout_school_level_id),
has_savings_id=VALUES(has_savings_id),
last_time_in_school_id=VALUES(last_time_in_school_id),
life_wish_id=VALUES(life_wish_id),
reason_not_in_school_id=VALUES(reason_not_in_school_id),
care_facility_enrolled=VALUES(care_facility_enrolled),
reason_not_in_hiv_care_other=VALUES(reason_not_in_hiv_care_other),
reason_never_tested_for_hiv_other=VALUES(reason_never_tested_for_hiv_other),
enrolled_in_hiv_care_id=VALUES(enrolled_in_hiv_care_id),
ever_tested_for_hiv_id=VALUES(ever_tested_for_hiv_id),
knowledge_of_hiv_test_centres_id=VALUES(knowledge_of_hiv_test_centres_id),
last_test_result_id=VALUES(last_test_result_id),
period_last_tested_id=VALUES(period_last_tested_id),
reason_not_in_hiv_care_id=VALUES(reason_not_in_hiv_care_id),
voided=VALUES(voided),
date_voided=VALUES(date_voided),
exit_status=VALUES(exit_status),
exit_date=VALUES(exit_date),
exit_reason=VALUES(exit_reason),
age_at_enrollment=VALUES(age_at_enrollment),
current_age=VALUES(current_age)
;

-- update current age
UPDATE dreams_production.flat_dreams_enrollment set current_age = DATEDIFF(CURDATE(), date_of_birth) DIV 365.25 where current_age != DATEDIFF(CURDATE(), date_of_birth) DIV 365.25 ;

-- update many to many fields
UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      i_data.client_id,
      group_concat(disabilitytype_id) AS disability_types
      from dreams_production.DreamsApp_clientindividualandhouseholddata i_data
      INNER JOIN dreams_production.DreamsApp_clientindividualandhouseholddata_disability_type dt ON dt.clientindividualandhouseholddata_id = i_data.id
      WHERE  (i_data.date_created > last_update_time or i_data.date_changed > last_update_time)
      GROUP BY i_data.client_id
  ) ind_data on ind_data.client_id = e.client_id
SET e.disability_types = ind_data.disability_types;

-- reproductive data: know fp methods

UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      rh.client_id,
      group_concat(familyplanningmethod_id) AS known_fp_methods
      FROM dreams_production.DreamsApp_clientreproductivehealthdata_known_fp_method fp
      INNER JOIN dreams_production.DreamsApp_clientreproductivehealthdata rh
      ON fp.clientreproductivehealthdata_id = rh.id
      WHERE  (rh.date_created > last_update_time or rh.date_changed > last_update_time)
      GROUP BY rh.client_id
  ) rpr_data on rpr_data.client_id = e.client_id
SET e.known_fp_methods = rpr_data.known_fp_methods;

-- drugs used in past one year
UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      dd.client_id,
      group_concat(d.drug_id) AS drugs_used_in_last_12_months
      FROM dreams_production.DreamsApp_clientdrugusedata_drug_used_last_12months d
      INNER JOIN dreams_production.DreamsApp_clientdrugusedata dd ON d.clientdrugusedata_id = dd.id
      WHERE  (dd.date_created > last_update_time or dd.date_changed > last_update_time)
      GROUP BY dd.client_id
  ) d_data on d_data.client_id = e.client_id
SET e.drugs_used_in_last_12_months = d_data.drugs_used_in_last_12_months;

-- dreams programs enrolled

UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      cpd.client_id   AS client_id,
      group_concat(dp.dreamsprogramme_id) AS programmes_enrolled
      FROM dreams_production.DreamsApp_clientparticipationindreams_dreams_program dp
      INNER JOIN dreams_production.DreamsApp_clientparticipationindreams cpd
      ON dp.clientparticipationindreams_id = cpd.id
      WHERE  (cpd.date_created > last_update_time or cpd.date_changed > last_update_time)
      GROUP BY client_id
  ) p on p.client_id = e.client_id
SET e.programmes_enrolled = p.programmes_enrolled;

-- gbv sought provider
UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      gbv.client_id,
      group_concat(provider.gbvhelpprovider_id) AS provider_list
      FROM dreams_production.DreamsApp_clientgenderbasedviolencedata_gbv_help_provider provider
      INNER JOIN dreams_production.DreamsApp_clientgenderbasedviolencedata gbv on gbv.id = provider.clientgenderbasedviolencedata_id
      WHERE  (gbv.date_created > last_update_time or gbv.date_changed > last_update_time)
      GROUP BY gbv.client_id
  ) gbv on gbv.client_id = e.client_id
SET e.providers_sought = gbv.provider_list;

-- gbv preferred provider

UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      gbv.client_id,
      group_concat(provider.gbvhelpprovider_id) AS provider_list
      FROM dreams_production.DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_p1bce provider -- DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_provider
      INNER JOIN dreams_production.DreamsApp_clientgenderbasedviolencedata gbv on gbv.id = provider.clientgenderbasedviolencedata_id
      WHERE  (gbv.date_created > last_update_time or gbv.date_changed > last_update_time)
      GROUP BY gbv.client_id
  ) gbv on gbv.client_id = e.client_id
SET e.preferred_providers = gbv.provider_list;

-- current education supporter

UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      ed.client_id,
      group_concat(educationsupporter_id)   AS current_edu_supporter_list
      FROM dreams_production.DreamsApp_clienteducationandemploymentdata_current_educationebf4 s -- DreamsApp_clienteducationandemploymentdata_current_education_supporter s
      INNER JOIN dreams_production.DreamsApp_clienteducationandemploymentdata ed ON ed.id = s.clienteducationandemploymentdata_id
      WHERE  (ed.date_created > last_update_time or ed.date_changed > last_update_time)
      GROUP BY ed.client_id
  ) ed on ed.client_id = e.client_id
SET e.current_edu_supporter_list = ed.current_edu_supporter_list;

-- reason never tested for hiv

UPDATE dreams_production.flat_dreams_enrollment e INNER JOIN (
    SELECT
      hiv_d.client_id,
      group_concat(rn.reasonnottestedforhiv_id) AS reason_not_tested_for_hiv
      FROM dreams_production.DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv rn
      INNER JOIN dreams_production.DreamsApp_clienthivtestingdata hiv_d ON hiv_d.id=rn.clienthivtestingdata_id
      WHERE  (hiv_d.date_created > last_update_time or hiv_d.date_changed > last_update_time)
      GROUP BY hiv_d.client_id
  ) hiv on hiv.client_id = e.client_id
SET e.reason_not_tested_for_hiv = hiv.reason_not_tested_for_hiv;

UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_implementingpartner
    ) ip ON ip.code = cl.implementing_partner_id
    INNER JOIN (SELECT id from DreamsApp_client d where (d.date_created >= last_update_time or d.date_changed >= last_update_time)) client on client.id = cl.client_id
    SET cl.implementing_partner = ip.name;

    /*Update verification document*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_verificationdocument
    ) v ON v.code = cl.verification_document_id
    INNER JOIN (SELECT id from DreamsApp_client d where (d.date_created >= last_update_time or d.date_changed >= last_update_time)) client on client.id = cl.client_id
    SET cl.verification_document = v.name;

    /*Update marital status*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_maritalstatus
    ) m ON m.code = cl.marital_status_id
    INNER JOIN (SELECT id from DreamsApp_client d where (d.date_created >= last_update_time or d.date_changed >= last_update_time)) client on client.id = cl.client_id
    SET cl.marital_status = m.name;

-- -------------------------------------- individual and household ----------------------------------------------------
    /*Update head of household*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_householdhead
    ) m ON m.code = cl.head_of_household_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.head_of_household = m.name;

    /*Update parent status*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.is_father_alive
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.father_alive = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.is_mother_alive
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.mother_alive = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.is_parent_chronically_ill
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.parent_chronically_ill = m.name;

    /* Wall, floor, roof, drinking water */
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_floormaterial
    ) m ON m.code = cl.main_floor_material_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.main_floor_material = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_roofingmaterial
    ) m ON m.code = cl.main_roof_material_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.main_roof_material = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_wallmaterial
    ) m ON m.code = cl.main_wall_material_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.main_wall_material = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_drinkingwater
    ) m ON m.code = cl.source_of_drinking_water_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.source_of_drinking_water = m.name;

    /* ct enrollment, disability, hunger*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_in_ct_program_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.currently_in_ct_program = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_enrolled_in_ct_program_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.ever_enrolled_in_ct_program = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_missed_full_day_food_in_4wks_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.ever_missed_full_day_food_in_4wks = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_disability_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.has_disability = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.no_of_days_missed_food_in_4wks_id
    INNER JOIN (SELECT client_id from DreamsApp_clientindividualandhouseholddata i  where (i.date_created >= last_update_time or i.date_changed >= last_update_time)) i on i.client_id = cl.client_id
    SET cl.no_of_days_missed_food_in_4wks = m.name;

    /* ------------------------------------------ sexuality -------------------------------------------------*/


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_ageofsexualpartner
    ) m ON m.code = cl.age_of_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.age_of_last_partner = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_ageofsexualpartner
    ) m ON m.code = cl.age_of_second_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.age_of_second_last_partner = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_ageofsexualpartner
    ) m ON m.code = cl.age_of_third_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.age_of_third_last_partner = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_had_sex_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.ever_had_sex = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_sexual_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.has_sexual_partner = m.name;

  /* partner hiv status*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.know_last_partner_hiv_status_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.know_last_partner_hiv_status = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.know_second_last_partner_hiv_status_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.know_second_last_partner_hiv_status = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.know_third_last_partner_hiv_status_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.know_third_last_partner_hiv_status = m.name;

    /* ------------partner circumcision-------------*/

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.last_partner_circumcised_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.last_partner_circumcised = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.second_last_partner_circumcised_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.second_last_partner_circumcised = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.third_last_partner_circumcised_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.third_last_partner_circumcised = m.name;

    /*------------ condom use --------------------*/

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.used_condom_with_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.used_condom_with_last_partner = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.used_condom_with_second_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.used_condom_with_second_last_partner = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.used_condom_with_third_last_partner_id
    INNER JOIN (SELECT client_id from DreamsApp_clientsexualactivitydata s   where (s.date_created >= last_update_time or s.date_changed >= last_update_time)) s on s.client_id = cl.client_id
    SET cl.used_condom_with_third_last_partner = m.name;

/*--------------- Reproductive Health ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.current_anc_enrollment_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.current_anc_enrollment = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_familyplanningmethod
    ) m ON m.code = cl.current_fp_method_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.current_fp_method = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_pregnant_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.currently_pregnant = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_use_modern_fp_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.currently_use_modern_fp = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.fp_methods_awareness_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.fp_methods_awareness = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_biological_children_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.has_biological_children = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_reasonnotusingfamilyplanning
    ) m ON m.code = cl.reason_not_using_fp_id
    INNER JOIN (SELECT client_id from DreamsApp_clientreproductivehealthdata rh  where (rh.date_created >= last_update_time or rh.date_changed >= last_update_time)) rh on rh.client_id = cl.client_id
    SET cl.reason_not_using_fp = m.name;

/*------------------------------- Drug Use ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.drug_abuse_last_12months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientdrugusedata dr  where (dr.date_created >= last_update_time or dr.date_changed >= last_update_time)) dr on dr.client_id = cl.client_id
    SET cl.drug_abuse_last_12months = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.frequency_of_alcohol_last_12months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientdrugusedata dr  where (dr.date_created >= last_update_time or dr.date_changed >= last_update_time)) dr on dr.client_id = cl.client_id
    SET cl.frequency_of_alcohol_last_12months = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.produced_alcohol_last_12months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientdrugusedata dr  where (dr.date_created >= last_update_time or dr.date_changed >= last_update_time)) dr on dr.client_id = cl.client_id
    SET cl.produced_alcohol_last_12months = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.used_alcohol_last_12months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientdrugusedata dr  where (dr.date_created >= last_update_time or dr.date_changed >= last_update_time)) dr on dr.client_id = cl.client_id
    SET cl.used_alcohol_last_12months = m.name;

/*------------------------------- GBV ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.economic_threat_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.economic_threat_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.economic_threat_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.economic_threat_last_3months = m.name;
/*-------------------------------------------------------------*/

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.humiliated_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.humiliated_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.humiliated_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.humiliated_last_3months = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.insulted_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.insulted_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.insulted_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.insulted_last_3months = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.knowledge_of_gbv_help_centres_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.knowledge_of_gbv_help_centres = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.physical_violence_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physical_violence_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.physical_violence_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physical_violence_last_3months = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.physically_forced_other_sex_acts_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physically_forced_other_sex_acts_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.physically_forced_other_sex_acts_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physically_forced_other_sex_acts_last_3months = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.physically_forced_sex_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physically_forced_sex_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.physically_forced_sex_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.physically_forced_sex_last_3months = m.name;
/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.seek_help_after_gbv_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.seek_help_after_gbv = m.name;

/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threatened_for_sexual_acts_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threatened_for_sexual_acts_last_3months = m.name;

/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threatened_for_sexual_acts_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.threatened_for_sexual_acts_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threatened_for_sexual_acts_last_3months = m.name;

/*-------------------------------------------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.threats_to_hurt_ever_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threats_to_hurt_ever = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_frequencyresponse
    ) m ON m.code = cl.threats_to_hurt_last_3months_id
    INNER JOIN (SELECT client_id from DreamsApp_clientgenderbasedviolencedata gbv  where (gbv.date_created >= last_update_time or gbv.date_changed >= last_update_time)) gbv on gbv.client_id = cl.client_id
    SET cl.threats_to_hurt_last_3months = m.name;

    /*------------------------------- Education and Employment ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_bankingplace
    ) m ON m.code = cl.banking_place_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.banking_place = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_sourceofincome
    ) m ON m.code = cl.current_income_source_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.current_income_source = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_schoollevel
    ) m ON m.code = cl.current_school_level_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.current_school_level = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_schooltype
    ) m ON m.code = cl.current_school_type_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.current_school_type = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.currently_in_school_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.currently_in_school = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_schoollevel
    ) m ON m.code = cl.dropout_school_level_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.dropout_school_level = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.has_savings_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.has_savings = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_periodresponse
    ) m ON m.code = cl.last_time_in_school_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.last_time_in_school = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_lifewish
    ) m ON m.code = cl.life_wish_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.life_wish = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_reasonnotinschool
    ) m ON m.code = cl.reason_not_in_school_id
    INNER JOIN (SELECT client_id from DreamsApp_clienteducationandemploymentdata edu  where (edu.date_created >= last_update_time or edu.date_changed >= last_update_time)) edu on edu.client_id = cl.client_id
    SET cl.reason_not_in_school = m.name;

    /*------------------------------- HIV Testing ---------------------------*/
    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.enrolled_in_hiv_care_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.enrolled_in_hiv_care = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.ever_tested_for_hiv_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.ever_tested_for_hiv = m.name;


    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_categoricalresponse
    ) m ON m.code = cl.knowledge_of_hiv_test_centres_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.knowledge_of_hiv_test_centres = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_hivtestresultresponse
    ) m ON m.code = cl.last_test_result_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.last_test_result = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_periodresponse
    ) m ON m.code = cl.period_last_tested_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.period_last_tested = m.name;

    UPDATE dreams_production.flat_dreams_enrollment cl
    INNER JOIN (
      select code, name from DreamsApp_reasonnotinhivcare
    ) m ON m.code = cl.reason_not_in_hiv_care_id
    INNER JOIN (SELECT client_id from DreamsApp_clienthivtestingdata hiv  where (hiv.date_created >= last_update_time or hiv.date_changed >= last_update_time)) hiv on hiv.client_id = cl.client_id
    SET cl.reason_not_in_hiv_care = m.name;

UPDATE dreams_production.DreamsApp_flatenrollmenttablelog SET date_completed = NOW() WHERE id=record_id;

END$$
DELIMITER ;


----------------- ------------------------ exporting services data -----------------------------------------------

SELECT client_id,
i.dreams_id DREAMS_ID,
-- CONCAT_WS(" ",i.first_name, i.middle_name, i.last_name) AS client_name,
i.date_of_birth,
i.implementing_partner IP_NAME,
i.implementing_partner_id IP_CODE,
i.county_of_residence,
i.sub_county,
i.ward,
i.date_of_enrollment as date_of_enrollment,
DATE(i.intervention_date) date_of_intervention,
quartername as intervention_quarter,
DATE(i.date_created) date_created,
i.intervention_type_id intervention_type_code,
i.intervention as intervention_type_name,
i.intervention_category intervention_category_name,
i.hts_result_id hts_result_code,
i.hts_result hts_result_name,
i.pregnancy_test_result_id pregnancy_test_result_code,
i.pregnancy_test_result pregnancy_test_result_name,
i.client_ccc_number,
i.date_linked_to_ccc,
i.no_of_sessions_attended,
i.comment
from stag_client_intervention i WHERE voided=0;


-- ------------------------ procedures for cleaning dreams ids --------------------------------------

DELIMITER $$
DROP FUNCTION IF EXISTS cleanDreamsSerial$$
CREATE FUNCTION cleanDreamsSerial(implementing_partner_id INT, ward INT) RETURNS VARCHAR(200)
DETERMINISTIC
BEGIN
DECLARE new_serial INT(11);
SELECT
  (max(CONVERT(SUBSTRING_INDEX(clean.dreams_id, '/', -1), UNSIGNED INTEGER )) + 1) INTO new_serial
from stag_clean_dreams_id clean
WHERE clean.implementing_partner_id=implementing_partner_id and clean.ward_id=ward and clean.dreams_id  is not null  group by implementing_partner_id, ward_id;

IF new_serial is NULL THEN
SET new_serial = 1;
END IF;
return CONCAT(implementing_partner_id, '/', ward, '/',new_serial);
END$$
DELIMITER ;


-- -------------------------------- creates a temporary table to hold clean dreams ID
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_dreams_id_staging_tables$$
CREATE PROCEDURE sp_dreams_id_staging_tables()
BEGIN
drop table if EXISTS stag_clean_dreams_id;

  DROP TABLE IF EXISTS stag_clean_dreams_id;
CREATE TABLE `stag_clean_dreams_id` (
  `client_id` int(11)  ,
  `dreams_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `implementing_partner_id` int(11) DEFAULT NULL,
  `ward_id` int(11) DEFAULT NULL,
  `err` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  INDEX (client_id),
  INDEX (dreams_id),
  INDEX(implementing_partner_id),
  INDEX(ward_id),
  INDEX (implementing_partner_id, ward_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into stag_clean_dreams_id (client_id, dreams_id, implementing_partner_id, ward_id, err)
  SELECT c.id, c.dreams_id, c.implementing_partner_id, c.ward_id, x.dreams_id as err
  FROM dreams_production.DreamsApp_client c
  left JOIN (
SELECT
  id,
  implementing_partner_id,
  dreams_id,
  dreams_id as assigned_dreams_id,
  county_of_residence_id,
  sub_county_id,
  ward_id,
  ROUND (
        (
            LENGTH(dreams_id)
            - LENGTH( REPLACE ( dreams_id, "/", "") )
        ) / LENGTH("/")
    ) AS slash_count ,
  SUBSTRING_INDEX(dreams_id, '/', 1)  AS IP_CODE,
  SUBSTRING_INDEX(SUBSTRING_INDEX(dreams_id, '/', 2), '/', -1)   AS WARD_CODE,
  SUBSTRING_INDEX(dreams_id, '/', -1) AS dreams_serial
FROM DreamsApp_client
-- GROUP BY dreams_id
HAVING ward_id is not null and DreamsApp_client.implementing_partner_id is not null and (dreams_id in (NULL, 'NONE', 'n/a', 'N/A', 'None', '') or dreams_serial > 20000 or slash_count < 2)
      ) x on c.dreams_id = x.dreams_id and c.id=x.id where x.dreams_id is null;

drop table if EXISTS stag_dreams_ids_with_errors;
create table stag_dreams_ids_with_errors as
      SELECT
  id,
  implementing_partner_id,
  dreams_id,
  dreams_id as assigned_dreams_id,
  county_of_residence_id,
  sub_county_id,
  ward_id,
  ROUND (
        (
            LENGTH(dreams_id)
            - LENGTH( REPLACE ( dreams_id, "/", "") )
        ) / LENGTH("/")
    ) AS slash_count ,
  SUBSTRING_INDEX(dreams_id, '/', 1)  AS IP_CODE,
  SUBSTRING_INDEX(SUBSTRING_INDEX(dreams_id, '/', 2), '/', -1)   AS WARD_CODE,
  SUBSTRING_INDEX(dreams_id, '/', -1) AS dreams_serial
FROM DreamsApp_client
-- GROUP BY dreams_id
HAVING ward_id is not null and DreamsApp_client.implementing_partner_id is not null and (dreams_id in (NULL, 'NONE', 'n/a', 'N/A', 'None', '') or dreams_serial > 20000 or slash_count < 2);
END;
  $$
DELIMITER ;

-- ----------------------    cursor to hold and correct dreams_id ------------

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_fetch_erroneous_dreams_id$$
CREATE PROCEDURE sp_fetch_erroneous_dreams_id()
BEGIN

  DECLARE no_more_rows BOOLEAN;
  DECLARE implementing_partner INT(11);
  DECLARE clientID INT(11);
  DECLARE dreamsID VARCHAR(50);
  DECLARE wardID INT(11);
  DECLARE v_row_count INT(11);

  DECLARE erroneous_records CURSOR FOR
    SELECT id, implementing_partner_id, dreams_id, ward_id FROM stag_dreams_ids_with_errors;
  DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET no_more_rows = TRUE;

  OPEN erroneous_records;
  SET v_row_count = FOUND_ROWS();

  IF v_row_count > 0 THEN
    dreams_ids: LOOP
    FETCH erroneous_records INTO clientID, implementing_partner, dreamsID, wardID;

    IF no_more_rows THEN
      CLOSE erroneous_records;
      LEAVE dreams_ids;
    END IF;
    CALL sp_update_erroneous_dreams_id(clientID, dreamsID, implementing_partner, wardID);

    END LOOP dreams_ids;
  ELSE
    SELECT "NO ROWS WERE FOUND";
  END IF;

END
$$
DELIMITER ;

-- ------------------------------ procedure to update erroneous ids ------------


DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_erroneous_dreams_id$$
CREATE PROCEDURE sp_update_erroneous_dreams_id(IN clientID INT(11), IN dreamsID VARCHAR(100), IN implementingPartnerID INT(11), IN ward INT(11))
BEGIN

  DECLARE new_dreams_id VARCHAR(100);
  SELECT cleanDreamsSerial(implementingPartnerID, ward) INTO new_dreams_id;
  UPDATE DreamsApp_client c
    SET c.dreams_id = new_dreams_id, c.date_changed = NOW() WHERE c.id=clientID;

  UPDATE stag_dreams_ids_with_errors
    SET assigned_dreams_id = new_dreams_id WHERE id=clientID;

  INSERT INTO stag_clean_dreams_id(client_id, dreams_id, implementing_partner_id, ward_id) VALUES (clientID, new_dreams_id, implementingPartnerID,ward );
END
$$
DELIMITER ;


-- FIXING MISSING WARD IDS FROM LIST PROVIDED BY IPS
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_fix_missing_enrollment_ward$$
CREATE PROCEDURE sp_fix_missing_enrollment_ward(IN wardID INT(11))
BEGIN

  DECLARE no_more_rows BOOLEAN;
  DECLARE dreamsID VARCHAR(50);
  DECLARE v_row_count INT(11);

  DECLARE erroneous_records CURSOR FOR
    SELECT dreams_id FROM missing_enrollment_ward WHERE ward_id = wardID ;

  DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET no_more_rows = TRUE;

  OPEN erroneous_records;
  SET v_row_count = FOUND_ROWS();
  SELECT v_row_count as 'found rows';
  IF v_row_count > 0 THEN
    dreams_ids: LOOP
      FETCH erroneous_records INTO dreamsID;

      IF no_more_rows THEN
        CLOSE erroneous_records;
        LEAVE dreams_ids;
      END IF;
      CALL sp_update_missing_ward_id(dreamsID, wardID);

    END LOOP dreams_ids;
  ELSE
    SELECT "NO ROWS WERE FOUND";
  END IF;

END
$$
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_missing_ward_id$$
CREATE PROCEDURE sp_update_missing_ward_id(IN dreamsID VARCHAR(100), IN ward INT(11))
BEGIN

  DECLARE occurence INT(11);
  SELECT COUNT(dreams_id) from DreamsApp_client where dreams_id = dreamsID INTO occurence;
  IF occurence > 1 THEN
    UPDATE missing_enrollment_ward SET status=3 WHERE dreams_id = dreamsID;
  ELSEIF occurence = 0 THEN
    UPDATE missing_enrollment_ward SET status=2 WHERE dreams_id = dreamsID;
  ELSEIF occurence = 1 THEN
    UPDATE DreamsApp_client SET ward_id=ward where dreams_id=dreamsID;
    UPDATE missing_enrollment_ward SET status=1 WHERE dreams_id = dreamsID;
  END IF;

END
$$
DELIMITER ;


-- Voiding records of provided client_id
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_void_records$$
CREATE PROCEDURE sp_void_records()
BEGIN

  DECLARE no_more_rows BOOLEAN;
  DECLARE clientID INT(11);
  DECLARE v_row_count INT(11);

  DECLARE erroneous_records CURSOR FOR
    SELECT client_id FROM enrollment_missing_ip_and_dreams_id WHERE status=0;

  DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET no_more_rows = TRUE;


  OPEN erroneous_records;
  SET v_row_count = FOUND_ROWS();
  SELECT v_row_count as 'found rows';
  IF v_row_count > 0 THEN
    client_ids: LOOP
      FETCH erroneous_records INTO clientID;

      IF no_more_rows THEN
        CLOSE erroneous_records;
        LEAVE client_ids;
      END IF;
      CALL sp_void_individual_records(clientID);

    END LOOP client_ids;
  ELSE
    SELECT "NO ROWS WERE FOUND";
  END IF;

END
$$
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS sp_void_individual_records$$
CREATE PROCEDURE sp_void_individual_records(IN clientID INT(11), IN reason_voided_param VARCHAR(100))
BEGIN

  DECLARE occurence INT(11);
  DECLARE exec_status INT(11) DEFAULT 1;

  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
      SET exec_status = -1;
      ROLLBACK;
    END;
  -- perform all procedure calls within a transaction
  START TRANSACTION;


  SELECT COUNT(id) from DreamsApp_client where id = clientID INTO occurence;
  IF occurence > 1 THEN
    UPDATE enrollment_missing_ip_and_dreams_id SET status=3 WHERE client_id = clientID;
  ELSEIF occurence = 0 THEN
    UPDATE enrollment_missing_ip_and_dreams_id SET status=2 WHERE client_id = clientID;
  ELSEIF occurence = 1 THEN
    -- void all modules
    UPDATE DreamsApp_intervention set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientdrugusedata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clienteducationandemploymentdata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientgenderbasedviolencedata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clienthivtestingdata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientindividualandhouseholddata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientparticipationindreams set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientreproductivehealthdata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientsexualactivitydata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_client set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where id=clientID;

  END IF;

  UPDATE enrollment_missing_ip_and_dreams_id SET status=exec_status WHERE client_id = clientID;
  COMMIT;

END
$$
DELIMITER ;



-- Voiding records of provided CLIENT ID
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_void_individual_records_using_client_id$$
CREATE PROCEDURE sp_void_individual_records_using_client_id(IN clientID INT(11), IN reason_voided_param VARCHAR(100))
BEGIN

  DECLARE occurence INT(11);
  DECLARE exec_status INT(11) DEFAULT 1;
  DECLARE void_id INT(11);

  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
      SET exec_status = -1;
      ROLLBACK;
    END;
  -- perform all procedure calls within a transaction
  START TRANSACTION;

    -- void all modules
    select min(id) into void_id from DreamsApp_clientdrugusedata where client_id=clientID;
    UPDATE DreamsApp_clientdrugusedata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clienteducationandemploymentdata where client_id=clientID;
    UPDATE DreamsApp_clienteducationandemploymentdata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clientgenderbasedviolencedata where client_id=clientID;
    UPDATE DreamsApp_clientgenderbasedviolencedata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clienthivtestingdata where client_id=clientID;
    UPDATE DreamsApp_clienthivtestingdata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clientindividualandhouseholddata where client_id=clientID;
    UPDATE DreamsApp_clientindividualandhouseholddata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clientparticipationindreams where client_id=clientID;
    UPDATE DreamsApp_clientparticipationindreams set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clientreproductivehealthdata where client_id=clientID;
    UPDATE DreamsApp_clientreproductivehealthdata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clientsexualactivitydata where client_id=clientID;
    UPDATE DreamsApp_clientsexualactivitydata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);


  COMMIT;
  UPDATE duplicate_client_id_in_enrollment_modules SET status=exec_status WHERE client_id = clientID;


END
$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_void_records$$
CREATE PROCEDURE sp_void_records()
BEGIN

  DECLARE no_more_rows BOOLEAN;
  DECLARE clientID INT(11);
  DECLARE v_row_count INT(11);

  DECLARE erroneous_records CURSOR FOR
    SELECT client_id FROM duplicate_client_id_in_enrollment_modules WHERE status=0;

  DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET no_more_rows = TRUE;


  OPEN erroneous_records;
  SET v_row_count = FOUND_ROWS();
  SELECT v_row_count as 'found rows';
  IF v_row_count > 0 THEN
    client_ids: LOOP
      FETCH erroneous_records INTO clientID;

      IF no_more_rows THEN
        CLOSE erroneous_records;
        LEAVE client_ids;
      END IF;
      CALL sp_void_individual_records_using_client_id(clientID, "Duplicate Enrollment data");

    END LOOP client_ids;
  ELSE
    SELECT "NO ROWS WERE FOUND";
  END IF;

END
$$
DELIMITER ;

-- Voiding records with dreams id provided
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_void_individual_records_using_dreams_id$$
CREATE PROCEDURE sp_void_individual_records_using_dreams_id(IN clientID INT(11), IN reason_voided_param VARCHAR(100))
BEGIN

  DECLARE occurence INT(11);
  DECLARE exec_status INT(11) DEFAULT 1;
  DECLARE void_id INT(11);

  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
      SET exec_status = -1;
      ROLLBACK;
    END;
  -- perform all procedure calls within a transaction
  START TRANSACTION;

    -- void all modules
    select min(id) into void_id from DreamsApp_clientdrugusedata where client_id=clientID;
    UPDATE DreamsApp_clientdrugusedata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clienteducationandemploymentdata where client_id=clientID;
    UPDATE DreamsApp_clienteducationandemploymentdata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clientgenderbasedviolencedata where client_id=clientID;
    UPDATE DreamsApp_clientgenderbasedviolencedata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clienthivtestingdata where client_id=clientID;
    UPDATE DreamsApp_clienthivtestingdata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clientindividualandhouseholddata where client_id=clientID;
    UPDATE DreamsApp_clientindividualandhouseholddata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clientparticipationindreams where client_id=clientID;
    UPDATE DreamsApp_clientparticipationindreams set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clientreproductivehealthdata where client_id=clientID;
    UPDATE DreamsApp_clientreproductivehealthdata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);

    select min(id) into void_id from DreamsApp_clientsexualactivitydata where client_id=clientID;
    UPDATE DreamsApp_clientsexualactivitydata set date_voided=NOW(), date_changed=NOW(), reason_voided=reason_voided_param, voided=1, voided_by_id=1 where client_id=clientID AND id NOT IN(void_id);


  COMMIT;
  UPDATE duplicate_client_id_in_enrollment_modules SET status=exec_status WHERE client_id = clientID;


END
$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_void_records$$
CREATE PROCEDURE sp_void_records()
BEGIN

  DECLARE no_more_rows BOOLEAN;
  DECLARE clientID INT(11);
  DECLARE v_row_count INT(11);

  DECLARE erroneous_records CURSOR FOR
    SELECT client_id FROM duplicate_client_id_in_enrollment_modules WHERE status=0;

  DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET no_more_rows = TRUE;


  OPEN erroneous_records;
  SET v_row_count = FOUND_ROWS();
  SELECT v_row_count as 'found rows';
  IF v_row_count > 0 THEN
    client_ids: LOOP
      FETCH erroneous_records INTO clientID;

      IF no_more_rows THEN
        CLOSE erroneous_records;
        LEAVE client_ids;
      END IF;
      CALL sp_void_individual_records_using_client_id(clientID, "Duplicate Enrollment data");

    END LOOP client_ids;
  ELSE
    SELECT "NO ROWS WERE FOUND";
  END IF;

END
$$
DELIMITER ;

-- creating table to hold dreams ids to be deleted
CREATE TABLE duplicate_dreams_id_corrections (
  id INT(11) AUTO_INCREMENT PRIMARY KEY ,
  dreams_id VARCHAR(50),
  action VARCHAR(50),
  implementing_partner INT(11),
  dreams_id_count INT(11) DEFAULT 0,
  client_id_count INT(11) DEFAULT 0,
  status INT(11) DEFAULT 0,
  INDEX(dreams_id),
  INDEX(action)
);

ALTER TABLE duplicate_dreams_id_corrections
    ADD COLUMN client_id INT(11) AFTER dreams_id,
    ADD COLUMN client_dreams_id_match INT(11) DEFAULT 0 AFTER client_id
;

ALTER TABLE duplicate_dreams_id_corrections
    ADD COLUMN new_dreams_id VARCHAR(50)
;
-- Populate duplicate_dreams_id_corrections table

INSERT INTO duplicate_dreams_id_corrections (dreams_id, action) VALUES
  ();

-- Voiding records of provided DREAMS ID and DREAMS ID not shared
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_dreams_id_corrections$$
CREATE PROCEDURE sp_dreams_id_corrections(IN correction VARCHAR(50))
BEGIN

  DECLARE no_more_rows BOOLEAN;
  DECLARE dreamsID VARCHAR(50);
  DECLARE v_row_count INT(11);

  DECLARE erroneous_records CURSOR FOR
    SELECT dreams_id FROM duplicate_dreams_id_corrections WHERE action=correction and status=0;

  DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET no_more_rows = TRUE;


  OPEN erroneous_records;
  SET v_row_count = FOUND_ROWS();
  SELECT v_row_count as 'found rows';
  IF v_row_count > 0 THEN
    client_ids: LOOP
      FETCH erroneous_records INTO dreamsID;

      IF no_more_rows THEN
        CLOSE erroneous_records;
        LEAVE client_ids;
      END IF;
      CALL sp_correct_dreams_id(dreamsID);

    END LOOP client_ids;
  ELSE
    SELECT "NO ROWS WERE FOUND";
  END IF;

END
$$
DELIMITER ;

-- Delete/void non-shared dreams id
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_correct_dreams_id$$
CREATE PROCEDURE sp_correct_dreams_id(IN dreamsID VARCHAR(50))
BEGIN

  DECLARE dreams_id_occurence INT(11);
  DECLARE client_id_occurence INT(11);
  DECLARE var_client_id INT(11);
  DECLARE exec_status INT(11) DEFAULT 1;

  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
      SET exec_status = -1;
      ROLLBACK;
    END;
  -- perform all procedure calls within a transaction
  START TRANSACTION;


  SELECT COUNT(dreams_id) from DreamsApp_client where dreams_id = dreamsID INTO dreams_id_occurence;
  SELECT COUNT(id) from DreamsApp_client where dreams_id = dreamsID INTO client_id_occurence;

  UPDATE duplicate_dreams_id_corrections SET client_id_count=client_id_occurence, dreams_id_count=dreams_id_occurence WHERE dreams_id = dreamsID;
  IF dreams_id_occurence > 1 THEN
    SET exec_status = 3;
  ELSEIF dreams_id_occurence = 0 THEN
    SET exec_status = 2;
  ELSEIF dreams_id_occurence = 1 THEN
    SELECT id from DreamsApp_client where dreams_id = dreamsID INTO var_client_id;
    -- void all modules
    UPDATE DreamsApp_clientdrugusedata set date_voided=NOW(), date_changed=NOW(), reason_voided="Duplicate Client", voided=1, voided_by_id=1 where client_id=var_client_id;
    UPDATE DreamsApp_clienteducationandemploymentdata set date_voided=NOW(), date_changed=NOW(), reason_voided="Duplicate Client", voided=1, voided_by_id=1 where client_id=var_client_id;
    UPDATE DreamsApp_clientgenderbasedviolencedata set date_voided=NOW(), date_changed=NOW(), reason_voided="Duplicate Client", voided=1, voided_by_id=1 where client_id=var_client_id;
    UPDATE DreamsApp_clienthivtestingdata set date_voided=NOW(), date_changed=NOW(), reason_voided="Duplicate Client", voided=1, voided_by_id=1 where client_id=var_client_id;
    UPDATE DreamsApp_clientindividualandhouseholddata set date_voided=NOW(), date_changed=NOW(), reason_voided="Duplicate Client", voided=1, voided_by_id=1 where client_id=var_client_id;
    UPDATE DreamsApp_clientparticipationindreams set date_voided=NOW(), date_changed=NOW(), reason_voided="Duplicate Client", voided=1, voided_by_id=1 where client_id=var_client_id;
    UPDATE DreamsApp_clientreproductivehealthdata set date_voided=NOW(), date_changed=NOW(), reason_voided="Duplicate Client", voided=1, voided_by_id=1 where client_id=var_client_id;
    UPDATE DreamsApp_clientsexualactivitydata set date_voided=NOW(), date_changed=NOW(), reason_voided="Duplicate Client", voided=1, voided_by_id=1 where client_id=var_client_id;
    UPDATE DreamsApp_intervention set date_voided=NOW(), date_changed=NOW(), reason_voided="Duplicate Client", voided=1, voided_by_id=1 where client_id=var_client_id;
    UPDATE DreamsApp_client set date_voided=NOW(), date_changed=NOW(), reason_voided="Duplicate Client", voided=1, voided_by_id=1 where id=var_client_id;

  END IF;

  COMMIT;

  UPDATE duplicate_dreams_id_corrections SET status=exec_status WHERE dreams_id = dreamsID;

END
$$
DELIMITER ;



-- -------------------------------------------- DELETE/RETAIN/REASSIGN DREAMS ID Based on IP actions ---------------------------------

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_reassign_or_delete_shared_dreams_id$$
CREATE PROCEDURE sp_reassign_or_delete_shared_dreams_id()
BEGIN

  DECLARE no_more_rows BOOLEAN;
  DECLARE dreamsID VARCHAR(50);
  DECLARE clientID INT(11);
  DECLARE cleanupAction VARCHAR(50);
  DECLARE v_row_count INT(11);

  DECLARE erroneous_records CURSOR FOR
    SELECT dreams_id, client_id, action FROM duplicate_dreams_id_corrections WHERE action IN ("DELETE", "REASSIGN") AND status=0;

  DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET no_more_rows = TRUE;


  OPEN erroneous_records;
  SET v_row_count = FOUND_ROWS();
  SELECT v_row_count as 'found rows';
  IF v_row_count > 0 THEN
    client_ids: LOOP
      FETCH erroneous_records INTO dreamsID, clientID, cleanupAction;

      IF no_more_rows THEN
        CLOSE erroneous_records;
        LEAVE client_ids;
      END IF;

      IF cleanupAction="DELETE" THEN
        CALL sp_delete_dreams_id(dreamsID, clientID);
      ELSEIF cleanupAction="REASSIGN" THEN
        CALL sp_reassign_dreams_id(dreamsID, clientID);
      END IF;

    END LOOP client_ids;
  ELSE
    SELECT "NO ROWS WERE FOUND";
  END IF;

END
$$
DELIMITER ;

-- Delete/void using client_id and dreams id
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_delete_dreams_id$$
CREATE PROCEDURE sp_delete_dreams_id(IN dreamsID VARCHAR(50), clientID INT(11))
BEGIN

  DECLARE client_id_dreams_id_match INT(11);
  DECLARE exec_status INT(11) DEFAULT 1;

  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
      SET exec_status = -1;
      ROLLBACK;
    END;
  -- perform all procedure calls within a transaction
  START TRANSACTION;


  SELECT IF(dreams_id=dreamsID, 1, 0) from DreamsApp_client where id = clientID INTO client_id_dreams_id_match; -- 1 if same, 0 if not same

  UPDATE duplicate_dreams_id_corrections SET client_dreams_id_match=client_id_dreams_id_match WHERE client_id = clientID;

  IF client_id_dreams_id_match = 0 THEN
    SET exec_status = 4; -- no matching client dreams id
  ELSEIF client_id_dreams_id_match = 1 THEN
    -- void all modules
    UPDATE DreamsApp_clientdrugusedata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clienteducationandemploymentdata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientgenderbasedviolencedata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clienthivtestingdata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientindividualandhouseholddata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientparticipationindreams set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientreproductivehealthdata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientsexualactivitydata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_intervention set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_client set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where id=clientID;

  END IF;

  COMMIT;

  UPDATE duplicate_dreams_id_corrections SET status=exec_status WHERE client_id = clientID;

END
$$
DELIMITER ;

-- Delete/void using client_id and dreams id
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_reassign_dreams_id$$
CREATE PROCEDURE sp_reassign_dreams_id(IN dreamsID VARCHAR(50), clientID INT(11))
BEGIN

  DECLARE client_id_dreams_id_match INT(11);
  DECLARE exec_status INT(11) DEFAULT 1;
  DECLARE ip_code INT(11);
  DECLARE ward_code INT(11);
  DECLARE newDreamsID VARCHAR(50);

  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
      SET exec_status = -1;
      ROLLBACK;
    END;
  -- perform all procedure calls within a transaction
  START TRANSACTION;

  SELECT IF(dreams_id=dreamsID, 1, 0) from DreamsApp_client where id = clientID INTO client_id_dreams_id_match; -- 1 if same, 0 if not same

  UPDATE duplicate_dreams_id_corrections SET client_dreams_id_match=client_id_dreams_id_match WHERE client_id = clientID;

  IF client_id_dreams_id_match = 0 THEN
    SET exec_status = 4; -- no matching client dreams id
  ELSEIF client_id_dreams_id_match = 1 THEN

    -- GET IP AND WARD CODES
    SELECT implementing_partner_id, ward_id INTO ip_code, ward_code from DreamsApp_client where id = clientID;
    SELECT nextDreamsSerial(ip_code, ward_code) INTO newDreamsID;
    -- Update client module to reflect the new dreams id

    UPDATE DreamsApp_client set dreams_id=newDreamsID, date_changed=NOW() where id=clientID;
    UPDATE duplicate_dreams_id_corrections SET new_dreams_id=newDreamsID WHERE client_id = clientID;

  END IF;

  COMMIT;

  UPDATE duplicate_dreams_id_corrections SET status=exec_status WHERE client_id = clientID;

END
$$
DELIMITER ;

-- voiding services

DELIMITER $$
DROP PROCEDURE IF EXISTS void_services$$
CREATE PROCEDURE sp_delete_dreams_id(IN dreamsID VARCHAR(50), clientID INT(11))
BEGIN

  DECLARE client_id_dreams_id_match INT(11);
  DECLARE exec_status INT(11) DEFAULT 1;

  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
      SET exec_status = -1;
      ROLLBACK;
    END;
  -- perform all procedure calls within a transaction
  START TRANSACTION;


  SELECT IF(dreams_id=dreamsID, 1, 0) from DreamsApp_client where id = clientID INTO client_id_dreams_id_match; -- 1 if same, 0 if not same

  UPDATE duplicate_dreams_id_corrections SET client_dreams_id_match=client_id_dreams_id_match WHERE client_id = clientID;

  IF client_id_dreams_id_match = 0 THEN
    SET exec_status = 4; -- no matching client dreams id
  ELSEIF client_id_dreams_id_match = 1 THEN
    -- void all modules
    UPDATE DreamsApp_clientdrugusedata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clienteducationandemploymentdata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientgenderbasedviolencedata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clienthivtestingdata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientindividualandhouseholddata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientparticipationindreams set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientreproductivehealthdata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_clientsexualactivitydata set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;
    UPDATE DreamsApp_intervention set date_voided=NOW(), date_changed=NOW(), reason_voided="Marked for deletion by IP", voided=1, voided_by_id=1 where client_id=clientID;

  END IF;

  COMMIT;

  UPDATE duplicate_dreams_id_corrections SET status=exec_status WHERE client_id = clientID;

END
$$
DELIMITER ;


-- zero services

select x.dreams_id, i.client_id, x.first_name, x.middle_name, x.last_name, x.implementing_partner, x.county_of_residence, x.sub_county, x.ward, x.date_of_enrollment_quarter
from stag_client_ex x
left outer join DreamsApp_intervention i on x.id=i.client_id
where x.implementing_partner_id=6 and x.exited=0 and x.voided != 1
having i.client_id is null;


-- create staging table for individual_client_service_layering : stag_individual_client_service_layering
drop table if EXISTS  stag_individual_client_service_layering;
create table stag_individual_client_service_layering AS
select
x.dreams_id,
i.client_id,
x.first_name,
x.middle_name,
x.last_name,
x.date_of_birth,
x.date_of_enrollment,
x.age_at_enrollment,
timestampdiff(YEAR,x.`date_of_birth`,CURDATE()) as current_age,
x.implementing_partner,
x.implementing_partner_id,
x.county_of_residence,
x.county_of_residence_id,
x.sub_county,
x.sub_county_id,
x.ward,
x.ward_id,
x.village,
IF(x.exited=1, "Yes", "") as exited_from_program,
x.date_exited as date_exited,
sum(if(intervention_type_id=1, 1, 0)) as shuga_II,
sum(if(intervention_type_id=2, 1, 0)) as respect_k,
sum(if(intervention_type_id=3, 1, 0)) as hcbf,
sum(if(intervention_type_id=4, 1, 0)) as mhmc,
sum(if(intervention_type_id=5, 1, 0)) as sister_to_sister_k,
sum(if(intervention_type_id=6, 1, 0)) as mlrc,
sum(if(intervention_type_id=7, 1, 0)) as behavioral_other,
sum(if(intervention_type_id=8, 1, 0)) as hts_client,
sum(if(intervention_type_id=9, 1, 0)) as hts_partner,
sum(if(intervention_type_id=10, 1, 0)) as linkage_to_ccc,
sum(if(intervention_type_id=11, 1, 0)) as pregnancy_test,
sum(if(intervention_type_id=12, 1, 0)) as anc_pmtct,
sum(if(intervention_type_id=13, 1, 0)) as sti_screening,
sum(if(intervention_type_id=14, 1, 0)) as sti_treatment,
sum(if(intervention_type_id=15, 1, 0)) as sti_linkage,
sum(if(intervention_type_id=16, 1, 0)) as tb_screening,
sum(if(intervention_type_id=17, 1, 0)) as linked_for_tb_treatment,
sum(if(intervention_type_id=18, 1, 0)) as condom_education_and_demo,
sum(if(intervention_type_id=19, 1, 0)) as condom_provided,
sum(if(intervention_type_id=20, 1, 0)) as partner_vmmc,
sum(if(intervention_type_id=21, 1, 0)) as contraception_education,
sum(if(intervention_type_id=22, 1, 0)) as contraception_ind_counseling,
sum(if(intervention_type_id=23, 1, 0)) as contraception_pills_oral,
sum(if(intervention_type_id=24, 1, 0)) as contraception_injectable,
sum(if(intervention_type_id=25, 1, 0)) as contraception_implant,
sum(if(intervention_type_id=26, 1, 0)) as contraception_iud_coil,
sum(if(intervention_type_id=27, 1, 0)) as prep,
sum(if(intervention_type_id=28, 1, 0)) as sexual_violence_pep,
sum(if(intervention_type_id=29, 1, 0)) as sexual_violence_pss,
sum(if(intervention_type_id=30, 1, 0)) as sexual_violence_rescue_shelter,
sum(if(intervention_type_id=31, 1, 0)) as sexual_violence_police,
sum(if(intervention_type_id=32, 1, 0)) as sexual_violence_trauma_counseling,
sum(if(intervention_type_id=33, 1, 0)) as sexual_violence_emergency_contraception,
sum(if(intervention_type_id=34, 1, 0)) as sexual_violence_exam_treatment,
sum(if(intervention_type_id=35, 1, 0)) as education_school_fees,
sum(if(intervention_type_id=36, 1, 0)) as education_stationery,
sum(if(intervention_type_id=37, 1, 0)) as education_uniform,
sum(if(intervention_type_id=38, 1, 0)) as education_other_support,
sum(if(intervention_type_id=39, 1, 0)) as parent_program_fmp,
sum(if(intervention_type_id=40, 1, 0)) as economic_strengthening_fc_training,
sum(if(intervention_type_id=41, 1, 0)) as economic_strengthening_voc_training,
sum(if(intervention_type_id=42, 1, 0)) as economic_strengthening_microfinance,
sum(if(intervention_type_id=43, 1, 0)) as economic_strengthening_internship,
sum(if(intervention_type_id=44, 1, 0)) as economic_strengthening_startups,
sum(if(intervention_type_id=45, 1, 0)) as cash_transfer,
sum(if(intervention_type_id=46, 1, 0)) as ovc_for_children_sibling_other,
sum(if(intervention_type_id=47, 1, 0)) as nutritional_support,
sum(if(intervention_type_id=48, 1, 0)) as drug_addiction_counseling,
sum(if(intervention_type_id=49, 1, 0)) as sab,
sum(if(intervention_type_id=50, 1, 0)) as hts_client_linked_to_hts,
sum(if(intervention_type_id=51, 1, 0)) as pregnancy_test_confirmed_linkage,
sum(if(intervention_type_id=52, 1, 0)) as hts_partner_linked_to_hts,
sum(if(intervention_type_id=53, 1, 0)) as positive_partner_linked_to_ccc,
sum(if(intervention_type_id=54, 1, 0)) as tube_ligation,
sum(if(intervention_type_id=55, 1, 0)) as sexual_violence_legal_support,
sum(if(intervention_type_id=56, 1, 0)) as economic_strengthening_employment,
sum(if(intervention_type_id=57, 1, 0)) as economic_strengthening_entrep_training,
sum(if(intervention_type_id=58, 1, 0)) as economic_strengthening_entrep_support,
sum(if(intervention_type_id=59, 1, 0)) as sexual_violence_other,
sum(if(intervention_type_id=60, 1, 0)) as physical_violence_pss,
sum(if(intervention_type_id=61, 1, 0)) as physical_violence_rescue_shelter,
sum(if(intervention_type_id=62, 1, 0)) as physical_violence_police,
sum(if(intervention_type_id=63, 1, 0)) as physical_violence_trauma_counseling,
sum(if(intervention_type_id=64, 1, 0)) as physical_violence_exam_treatment,
sum(if(intervention_type_id=65, 1, 0)) as physical_violence_legal_support,
sum(if(intervention_type_id=66, 1, 0)) as physical_violence_other,
sum(if(intervention_type_id=67, 1, 0)) as bio_medical_other,
sum(if(intervention_type_id=68, 1, 0)) as social_protection_other,
sum(if(intervention_type_id=69, 1, 0)) as parent_program_fmp_2

from stag_client_ex x
left outer join stag_client_intervention i on x.id=i.client_id
where (i.voided = 0 or isnull(i.voided)) and
      (x.voided = 0 or isnull(x.voided)) and (x.dreams_id is not null and x.dreams_id != '')
group by x.dreams_id;




select id, client_id, voided, reason_voided, date_voided, date_changed  from DreamsApp_clientdrugusedata where client_id=31927;
select id, client_id,voided, reason_voided, date_voided, date_changed  from DreamsApp_clienteducationandemploymentdata where client_id=31927;
select id, client_id,voided, reason_voided, date_voided, date_changed  from DreamsApp_clientgenderbasedviolencedata where client_id=31927;
select id, client_id,voided, reason_voided, date_voided, date_changed  from DreamsApp_clienthivtestingdata where client_id=31927;
select id, client_id,voided, reason_voided, date_voided, date_changed  from DreamsApp_clientindividualandhouseholddata where client_id=31927;
select id, client_id,voided, reason_voided, date_voided, date_changed  from DreamsApp_clientparticipationindreams where client_id=31927;
select id, client_id,voided, reason_voided, date_voided, date_changed  from DreamsApp_clientreproductivehealthdata where client_id=31927;
select id, client_id,voided, reason_voided, date_voided, date_changed  from DreamsApp_clientsexualactivitydata where client_id=31927;
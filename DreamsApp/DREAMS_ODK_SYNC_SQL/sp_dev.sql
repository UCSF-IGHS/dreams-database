
-- setup first time setup tables

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_dreamsTablesSetup$$
CREATE PROCEDURE sp_dreamsTablesSetup()
BEGIN

-- defining table to be populated by odk enrollment trigger
DROP TABLE IF EXISTS dreams_dev.odk_dreams_sync;
CREATE TABLE dreams_dev.odk_dreams_sync (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(100) NOT NULL DEFAULT '',
  `synced` int(11) NOT NULL DEFAULT '0',
  `form` varchar(100) NOT NULL DEFAULT '',
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);


-- defining table for sync log
DROP TABLE IF EXISTS dreams_dev.odk_dreams_sync_log;
CREATE TABLE dreams_dev.odk_dreams_sync_log (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` varchar(100) NOT NULL DEFAULT 'Scheduled Update',
  `last_update` DATETIME,
  PRIMARY KEY (`id`)
);

-- create flat table for reporting

DROP TABLE IF EXISTS dreams_dev.flat_dreams_enrollment;

CREATE TABLE dreams_dev.flat_dreams_enrollment (
client_id INT(11) PRIMARY KEY NOT NULL,
first_name VARCHAR(100),
middle_name VARCHAR(100),
last_name VARCHAR(100),
date_of_birth DATE,
verification_document_id INT(11),
verification_doc_no VARCHAR(50),
date_of_enrollment DATE,
phone_number VARCHAR(15),
dss_id_number VARCHAR(20),
informal_settlement VARCHAR(50),
village VARCHAR(50),
landmark VARCHAR(255),
dreams_id VARCHAR(20),
guardian_name VARCHAR(50),
relationship_with_guardian VARCHAR(50),
guardian_phone_number VARCHAR(15),
guardian_national_id VARCHAR(20),
date_created DATE,
county_of_residence_id INT(11),
implementing_partner_id INT(11),
marital_status_id INT(11),
sub_county_id INT(11),
ward_id INT(11),
ward_name VARCHAR(50),
sub_county_code INT(11),
sub_county_name VARCHAR(100),
county_code INT(11),
county_name VARCHAR(30),
head_of_household_id INT(11),
head_of_household_other VARCHAR(50),
age_of_household_head INT(11),
is_father_alive INT(11),
is_mother_alive INT(11),
is_parent_chronically_ill INT(11),
main_floor_material_id INT(11),
main_floor_material_other VARCHAR(50),
main_roof_material_id INT(11),
main_roof_material_other VARCHAR(50),
main_wall_material_id INT(11),
main_wall_material_other VARCHAR(50),
source_of_drinking_water_id INT(11),
source_of_drinking_water_other VARCHAR(50),
no_of_adults INT(11),
no_of_females INT(11),
no_of_males INT(11),
no_of_children INT(11),
currently_in_ct_program_id INT(11),
current_ct_program VARCHAR(50),
ever_enrolled_in_ct_program_id INT(11),
ever_missed_full_day_food_in_4wks_id INT(11),
has_disability_id INT(11),
no_of_days_missed_food_in_4wks_id INT(11),
disability_types VARCHAR(20),
no_of_people_in_household INT(11),
age_at_first_sexual_encounter INT(11),
sex_partners_in_last_12months INT(11),
age_of_last_partner_id INT(11),
age_of_second_last_partner_id INT(11),
age_of_third_last_partner_id INT(11),
ever_had_sex_id INT(11),
has_sexual_partner_id INT(11),
know_last_partner_hiv_status_id INT(11),
know_second_last_partner_hiv_status_id INT(11),
know_third_last_partner_hiv_status_id INT(11),
last_partner_circumcised_id INT(11),
received_money_gift_for_sex_id INT(11),
second_last_partner_circumcised_id INT(11),
third_last_partner_circumcised_id INT(11),
used_condom_with_last_partner_id INT(11),
used_condom_with_second_last_partner_id INT(11),
used_condom_with_third_last_partner_id INT(11),
no_of_biological_children INT(11),
anc_facility_name VARCHAR(50),
known_fp_method_other VARCHAR(50),
current_fp_method_other VARCHAR(50),
reason_not_using_fp_other VARCHAR(50),
current_anc_enrollment_id INT(11),
current_fp_method_id INT(11),
currently_pregnant_id INT(11),
currently_use_modern_fp_id INT(11),
fp_methods_awareness_id INT(11),
has_biological_children_id INT(11),
reason_not_using_fp_id INT(11),
known_fp_methods VARCHAR(20),
drug_abuse_last_12months_other VARCHAR(50),
drug_used_last_12months_other VARCHAR(50),
drug_abuse_last_12months_id INT(11),
frequency_of_alcohol_last_12months_id INT(11),
produced_alcohol_last_12months_id INT(11),
used_alcohol_last_12months_id INT(11),
drugs_used_in_last_12_months VARCHAR(20),
dreams_program_other VARCHAR(50),
programmes_enrolled VARCHAR(20),
gbv_help_provider_other VARCHAR(50),
preferred_gbv_help_provider_other VARCHAR(50),
economic_threat_ever_id INT(11),
economic_threat_last_3months_id INT(11),
humiliated_ever_id INT(11),
humiliated_last_3months_id INT(11),
insulted_ever_id INT(11),
insulted_last_3months_id INT(11),
knowledge_of_gbv_help_centres_id INT(11),
physical_violence_ever_id INT(11),
physical_violence_last_3months_id INT(11),
physically_forced_other_sex_acts_ever_id INT(11),
physically_forced_other_sex_acts_last_3months_id INT(11),
physically_forced_sex_ever_id INT(11),
physically_forced_sex_last_3months_id INT(11),
seek_help_after_gbv_id INT(11),
threatened_for_sexual_acts_ever_id INT(11),
threatened_for_sexual_acts_last_3months_id INT(11),
threats_to_hurt_ever_id INT(11),
threats_to_hurt_last_3months_id INT(11),
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
current_income_source_id INT(11),
current_school_level_id INT(11),
current_school_type_id INT(11),
currently_in_school_id INT(11),
dropout_school_level_id INT(11),
has_savings_id INT(11),
last_time_in_school_id INT(11),
life_wish_id INT(11),
reason_not_in_school_id INT(11),
current_edu_supporter_list VARCHAR(20),
care_facility_enrolled VARCHAR(50),
reason_not_in_hiv_care_other VARCHAR(50),
reason_never_tested_for_hiv_other VARCHAR(50),
enrolled_in_hiv_care_id INT(11),
ever_tested_for_hiv_id INT(11),
knowledge_of_hiv_test_centres_id INT(11),
last_test_result_id INT(11),
period_last_tested_id INT(11),
reason_not_in_hiv_care_id INT(11),
reason_not_tested_for_hiv VARCHAR(20)
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

END;
$$
DELIMITER ;

-- -----------------------------------------       event definition  ------------------------------------------------------
DELIMITER $$
DROP EVENT IF EXISTS event_odk_dreams_enrollment_sync$$
CREATE EVENT event_odk_dreams_enrollment_sync
ON SCHEDULE EVERY 2 MINUTE STARTS CURRENT_TIMESTAMP
DO
BEGIN
CALL sp_sync_odk_dreams_data();
CALL sp_update_demographics_location();
CALL sp_update_flat_enrollment_table();
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
from DreamsApp_client WHERE dreams_id is not null AND DreamsApp_client.implementing_partner_id=implementing_partner_id group by implementing_partner_id;

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

    INSERT INTO dreams_dev.DreamsApp_client
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
      verification_document_id,
      verification_doc_no,
      implementing_partner_id,
      ward_id,
      odk_enrollment_uuid,
      date_created
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
      COALESCE(d.DEMOGRAPHIC_DREAMSID, nextDreamsSerial(d.IPNAME, d.DEMOGRAPHIC_WARD)) as Dreams_id,
      d.DEMOGRAPHIC_CAREGIVER AS caregiver_name,
      d.DEMOGRAPHIC_RELATIONSHIP as caregiver_relationship,
      d.DEMOGRAPHIC_PHONENUMBER as caregiver_phone_no,
      d.DEMOGRAPHIC_NATIONAL_ID as caregiver_ID_no,
      d.DEMOGRAPHIC_INFORMALSTTLEMENTT as informal_settlement,
      d.DEMOGRAPHIC_LANDMARK as landmark,
      d.VERIFICATIONDOC as verification_doc,
      COALESCE(d.VERIFICATION_1, d.VERIFICATION_2, d.VERIFICATION_3, d.VERIFICATIONDOCSPECIFY) as verification_doc_no,
      d.IPNAME as ip_name,
      d.DEMOGRAPHIC_WARD,
      d._URI as uuid,
      now()
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

    INSERT INTO dreams_dev.DreamsApp_clientindividualandhouseholddata
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
    INSERT INTO dreams_dev.DreamsApp_clientindividualandhouseholddata_disability_type (clientindividualandhouseholddata_id, disabilitytype_id)
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
    INSERT INTO dreams_dev.DreamsApp_clientsexualactivitydata
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

    INSERT INTO dreams_dev.DreamsApp_clientreproductivehealthdata
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
    INSERT INTO dreams_dev.DreamsApp_clientreproductivehealthdata_known_fp_method (clientreproductivehealthdata_id, familyplanningmethod_id)
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

    INSERT INTO dreams_dev.DreamsApp_clientdrugusedata
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
    INSERT INTO dreams_dev.DreamsApp_clientdrugusedata_drug_used_last_12months (clientdrugusedata_id, drug_id)
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

    INSERT INTO dreams_dev.DreamsApp_clientparticipationindreams
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
    INSERT INTO dreams_dev.DreamsApp_clientparticipationindreams_dreams_program (clientparticipationindreams_id, dreamsprogramme_id)
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

    INSERT INTO dreams_dev.DreamsApp_clientgenderbasedviolencedata
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
    INSERT INTO dreams_dev.DreamsApp_clientgenderbasedviolencedata_gbv_help_provider (clientgenderbasedviolencedata_id, gbvhelpprovider_id)
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
    INSERT INTO dreams_dev.DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_p1bce (clientgenderbasedviolencedata_id, gbvhelpprovider_id)
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

    INSERT INTO dreams_dev.DreamsApp_clienteducationandemploymentdata
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
    INSERT INTO dreams_dev.DreamsApp_clienteducationandemploymentdata_current_educationebf4 (clienteducationandemploymentdata_id, educationsupporter_id)
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

    INSERT INTO dreams_dev.DreamsApp_clienthivtestingdata
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
    INSERT INTO dreams_dev.DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv (clienthivtestingdata_id, reasonnottestedforhiv_id)
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

-- get reason one has never tested for hiv: django many to many relationship

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_ct_source_of_livelihood$$
CREATE PROCEDURE sp_ct_source_of_livelihood(IN recordID INT(11), IN parentUUID VARCHAR(100))
  BEGIN
    INSERT INTO dreams_dev.DreamsApp_homevisitverification_source_of_livelihood (homevisitverification_id, sourceofincome_id)
    SELECT recordID, c.VALUE
    FROM odk_aggregate.CT_HOME_VISIT_VERFICATION_FORM_Q3 c
    WHERE c._PARENT_AURI=parentUUID;

  END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_demographics_location$$
CREATE PROCEDURE sp_update_demographics_location()
  BEGIN
    UPDATE dreams_dev.DreamsApp_client cl
    INNER JOIN (
      SELECT
      w.code ward_code,
      sc.id subcounty_id,
      c.id county_id
    from dreams_dev.DreamsApp_ward w
    INNER JOIN dreams_dev.DreamsApp_subcounty sc ON sc.id = w.sub_county_id
    INNER JOIN dreams_dev.DreamsApp_county c ON c.id=sc.county_id
    ) location ON location.ward_code = cl.ward_id
    SET cl.sub_county_id = location.subcounty_id, cl.county_of_residence_id = location.county_id
    WHERE (cl.sub_county_id is NULL OR cl.county_of_residence_id is NULL)

;
  END $$
DELIMITER ;


-- ------------------------------------- insert into flat table ---------

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_populate_flat_enrollment_table$$
CREATE PROCEDURE sp_populate_flat_enrollment_table()
BEGIN

DECLARE record_id INT(11);
INSERT INTO dreams_dev.DreamsApp_flatenrollmenttablelog(date_started, activity) VALUES(NOW(), 'First time population of table');
SET record_id = LAST_INSERT_ID();

INSERT INTO dreams_dev.flat_dreams_enrollment(
client_id,
first_name,
middle_name,
last_name,
date_of_birth,
verification_document_id,
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
reason_not_in_hiv_care_id
)
select
d.id,
d.first_name,
d.middle_name,
d.last_name,
d.date_of_birth,
d.verification_document_id,
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
hiv.reason_not_in_hiv_care_id
from
dreams_dev.DreamsApp_client AS d
LEFT OUTER JOIN dreams_dev.DreamsApp_clientindividualandhouseholddata i on i.client_id=d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clientsexualactivitydata s ON s.client_id = d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clientreproductivehealthdata rh ON rh.client_id=d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clientdrugusedata dr on dr.client_id=d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clientparticipationindreams p on p.client_id=d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clientgenderbasedviolencedata gbv ON gbv.client_id=d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clienteducationandemploymentdata edu ON edu.client_id = d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clienthivtestingdata hiv ON hiv.client_id=d.id
LEFT OUTER JOIN (
SELECT
w.id as ward_code,
w.name as ward_name,
w.sub_county_id as sub_county_code,
s.name as sub_county_name,
s.county_id as county_code,
c.name as county_name
from dreams_dev.DreamsApp_ward w
INNER JOIN dreams_dev.DreamsApp_subcounty s ON s.id = w.sub_county_id
INNER JOIN dreams_dev.DreamsApp_county c ON s.county_id = c.id
) l ON l.ward_code = d.ward_id
group by d.id
;

-- update many to many fields
UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      i_data.client_id,
      group_concat(disabilitytype_id) AS disability_types
      from dreams_dev.DreamsApp_clientindividualandhouseholddata i_data
      INNER JOIN dreams_dev.DreamsApp_clientindividualandhouseholddata_disability_type dt ON dt.clientindividualandhouseholddata_id = i_data.id
      GROUP BY i_data.client_id
  ) ind_data on ind_data.client_id = e.client_id
SET e.disability_types = ind_data.disability_types;

-- reproductive data: know fp methods

UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      rh.client_id,
      group_concat(familyplanningmethod_id) AS known_fp_methods
      FROM dreams_dev.DreamsApp_clientreproductivehealthdata_known_fp_method fp
      INNER JOIN dreams_dev.DreamsApp_clientreproductivehealthdata rh
      ON fp.clientreproductivehealthdata_id = rh.id
      GROUP BY rh.client_id
  ) rpr_data on rpr_data.client_id = e.client_id
SET e.known_fp_methods = rpr_data.known_fp_methods;

-- drugs used in past one year
UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      dd.client_id,
      group_concat(d.drug_id) AS drugs_used_in_last_12_months
      FROM dreams_dev.DreamsApp_clientdrugusedata_drug_used_last_12months d
      INNER JOIN dreams_dev.DreamsApp_clientdrugusedata dd ON d.clientdrugusedata_id = dd.id
      GROUP BY dd.client_id
  ) d_data on d_data.client_id = e.client_id
SET e.drugs_used_in_last_12_months = d_data.drugs_used_in_last_12_months;

-- dreams programs enrolled

UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      cpd.client_id   AS client_id,
      group_concat(dp.dreamsprogramme_id) AS programmes_enrolled
      FROM dreams_dev.DreamsApp_clientparticipationindreams_dreams_program dp
      INNER JOIN dreams_dev.DreamsApp_clientparticipationindreams cpd
      ON dp.clientparticipationindreams_id = cpd.id
      GROUP BY client_id
  ) p on p.client_id = e.client_id
SET e.programmes_enrolled = p.programmes_enrolled;

-- gbv sought provider
UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      gbv.client_id,
      group_concat(provider.gbvhelpprovider_id) AS provider_list
      FROM dreams_dev.DreamsApp_clientgenderbasedviolencedata_gbv_help_provider provider
      INNER JOIN dreams_dev.DreamsApp_clientgenderbasedviolencedata gbv on gbv.id = provider.clientgenderbasedviolencedata_id
      GROUP BY gbv.client_id
  ) gbv on gbv.client_id = e.client_id
SET e.providers_sought = gbv.provider_list;

-- gbv preferred provider

UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      gbv.client_id,
      group_concat(provider.gbvhelpprovider_id) AS provider_list
      FROM dreams_dev.DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_p1bce provider -- DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_provider
      INNER JOIN dreams_dev.DreamsApp_clientgenderbasedviolencedata gbv on gbv.id = provider.clientgenderbasedviolencedata_id
      GROUP BY gbv.client_id
  ) gbv on gbv.client_id = e.client_id
SET e.preferred_providers = gbv.provider_list;

-- current education supporter

UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      ed.client_id,
      group_concat(educationsupporter_id)   AS current_edu_supporter_list
      FROM dreams_dev.DreamsApp_clienteducationandemploymentdata_current_educationebf4 s -- DreamsApp_clienteducationandemploymentdata_current_education_supporter s
      INNER JOIN dreams_dev.DreamsApp_clienteducationandemploymentdata ed ON ed.id = s.clienteducationandemploymentdata_id
      GROUP BY ed.client_id
  ) ed on ed.client_id = e.client_id
SET e.current_edu_supporter_list = ed.current_edu_supporter_list;

-- reason never tested for hiv

UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      hiv_d.client_id,
      group_concat(rn.reasonnottestedforhiv_id) AS reason_not_tested_for_hiv
      FROM dreams_dev.DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv rn
      INNER JOIN dreams_dev.DreamsApp_clienthivtestingdata hiv_d ON hiv_d.id=rn.clienthivtestingdata_id
      GROUP BY hiv_d.client_id
  ) hiv on hiv.client_id = e.client_id
SET e.reason_not_tested_for_hiv = hiv.reason_not_tested_for_hiv;

UPDATE dreams_dev.DreamsApp_flatenrollmenttablelog SET date_completed = NOW() WHERE id=record_id;

END$$
DELIMITER ;


-- ------------------------------------------- pick changes after initial setup and population      -------------------------------------

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_flat_enrollment_table$$
CREATE PROCEDURE sp_update_flat_enrollment_table()
BEGIN

DECLARE record_id INT(11);
DECLARE last_update_time DATETIME;
SELECT max(date_completed) into last_update_time from dreams_dev.DreamsApp_flatenrollmenttablelog;
INSERT INTO dreams_dev.DreamsApp_flatenrollmenttablelog(date_started, activity) VALUES(NOW(), 'Table Updates');
SET record_id = LAST_INSERT_ID();

INSERT INTO dreams_dev.flat_dreams_enrollment(
client_id,
first_name,
middle_name,
last_name,
date_of_birth,
verification_document_id,
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
reason_not_in_hiv_care_id
)
select
d.id,
d.first_name,
d.middle_name,
d.last_name,
d.date_of_birth,
d.verification_document_id,
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
hiv.reason_not_in_hiv_care_id
from
dreams_dev.DreamsApp_client AS d
LEFT OUTER JOIN dreams_dev.DreamsApp_clientindividualandhouseholddata i on i.client_id=d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clientsexualactivitydata s ON s.client_id = d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clientreproductivehealthdata rh ON rh.client_id=d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clientdrugusedata dr on dr.client_id=d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clientparticipationindreams p on p.client_id=d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clientgenderbasedviolencedata gbv ON gbv.client_id=d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clienteducationandemploymentdata edu ON edu.client_id = d.id
LEFT OUTER JOIN dreams_dev.DreamsApp_clienthivtestingdata hiv ON hiv.client_id=d.id
LEFT OUTER JOIN (
SELECT
w.id as ward_code,
w.name as ward_name,
w.sub_county_id as sub_county_code,
s.name as sub_county_name,
s.county_id as county_code,
c.name as county_name
from dreams_dev.DreamsApp_ward w
INNER JOIN dreams_dev.DreamsApp_subcounty s ON s.id = w.sub_county_id
INNER JOIN dreams_dev.DreamsApp_county c ON s.county_id = c.id
) l ON l.ward_code = d.ward_id
where (d.date_created > last_update_time or d.date_changed > last_update_time)
  or (i.date_created > last_update_time or i.date_changed > last_update_time)
  or (s.date_created > last_update_time or s.date_changed > last_update_time)
  or (rh.date_created > last_update_time or rh.date_changed > last_update_time)
  or (dr.date_created > last_update_time or dr.date_changed > last_update_time)
  or (p.date_created > last_update_time or p.date_changed > last_update_time)
  or (gbv.date_created > last_update_time or gbv.date_changed > last_update_time)
  or (edu.date_created > last_update_time or edu.date_changed > last_update_time)
  or (hiv.date_created > last_update_time or hiv.date_changed > last_update_time)
group by d.id
ON DUPLICATE KEY UPDATE
first_name=VALUES(first_name),
middle_name=VALUES(middle_name),
last_name=VALUES(last_name),
date_of_birth=VALUES(date_of_birth),
verification_document_id=VALUES(verification_document_id),
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
reason_not_in_hiv_care_id=VALUES(reason_not_in_hiv_care_id)

;
-- update many to many fields
UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      i_data.client_id,
      group_concat(disabilitytype_id) AS disability_types
      from dreams_dev.DreamsApp_clientindividualandhouseholddata i_data
      INNER JOIN dreams_dev.DreamsApp_clientindividualandhouseholddata_disability_type dt ON dt.clientindividualandhouseholddata_id = i_data.id
      WHERE  (i_data.date_created > last_update_time or i_data.date_changed > last_update_time)
      GROUP BY i_data.client_id
  ) ind_data on ind_data.client_id = e.client_id
SET e.disability_types = ind_data.disability_types;

-- reproductive data: know fp methods

UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      rh.client_id,
      group_concat(familyplanningmethod_id) AS known_fp_methods
      FROM dreams_dev.DreamsApp_clientreproductivehealthdata_known_fp_method fp
      INNER JOIN dreams_dev.DreamsApp_clientreproductivehealthdata rh
      ON fp.clientreproductivehealthdata_id = rh.id
      WHERE  (rh.date_created > last_update_time or rh.date_changed > last_update_time)
      GROUP BY rh.client_id
  ) rpr_data on rpr_data.client_id = e.client_id
SET e.known_fp_methods = rpr_data.known_fp_methods;

-- drugs used in past one year
UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      dd.client_id,
      group_concat(d.drug_id) AS drugs_used_in_last_12_months
      FROM dreams_dev.DreamsApp_clientdrugusedata_drug_used_last_12months d
      INNER JOIN dreams_dev.DreamsApp_clientdrugusedata dd ON d.clientdrugusedata_id = dd.id
      WHERE  (dd.date_created > last_update_time or dd.date_changed > last_update_time)
      GROUP BY dd.client_id
  ) d_data on d_data.client_id = e.client_id
SET e.drugs_used_in_last_12_months = d_data.drugs_used_in_last_12_months;

-- dreams programs enrolled

UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      cpd.client_id   AS client_id,
      group_concat(dp.dreamsprogramme_id) AS programmes_enrolled
      FROM dreams_dev.DreamsApp_clientparticipationindreams_dreams_program dp
      INNER JOIN dreams_dev.DreamsApp_clientparticipationindreams cpd
      ON dp.clientparticipationindreams_id = cpd.id
      WHERE  (cpd.date_created > last_update_time or cpd.date_changed > last_update_time)
      GROUP BY client_id
  ) p on p.client_id = e.client_id
SET e.programmes_enrolled = p.programmes_enrolled;

-- gbv sought provider
UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      gbv.client_id,
      group_concat(provider.gbvhelpprovider_id) AS provider_list
      FROM dreams_dev.DreamsApp_clientgenderbasedviolencedata_gbv_help_provider provider
      INNER JOIN dreams_dev.DreamsApp_clientgenderbasedviolencedata gbv on gbv.id = provider.clientgenderbasedviolencedata_id
      WHERE  (gbv.date_created > last_update_time or gbv.date_changed > last_update_time)
      GROUP BY gbv.client_id
  ) gbv on gbv.client_id = e.client_id
SET e.providers_sought = gbv.provider_list;

-- gbv preferred provider

UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      gbv.client_id,
      group_concat(provider.gbvhelpprovider_id) AS provider_list
      FROM dreams_dev.DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_p1bce provider -- DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_provider
      INNER JOIN dreams_dev.DreamsApp_clientgenderbasedviolencedata gbv on gbv.id = provider.clientgenderbasedviolencedata_id
      WHERE  (gbv.date_created > last_update_time or gbv.date_changed > last_update_time)
      GROUP BY gbv.client_id
  ) gbv on gbv.client_id = e.client_id
SET e.preferred_providers = gbv.provider_list;

-- current education supporter

UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      ed.client_id,
      group_concat(educationsupporter_id)   AS current_edu_supporter_list
      FROM dreams_dev.DreamsApp_clienteducationandemploymentdata_current_educationebf4 s -- DreamsApp_clienteducationandemploymentdata_current_education_supporter s
      INNER JOIN dreams_dev.DreamsApp_clienteducationandemploymentdata ed ON ed.id = s.clienteducationandemploymentdata_id
      WHERE  (ed.date_created > last_update_time or ed.date_changed > last_update_time)
      GROUP BY ed.client_id
  ) ed on ed.client_id = e.client_id
SET e.current_edu_supporter_list = ed.current_edu_supporter_list;

-- reason never tested for hiv

UPDATE dreams_dev.flat_dreams_enrollment e INNER JOIN (
    SELECT
      hiv_d.client_id,
      group_concat(rn.reasonnottestedforhiv_id) AS reason_not_tested_for_hiv
      FROM dreams_dev.DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv rn
      INNER JOIN dreams_dev.DreamsApp_clienthivtestingdata hiv_d ON hiv_d.id=rn.clienthivtestingdata_id
      WHERE  (hiv_d.date_created > last_update_time or hiv_d.date_changed > last_update_time)
      GROUP BY hiv_d.client_id
  ) hiv on hiv.client_id = e.client_id
SET e.reason_not_tested_for_hiv = hiv.reason_not_tested_for_hiv;

UPDATE dreams_dev.DreamsApp_flatenrollmenttablelog SET date_completed = NOW() WHERE id=record_id;

END$$
DELIMITER ;






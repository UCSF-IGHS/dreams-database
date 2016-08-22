
-- defining table to be populated by odk enrollment trigger
CREATE TABLE `odk_dreams_sync` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(100) NOT NULL DEFAULT '',
  `synced` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
);

-- ==============================================  Trigger ---------------------------------------------------------------

DELIMITER $$
DROP TRIGGER IF EXISTS after_dreams_odk_enrollment_insert_dev$$
CREATE TRIGGER after_dreams_odk_enrollment_insert_dev
AFTER INSERT
ON odk_aggregate.DREAMS_ENROLMENT_FORM_CORE2
FOR EACH ROW
BEGIN
INSERT INTO dreams.odk_dreams_sync
(
uuid
)
select
NEW._PARENT_AURI
from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE2 where _PARENT_AURI = NEW._PARENT_AURI
;
END;
$$
DELIMITER ;



-- -----------------------------------------       event definition  ------------------------------------------------------
DELIMITER $$
DROP EVENT IF EXISTS odk_dreams_enrollment_sync$$
CREATE EVENT odk_dreams_enrollment_sync
	ON SCHEDULE EVERY 2 MINUTE STARTS CURRENT_TIMESTAMP
	DO
		call sp_sync_odk_dreams_data();
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
    DECLARE v_row_count INT(11);

    DECLARE odk_enrollment_records CURSOR FOR
      SELECT uuid FROM odk_dreams_sync WHERE synced=0 LIMIT 50;

    DECLARE CONTINUE HANDLER FOR NOT FOUND
      SET no_more_rows = TRUE;

    OPEN odk_enrollment_records;
    SET v_row_count = FOUND_ROWS();

    IF v_row_count > 0 THEN
      get_enrollment_record: LOOP
      FETCH odk_enrollment_records INTO record_uuid;

      IF no_more_rows THEN
        CLOSE odk_enrollment_records;
        LEAVE get_enrollment_record;
      END IF;

      CALL sp_sync_client_data(record_uuid);

    END LOOP get_enrollment_record;
    ELSE
      SELECT "NO ROWS WERE FOUND";
    END IF;

  END
  $$
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS sp_sync_client_data$$
CREATE PROCEDURE sp_sync_client_data(IN recordUUID VARCHAR(100))
	BEGIN
    DECLARE exec_status INT(11) DEFAULT 1;
    DECLARE client_id INT(11);
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
      BEGIN
        SET exec_status = -1;
        ROLLBACK;
      END;
    -- perform all procedure calls in a transaction
    START TRANSACTION;

		CALL sp_demographic_data(recordUUID);
    SET client_id = LAST_INSERT_ID();
    -- CALL sp_individual_and_household_data(recordUUID, client_id);
    CALL sp_sexuality_data(recordUUID, client_id);
    -- CALL sp_reproductive_health_data(recordUUID, client_id);
    -- CALL sp_drug_use_data(recordUUID, client_id);
    -- CALL sp_program_participation_data(recordUUID, client_id);
    -- CALL sp_gbv_data(recordUUID, client_id);
    --  CALL sp_education_and_employment(recordUUID, client_id);
    -- CALL sp_hiv_testing(recordUUID, client_id);
    -- commit all inserts if all procedure calls are successful
    UPDATE odk_dreams_sync SET synced=exec_status WHERE uuid=recordUUID;
    COMMIT;

	END;
		$$
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
      odk_enrollment_uuid
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
      d.DEMOGRAPHIC_DREAMSID as Dreams_id,
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
      d._URI as uuid
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
      disability_type_id,
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
      d.MODULE_Q113 as disability_type,
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
  END
		$$
DELIMITER ;


-- Getting sexuality data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_sexuality_data$$
CREATE PROCEDURE sp_sexuality_data(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN
    SELECT concat('UUID: ',recordUUID, ', clientID: ', clientID);
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
  END
		$$
DELIMITER ;



-- Getting Drug Use data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_drug_use_data$$
CREATE PROCEDURE sp_drug_use_data(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN

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
  END
		$$
DELIMITER ;


-- Getting Dreams Programme participation
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_program_participation_data$$
CREATE PROCEDURE sp_program_participation_data(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN

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
  END
		$$
DELIMITER ;


-- Getting GBV data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_gbv_data$$
CREATE PROCEDURE sp_gbv_data(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN

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
  END
		$$
DELIMITER ;


-- Getting Education and employment data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_education_and_employment$$
CREATE PROCEDURE sp_education_and_employment(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN

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
  END
		$$
DELIMITER ;


-- Getting HIV testing
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_hiv_testing$$
CREATE PROCEDURE sp_hiv_testing(IN recordUUID VARCHAR(100), IN clientID INT(11))
	BEGIN

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
  END
		$$
DELIMITER ;

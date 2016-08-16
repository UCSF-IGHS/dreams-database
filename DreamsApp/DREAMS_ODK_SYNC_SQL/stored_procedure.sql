-- event definition
DELIMITER $$
DROP EVENT IF EXISTS odk_dreams_enrollment_sync$$
CREATE EVENT odk_dreams_enrollment_sync
	ON SCHEDULE EVERY 2 MINUTE STARTS CURRENT_TIMESTAMP
	DO
		call syn_odk_dreams_enrollment();
	$$
DELIMITER ;


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

DELIMITER $$
DROP PROCEDURE IF EXISTS syn_odk_dreams_enrollment$$
CREATE PROCEDURE syn_odk_dreams_enrollment(IN recordUUID VARCHAR(100))
	BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
      BEGIN
        UPDATE odk_dreams_sync SET synced=-1 WHERE uuid=recordUUID;
      END;
    -- perform all procedure calls in a transaction
    START TRANSACTION;

		CALL sp_demographic_data(recordUUID);
    CALL sp_individual_and_household_data(recordUUID);
    CALL sp_sexuality_data(recordUUID, client_id);
    CALL sp_reproductive_health_data(recordUUID);
    CALL sp_drug_use_data(recordUUID);
    CALL sp_program_participation_data(recordUUID);
    CALL sp_gbv_data(recordUUID);
    CALL sp_education_and_employment(recordUUID);
    -- commit all inserts if all procedure calls are successful
     UPDATE odk_dreams_sync SET synced=1 WHERE uuid=recordUUID;
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
      odk_enrollment_uuid
    )
    select
      d.DEMOGRAPHIC_FIRSTNAME_1 as f_name,
      d.DEMOGRAPHIC_MIDDLENAME_1 as m_name,
      d.DEMOGRAPHIC_LASTNAME_1 as l_name,
      date(d.DEMOGRAPHIC_DOB) as dob,
      date(d.DEMOGRAPHIC_DOE) as date_of_enrollment,
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
      COALESCE(o.RESPONSE2, o.RESPONSE2SPECIFY) as verification_doc,
      COALESCE(d.DEMOGRAPHIC_VERIFICATION_1, d.DEMOGRAPHIC_VERIFICATION_2, d.DEMOGRAPHIC_VERIFICATION_3, d.DEMOGRAPHIC_VERIFICATIONSPECIFY) as verification_doc_no,
      o.IPNAME as ip_name
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE3 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where o.ENROLNOTENROLED = 1 and d._PARENT_AURI in (select uuid from non_synced_odk_enrollment);
  END
		$$
DELIMITER ;

-- Getting individual and household data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_individual_and_household_data$$
CREATE PROCEDURE sp_individual_and_household_data(IN recordUUID VARCHAR(100))
	BEGIN

    INSERT INTO dreams_dev.DreamsApp_client
    (
      client,
      head_of_household,
      last_name,
      head_of_household_other,
      age_of_household_head,
      is_father_alive,
      is_mother_alive,
      is_parent_chronically_ill,
      main_floor_material,
      main_floor_material_other,
      main_roof_material,
      main_roof_material_other,
      main_wall_material,
      main_wall_material_other,
      source_of_drinking_water,
      source_of_drinking_water_other,
      ever_missed_full_day_food_in_4wks,
      no_of_days_missed_food_in_4wks,
      has_disability,
      disability_type,
      disability_type_other,
      no_of_people_in_household,
      no_of_females,
      no_of_males,
      no_of_adults,
      no_of_children,
      ever_enrolled_in_ct_program,
      currently_in_ct_program,
      current_ct_program
    )
    select
      d.DEMOGRAPHIC_FIRSTNAME_1 as f_name,
      d.DEMOGRAPHIC_MIDDLENAME_1 as m_name,
      d.DEMOGRAPHIC_LASTNAME_1 as l_name,
      date(d.DEMOGRAPHIC_DOB) as dob,
      date(d.DEMOGRAPHIC_DOE) as date_of_enrollment,
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
      COALESCE(o.RESPONSE2, o.RESPONSE2SPECIFY) as verification_doc,
      COALESCE(d.DEMOGRAPHIC_VERIFICATION_1, d.DEMOGRAPHIC_VERIFICATION_2, d.DEMOGRAPHIC_VERIFICATION_3, d.DEMOGRAPHIC_VERIFICATIONSPECIFY) as verification_doc_no,
      o.IPNAME as ip_name
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE3 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where o.ENROLNOTENROLED = 1 and d._PARENT_AURI in (select uuid from non_synced_odk_enrollment);
  END
		$$
DELIMITER ;


-- Getting sexuality data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_sexuality_data$$
CREATE PROCEDURE sp_sexuality_data(IN recordUUID VARCHAR(100))
	BEGIN

    INSERT INTO dreams_dev.DreamsApp_client
    (
      client,
      ever_had_sex,
      last_name,
      age_at_first_sexual_encounter,
      has_sexual_partner,
      sex_partners_in_last_12months,
      age_of_last_partner,
      age_of_second_last_partner,
      age_of_third_last_partner,
      last_partner_circumcised,
      second_last_partner_circumcised,
      third_last_partner_circumcised,
      know_last_partner_hiv_status,
      know_second_last_partner_hiv_status,
      know_third_last_partner_hiv_status,
      used_condom_with_last_partner,
      used_condom_with_second_last_partner,
      used_condom_with_third_last_partner,
      received_money_gift_for_sex
    )
    select
      d.DEMOGRAPHIC_FIRSTNAME_1 as f_name,
      d.DEMOGRAPHIC_MIDDLENAME_1 as m_name,
      d.DEMOGRAPHIC_LASTNAME_1 as l_name,
      date(d.DEMOGRAPHIC_DOB) as dob,
      date(d.DEMOGRAPHIC_DOE) as date_of_enrollment,
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
      COALESCE(o.RESPONSE2, o.RESPONSE2SPECIFY) as verification_doc,
      COALESCE(d.DEMOGRAPHIC_VERIFICATION_1, d.DEMOGRAPHIC_VERIFICATION_2, d.DEMOGRAPHIC_VERIFICATION_3, d.DEMOGRAPHIC_VERIFICATIONSPECIFY) as verification_doc_no,
      o.IPNAME as ip_name
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE3 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where o.ENROLNOTENROLED = 1 and d._PARENT_AURI in (select uuid from non_synced_odk_enrollment);
  END
		$$
DELIMITER ;


-- Getting reproductive health data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_reproductive_health_data$$
CREATE PROCEDURE sp_reproductive_health_data(IN recordUUID VARCHAR(100))
	BEGIN

    INSERT INTO dreams_dev.DreamsApp_client
    (
      client,
      has_biological_children,
      no_of_biological_children,
      currently_pregnant,
      current_anc_enrollment,
      anc_facility_name,
      fp_methods_awareness,
      known_fp_method,
      known_fp_method_other,
      currently_use_modern_fp,
      current_fp_method,
      current_fp_method_other
    )
    select
      d.DEMOGRAPHIC_FIRSTNAME_1 as f_name,
      d.DEMOGRAPHIC_MIDDLENAME_1 as m_name,
      d.DEMOGRAPHIC_LASTNAME_1 as l_name,
      date(d.DEMOGRAPHIC_DOB) as dob,
      date(d.DEMOGRAPHIC_DOE) as date_of_enrollment,
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
      COALESCE(o.RESPONSE2, o.RESPONSE2SPECIFY) as verification_doc,
      COALESCE(d.DEMOGRAPHIC_VERIFICATION_1, d.DEMOGRAPHIC_VERIFICATION_2, d.DEMOGRAPHIC_VERIFICATION_3, d.DEMOGRAPHIC_VERIFICATIONSPECIFY) as verification_doc_no,
      o.IPNAME as ip_name
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE3 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where o.ENROLNOTENROLED = 1 and d._PARENT_AURI in (select uuid from non_synced_odk_enrollment);
  END
		$$
DELIMITER ;



-- Getting Drug Use data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_drug_use_data$$
CREATE PROCEDURE sp_drug_use_data(IN recordUUID VARCHAR(100))
	BEGIN

    INSERT INTO dreams_dev.DreamsApp_client
    (
      client,
      used_alcohol_last_12months,
      frequency_of_alcohol_last_12months,
      drug_abuse_last_12months,
      drug_abuse_last_12months_other,
      drug_used_last_12months,
      drug_used_last_12months_other,
      produced_alcohol_last_12months
    )
    select
      d.DEMOGRAPHIC_FIRSTNAME_1 as f_name,
      d.DEMOGRAPHIC_MIDDLENAME_1 as m_name,
      d.DEMOGRAPHIC_LASTNAME_1 as l_name,
      date(d.DEMOGRAPHIC_DOB) as dob,
      date(d.DEMOGRAPHIC_DOE) as date_of_enrollment,
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
      COALESCE(o.RESPONSE2, o.RESPONSE2SPECIFY) as verification_doc,
      COALESCE(d.DEMOGRAPHIC_VERIFICATION_1, d.DEMOGRAPHIC_VERIFICATION_2, d.DEMOGRAPHIC_VERIFICATION_3, d.DEMOGRAPHIC_VERIFICATIONSPECIFY) as verification_doc_no,
      o.IPNAME as ip_name
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE3 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where o.ENROLNOTENROLED = 1 and d._PARENT_AURI in (select uuid from non_synced_odk_enrollment);
  END
		$$
DELIMITER ;


-- Getting Dreams Programme participation
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_program_participation_data$$
CREATE PROCEDURE sp_program_participation_data(IN recordUUID VARCHAR(100))
	BEGIN

    INSERT INTO dreams_dev.DreamsApp_client
    (
      client,
      dreams_program,
      dreams_program_other
    )
    select
      d.DEMOGRAPHIC_FIRSTNAME_1 as f_name,
      d.DEMOGRAPHIC_MIDDLENAME_1 as m_name,
      d.DEMOGRAPHIC_LASTNAME_1 as l_name,
      date(d.DEMOGRAPHIC_DOB) as dob,
      date(d.DEMOGRAPHIC_DOE) as date_of_enrollment,
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
      COALESCE(o.RESPONSE2, o.RESPONSE2SPECIFY) as verification_doc,
      COALESCE(d.DEMOGRAPHIC_VERIFICATION_1, d.DEMOGRAPHIC_VERIFICATION_2, d.DEMOGRAPHIC_VERIFICATION_3, d.DEMOGRAPHIC_VERIFICATIONSPECIFY) as verification_doc_no,
      o.IPNAME as ip_name
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE3 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where o.ENROLNOTENROLED = 1 and d._PARENT_AURI in (select uuid from non_synced_odk_enrollment);
  END
		$$
DELIMITER ;


-- Getting GBV data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_gbv_data$$
CREATE PROCEDURE sp_gbv_data(IN recordUUID VARCHAR(100))
	BEGIN

    INSERT INTO dreams_dev.DreamsApp_client
    (
      client,
      humiliated_ever,
      humiliated_last_3months,
      threats_to_hurt_ever,
      threats_to_hurt_last_3months,
      insulted_ever,
      insulted_last_3months,
      economic_threat_ever,
      economic_threat_last_3months,
      physical_violence_ever,
      physical_violence_last_3months,
      physically_forced_sex_ever,
      physically_forced_sex_last_3months,
      physically_forced_other_sex_acts_ever,
      physically_forced_other_sex_acts_last_3months,
      threatened_for_sexual_acts_ever,
      threatened_for_sexual_acts_last_3months,
      seek_help_after_gbv,
      gbv_help_provider,
      gbv_help_provider_other,
      knowledge_of_gbv_help_centres,
      preferred_gbv_help_provider,
      preferred_gbv_help_provider_other
    )
    select
      d.DEMOGRAPHIC_FIRSTNAME_1 as f_name,
      d.DEMOGRAPHIC_MIDDLENAME_1 as m_name,
      d.DEMOGRAPHIC_LASTNAME_1 as l_name,
      date(d.DEMOGRAPHIC_DOB) as dob,
      date(d.DEMOGRAPHIC_DOE) as date_of_enrollment,
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
      COALESCE(o.RESPONSE2, o.RESPONSE2SPECIFY) as verification_doc,
      COALESCE(d.DEMOGRAPHIC_VERIFICATION_1, d.DEMOGRAPHIC_VERIFICATION_2, d.DEMOGRAPHIC_VERIFICATION_3, d.DEMOGRAPHIC_VERIFICATIONSPECIFY) as verification_doc_no,
      o.IPNAME as ip_name
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE3 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where o.ENROLNOTENROLED = 1 and d._PARENT_AURI in (select uuid from non_synced_odk_enrollment);
  END
		$$
DELIMITER ;


-- Getting Education and employment data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_education_and_employment$$
CREATE PROCEDURE sp_education_and_employment(IN recordUUID VARCHAR(100))
	BEGIN

    INSERT INTO dreams_dev.DreamsApp_client
    (
      client,
      currently_in_school,
      current_school_name,
      current_school_type,
      current_school_level,
      current_class,
      current_school_level_other,
      current_education_supporter,
      current_education_supporter_other,
      reason_not_in_school,
      reason_not_in_school_other,
      last_time_in_school,
      dropout_school_level,
      dropout_class,
      life_wish,
      life_wish_other,
      current_income_source,
      current_income_source_other,
      has_savings,
      banking_place,
      banking_place_other
    )
    select
      d.DEMOGRAPHIC_FIRSTNAME_1 as f_name,
      d.DEMOGRAPHIC_MIDDLENAME_1 as m_name,
      d.DEMOGRAPHIC_LASTNAME_1 as l_name,
      date(d.DEMOGRAPHIC_DOB) as dob,
      date(d.DEMOGRAPHIC_DOE) as date_of_enrollment,
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
      COALESCE(o.RESPONSE2, o.RESPONSE2SPECIFY) as verification_doc,
      COALESCE(d.DEMOGRAPHIC_VERIFICATION_1, d.DEMOGRAPHIC_VERIFICATION_2, d.DEMOGRAPHIC_VERIFICATION_3, d.DEMOGRAPHIC_VERIFICATIONSPECIFY) as verification_doc_no,
      o.IPNAME as ip_name
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE3 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where o.ENROLNOTENROLED = 1 and d._PARENT_AURI in (select uuid from non_synced_odk_enrollment);
  END
		$$
DELIMITER ;


-- Getting Many to Many relationship data
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_many_to_many$$
CREATE PROCEDURE sp_many_to_many(IN odkUUID VARCHAR(100))
	BEGIN

    INSERT INTO dreams_dev.DreamsApp_client
    (
      client,
      currently_in_school,
      current_school_name,
      current_school_type,
      current_school_level,
      current_class,
      current_school_level_other,
      current_education_supporter,
      current_education_supporter_other,
      reason_not_in_school,
      reason_not_in_school_other,
      last_time_in_school,
      dropout_school_level,
      dropout_class,
      life_wish,
      life_wish_other,
      current_income_source,
      current_income_source_other,
      has_savings,
      banking_place,
      banking_place_other
    )
    select
      d.DEMOGRAPHIC_FIRSTNAME_1 as f_name,
      d.DEMOGRAPHIC_MIDDLENAME_1 as m_name,
      d.DEMOGRAPHIC_LASTNAME_1 as l_name,
      date(d.DEMOGRAPHIC_DOB) as dob,
      date(d.DEMOGRAPHIC_DOE) as date_of_enrollment,
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
      COALESCE(o.RESPONSE2, o.RESPONSE2SPECIFY) as verification_doc,
      COALESCE(d.DEMOGRAPHIC_VERIFICATION_1, d.DEMOGRAPHIC_VERIFICATION_2, d.DEMOGRAPHIC_VERIFICATION_3, d.DEMOGRAPHIC_VERIFICATIONSPECIFY) as verification_doc_no,
      o.IPNAME as ip_name
    from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE3 d
    inner join odk_aggregate.DREAMS_ENROLMENT_FORM_CORE o on o._URI = d._PARENT_AURI
    where o.ENROLNOTENROLED = 1 and d._PARENT_AURI in (select uuid from non_synced_odk_enrollment);
  END
		$$
DELIMITER ;

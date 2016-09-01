
-- Define a cursor to loop through odk_dreams_sync

DELIMITER $$
DROP PROCEDURE IF EXISTS enrollment_cursor$$
CREATE PROCEDURE enrollment_cursor()
  BEGIN

    DECLARE no_more_rows BOOLEAN;
    DECLARE record_uuid VARCHAR(100);

    DECLARE odk_enrollment_records CURSOR FOR
      SELECT uuid FROM odk_dreams_sync WHERE synced=0 LIMIT 50;

    DECLARE CONTINUE HANDLER FOR NOT FOUND
      SET no_more_rows = TRUE;

    OPEN odk_enrollment_records;

    get_enrollment_record: LOOP
      FETCH odk_enrollment_records INTO record_uuid;

      IF no_more_rows THEN
        CLOSE odk_enrollment_records;
        LEAVE get_enrollment_record;
      END IF;

      CALL syn_odk_dreams_enrollment(record_uuid);

    END LOOP get_enrollment_record;

  END
  $$
DELIMITER ;

-- ----------------------------------------- test ----------------
DELIMITER $$
DROP PROCEDURE IF EXISTS enrollment_cursor$$
CREATE PROCEDURE enrollment_cursor()
  BEGIN

    DECLARE no_more_rows BOOLEAN;
    DECLARE record_uuid VARCHAR(100);

    DECLARE odk_enrollment_records CURSOR FOR
      SELECT uuid FROM odk_dreams_sync WHERE synced=0 LIMIT 50;

    DECLARE CONTINUE HANDLER FOR NOT FOUND
      SET no_more_rows = TRUE;

    OPEN odk_enrollment_records;

    get_enrollment_record: LOOP
      FETCH odk_enrollment_records INTO record_uuid;

      IF no_more_rows THEN
        CLOSE odk_enrollment_records;
        LEAVE get_enrollment_record;
      END IF;
      SELECT record_uuid;
      CALL syn_odk_dreams_enrollment(record_uuid);

    END LOOP get_enrollment_record;

  END
  $$
DELIMITER ;


/*SELECT c.column_name
  FROM INFORMATION_SCHEMA.COLUMNS c
 WHERE c.table_name = 'tbl_name'
-- AND c.table_schema = 'db_name'
ORDER BY c.column_name*/

SELECT c.column_name
  FROM INFORMATION_SCHEMA.COLUMNS c
 WHERE c.table_name = 'DREAMS_ENROLMENT_FORM_CORE'
ORDER BY c.column_name;

SELECT c.column_name
  FROM INFORMATION_SCHEMA.COLUMNS c
 WHERE c.table_name = 'DREAMS_ENROLMENT_FORM_CORE2'
ORDER BY c.column_name
;
-- ------------------------------

INSERT INTO dreams_dev.odk_dreams_sync (uuid) select _URI from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE;

CALL sp_demographic_data('uuid:c793d18b-5a17-4a6a-a63e-2bdb984a9ae5');
-- ========================================


DELETE from DreamsApp_clientindividualandhouseholddata;
ALTER TABLE DreamsApp_clientindividualandhouseholddata AUTO_INCREMENT=1;

DELETE from DreamsApp_clientsexualactivitydata;
ALTER TABLE DreamsApp_clientsexualactivitydata AUTO_INCREMENT=1;

DELETE from DreamsApp_clientreproductivehealthdata_known_fp_method;
ALTER TABLE DreamsApp_clientreproductivehealthdata_known_fp_method AUTO_INCREMENT=1;

DELETE from DreamsApp_clientreproductivehealthdata;
ALTER TABLE DreamsApp_clientreproductivehealthdata AUTO_INCREMENT=1;

DELETE FROM DreamsApp_clientdrugusedata_drug_used_last_12months;
ALTER TABLE DreamsApp_clientdrugusedata_drug_used_last_12months AUTO_INCREMENT=1;

DELETE FROM DreamsApp_clientdrugusedata;
ALTER TABLE DreamsApp_clientdrugusedata AUTO_INCREMENT=1;

DELETE FROM DreamsApp_clientparticipationindreams_dreams_program;
ALTER TABLE DreamsApp_clientparticipationindreams_dreams_program AUTO_INCREMENT=1;

DELETE FROM DreamsApp_clientparticipationindreams;
ALTER TABLE DreamsApp_clientparticipationindreams AUTO_INCREMENT=1;

DELETE FROM DreamsApp_clientgenderbasedviolencedata_gbv_help_provider;
ALTER TABLE DreamsApp_clientgenderbasedviolencedata_gbv_help_provider AUTO_INCREMENT=1;

DELETE FROM DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_p1bce;
ALTER TABLE DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_p1bce AUTO_INCREMENT=1;

DELETE FROM DreamsApp_clientgenderbasedviolencedata;
ALTER TABLE DreamsApp_clientgenderbasedviolencedata AUTO_INCREMENT=1;

DELETE FROM DreamsApp_clienteducationandemploymentdata_current_educationebf4;
ALTER TABLE DreamsApp_clienteducationandemploymentdata_current_educationebf4 AUTO_INCREMENT=1;

DELETE from DreamsApp_clienteducationandemploymentdata;
ALTER TABLE DreamsApp_clienteducationandemploymentdata AUTO_INCREMENT=1;

DELETE from DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv;
ALTER TABLE DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv AUTO_INCREMENT=1;

DELETE from DreamsApp_clienthivtestingdata;
ALTER TABLE DreamsApp_clienthivtestingdata AUTO_INCREMENT=1;


DELETE from DreamsApp_client;
ALTER TABLE DreamsApp_client AUTO_INCREMENT=1;

update odk_dreams_sync set synced=0;


-- ================================================
select id, client_id from DreamsApp_clienteducationandemploymentdata;
select odk_enrollment_uuid, id from DreamsApp_client;

-- ============================ changing collation and character set ==================
ALTER DATABASE odk_aggregate CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE DREAMS_ENROLMENT_FORM_CORE CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE DREAMS_ENROLMENT_FORM_CORE2 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE DREAMS_ENROLMENT_FORM_MODULE_2_Q204 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE DREAMS_ENROLMENT_FORM_MODULE_3_Q307 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE DREAMS_ENROLMENT_FORM_MODULE_3_Q3072 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE DREAMS_ENROLMENT_FORM_Q507 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE DREAMS_ENROLMENT_FORM_MODULE_6_Q610 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE DREAMS_ENROLMENT_FORM_MODULE_6_Q612 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE DREAMS_ENROLMENT_FORM_MODULE_7_Q704 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
ALTER TABLE DREAMS_ENROLMENT_FORM_MODULE_8_Q801 CONVERT TO CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';


-- ========================================== many to many relationship ============================

-- Education and employment ++++++
--        current_education_supporter -- table DREAMS_ENROLMENT_FORM_MODULE_2_Q204

--

-- Client HIV Testing ++++++
--        reason_never_tested_for_hiv -- table DREAMS_ENROLMENT_FORM_MODULE_3_Q307

-- Reproductive Health
--        known_fp_method -- table DREAMS_ENROLMENT_FORM_Q507

-- Gender Based Violence
--        gbv_help_provider -- table DREAMS_ENROLMENT_FORM_MODULE_6_Q610
--        preferred_gbv_help_provider -- table DREAMS_ENROLMENT_FORM_MODULE_6_Q612

-- Drug Use
--        drug_used_last_12months -- table DREAMS_ENROLMENT_FORM_MODULE_7_Q704


-- Programme participation
--        dreams_program -- table DREAMS_ENROLMENT_FORM_MODULE_8_Q801


SELECT hiv_d.*, rn_not_tested.reason_not_tested_for_hiv from DreamsApp_clienthivtestingdata hiv_d
left outer join (
    SELECT rn.clienthivtestingdata_id as rec_id, group_concat(rn.reasonnottestedforhiv_id) as reason_not_tested_for_hiv
    from DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv rn
    GROUP BY rec_id
    ) rn_not_tested on rn_not_tested.rec_id = hiv_d.id
GROUP BY hiv_d.id
;

SELECT
d.*,
i.*,
s.*,
r.*,
dr.*,
p.*,
gbv.*,
edu.*,
hiv.*
from
DreamsApp_client as d
INNER JOIN DreamsApp_clientindividualandhouseholddata i on i.client_id = d.id
INNER JOIN DreamsApp_clientsexualactivitydata s on s.client_id = d.id
left OUTER JOIN (
  SELECT *
FROM DreamsApp_clientreproductivehealthdata rh
  LEFT OUTER JOIN
(
  SELECT
    fp.clientreproductivehealthdata_id as rh_id,
    group_concat(familyplanningmethod_id) AS known_fp_methods
  FROM DreamsApp_clientreproductivehealthdata_known_fp_method fp
    LEFT OUTER JOIN DreamsApp_clientreproductivehealthdata rh ON fp.clientreproductivehealthdata_id = rh.id
  GROUP BY fp.clientreproductivehealthdata_id
) fpm on fpm.rh_id = rh.id ) r on r.client_id = d.id
LEFT OUTER JOIN (
  SELECT *
FROM DreamsApp_clientdrugusedata dd
  LEFT OUTER JOIN
(
SELECT
d.clientdrugusedata_id as dd_id,
group_concat(d.drug_id) AS drugs_used_in_last_12_months
FROM DreamsApp_clientdrugusedata_drug_used_last_12months d
LEFT OUTER JOIN DreamsApp_clientdrugusedata inner_dd ON d.clientdrugusedata_id = inner_dd.id
GROUP BY dd_id
) d on d.dd_id = dd.id ) dr on dr.client_id = d.id
INNER JOIN (SELECT *
FROM DreamsApp_clientparticipationindreams pp
  LEFT OUTER JOIN
(
SELECT
dp.clientparticipationindreams_id as pr_id,
group_concat(dp.dreamsprogramme_id) AS programmes_enrolled
FROM DreamsApp_clientparticipationindreams_dreams_program dp
LEFT OUTER JOIN DreamsApp_clientparticipationindreams inner_pp ON dp.clientparticipationindreams_id = inner_pp.id
GROUP BY pr_id
) pr on pr.pr_id = pp.id) p on p.client_id = d.id
INNER JOIN DreamsApp_clientgenderbasedviolencedata gbv on gbv.client_id = d.id
INNER JOIN DreamsApp_clienteducationandemploymentdata edu on edu.client_id = d.id
INNER JOIN DreamsApp_clienthivtestingdata hiv on hiv.client_id = d.id;

-- --------------------------------------- TEST ----------------

SELECT
d.*,
i.*,
s.*,
r.*,
dr.*,
p.*,
gbv.*,
edu.*,
hiv.*
from
DreamsApp_client as d
INNER JOIN DreamsApp_clientindividualandhouseholddata i on i.client_id = d.id
INNER JOIN DreamsApp_clientsexualactivitydata s on s.client_id = d.id
left OUTER JOIN (
SELECT *
FROM DreamsApp_clientreproductivehealthdata rh
LEFT OUTER JOIN
(
SELECT
fp.clientreproductivehealthdata_id as rh_id,
group_concat(familyplanningmethod_id) AS known_fp_methods
FROM DreamsApp_clientreproductivehealthdata_known_fp_method fp
LEFT OUTER JOIN DreamsApp_clientreproductivehealthdata rh ON fp.clientreproductivehealthdata_id = rh.id
GROUP BY fp.clientreproductivehealthdata_id
) fpm on fpm.rh_id = rh.id ) r on r.client_id = d.id
LEFT OUTER JOIN (
SELECT *
FROM DreamsApp_clientdrugusedata dd
LEFT OUTER JOIN
(
SELECT
d.clientdrugusedata_id as dd_id,
group_concat(d.drug_id) AS drugs_used_in_last_12_months
FROM DreamsApp_clientdrugusedata_drug_used_last_12months d
LEFT OUTER JOIN DreamsApp_clientdrugusedata inner_dd ON d.clientdrugusedata_id = inner_dd.id
GROUP BY dd_id
) d on d.dd_id = dd.id ) dr on dr.client_id = d.id
INNER JOIN (SELECT *
FROM DreamsApp_clientparticipationindreams pp
LEFT OUTER JOIN
(
SELECT
dp.clientparticipationindreams_id as pr_id,
group_concat(dp.dreamsprogramme_id) AS programmes_enrolled
FROM DreamsApp_clientparticipationindreams_dreams_program dp
LEFT OUTER JOIN DreamsApp_clientparticipationindreams inner_pp ON dp.clientparticipationindreams_id = inner_pp.id
GROUP BY pr_id
) pr on pr.pr_id = pp.id) p on p.client_id = d.id
INNER JOIN (SELECT gbv.*, providers.provider_list as providers_sought, p_providers.provider_list as preferred_providers
FROM DreamsApp_clientgenderbasedviolencedata gbv
LEFT OUTER JOIN (
select provider.clientgenderbasedviolencedata_id as rec_id, group_concat(provider.gbvhelpprovider_id) as provider_list
from DreamsApp_clientgenderbasedviolencedata_gbv_help_provider provider
GROUP BY rec_id
) providers on providers.rec_id = gbv.id
LEFT OUTER JOIN (
select provider.clientgenderbasedviolencedata_id as rec_id, group_concat(provider.gbvhelpprovider_id) as provider_list
from DreamsApp_clientgenderbasedviolencedata_preferred_gbv_help_p1bce provider
GROUP BY rec_id
    ) p_providers on p_providers.rec_id = gbv.id
GROUP BY gbv.id) gbv on gbv.client_id = d.id
INNER JOIN (SELECT ed.*, edu_sup.current_edu_supporter_list from DreamsApp_clienteducationandemploymentdata ed
left outer join (
    select s.clienteducationandemploymentdata_id as rec_id, group_concat(educationsupporter_id) as current_edu_supporter_list
    from  DreamsApp_clienteducationandemploymentdata_current_educationebf4 s
    GROUP BY rec_id
    ) edu_sup on edu_sup.rec_id = ed.id
GROUP BY ed.id) edu on edu.client_id = d.id
INNER JOIN (SELECT hiv_d.*, rn_not_tested.reason_not_tested_for_hiv from DreamsApp_clienthivtestingdata hiv_d
left outer join (
    SELECT rn.clienthivtestingdata_id as rec_id, group_concat(rn.reasonnottestedforhiv_id) as reason_not_tested_for_hiv
    from DreamsApp_clienthivtestingdata_reason_never_tested_for_hiv rn
    GROUP BY rec_id
    ) rn_not_tested on rn_not_tested.rec_id = hiv_d.id
GROUP BY hiv_d.id) hiv on hiv.client_id = d.id;

SELECT
d.*,
i.*,
s.*,
r.*,
dr.*,
p.*,
gbv.*,
edu.*,
hiv.*
from
DreamsApp_client as d
INNER JOIN DreamsApp_clientindividualandhouseholddata i on i.client_id = d.id
INNER JOIN DreamsApp_clientsexualactivitydata s on s.client_id = d.id
INNER JOIN DreamsApp_clientreproductivehealthdata r on r.client_id = d.id
INNER JOIN DreamsApp_clientdrugusedata dr on dr.client_id = d.id
INNER JOIN DreamsApp_clientparticipationindreams p on p.client_id = d.id
INNER JOIN DreamsApp_clientgenderbasedviolencedata gbv on gbv.client_id = d.id
INNER JOIN DreamsApp_clienteducationandemploymentdata edu on edu.client_id = d.id
INNER JOIN DreamsApp_clienthivtestingdata hiv on hiv.client_id = d.id






-- ==============================================  Trigger on Enrollment tables-----------------------------------------

DELIMITER $$
DROP TRIGGER IF EXISTS after_dreams_odk_enrollment_insert_dev$$
CREATE TRIGGER after_dreams_odk_enrollment_insert_dev
AFTER INSERT
ON odk_aggregate.DREAMS_ENROLMENT_FORM_CORE2
FOR EACH ROW
BEGIN
INSERT INTO dreams_test.odk_dreams_sync
(
uuid, form
)
select
NEW._PARENT_AURI, 'enrollment'
from odk_aggregate.DREAMS_ENROLMENT_FORM_CORE2 where _PARENT_AURI = NEW._PARENT_AURI
;
END;
$$
DELIMITER ;


-- ==============================================  Trigger on Home Visit tables-----------------------------------------

DELIMITER $$
DROP TRIGGER IF EXISTS after_dreams_odk_home_visit_insert$$
CREATE TRIGGER after_dreams_odk_home_visit_insert
AFTER INSERT
ON odk_aggregate.CT_HOME_VISIT_VERFICATION_FORM_CORE
FOR EACH ROW
BEGIN
INSERT INTO dreams_test.odk_dreams_sync
(
uuid, form
)
select
NEW._URI, 'home_visit'
from odk_aggregate.CT_HOME_VISIT_VERFICATION_FORM_CORE where _URI = NEW._URI
;
END;
$$
DELIMITER ;


-- ------------------------------------------- take care of imports from excel database -------------------------------
-- set date created



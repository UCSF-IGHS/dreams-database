
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
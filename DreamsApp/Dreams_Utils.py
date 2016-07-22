from django.core.files.storage import default_storage
import openpyxl as xl
import xlrd
import traceback
from Dreams_Excel_Mapping import *
from string import Template
import datetime
from django.db import connection


class DreamsEnrollmentExcelDatabase(object):

    document_path = ''
    workbook = ''

    def __init__(self):
        pass

    def create_tmp_file(self, excel):
        try:
            with open(default_storage.path('tmp/enrollment.xlsx'), 'wb+') as destination:
                for chunk in excel.chunks():
                    destination.write(chunk)
            destination.closed
            self.document_path = default_storage.path('tmp/enrollment.xlsx')
            return default_storage.path('tmp/enrollment.xlsx')
        except:
            print 'Could not create a temp file'
            return

    def get_document_path(self):
        return self.document_path

    def validate_excel_document(self):
        # check to see if Main Database sheet exists
        # TODO define and implement more checks

        wb = xl.load_workbook(self.get_document_path(), read_only=True, keep_vba=False)
        self.workbook = wb
        if 'Main Database' in wb.get_sheet_names():
            return True
        else:
            return False

    def get_sheet_names(self):
        if self.validate_excel_document():
            return xl.load_workbook(self.get_document_path(), read_only=True, keep_vba=False).get_sheet_names()
        else:
            return 'Invalid Sheets'

    def excel_enrollment_data(self):
        if self.validate_excel_document():
            try:
                sql_statement = self.generate_insert_SQL(52, 60)
                # print sql_statement
                self.execute_SQL_Query(sql_statement)

            except Exception as e:
                tb = traceback.format_exc()
                print 'There was an error ' + tb
            return

    def generate_insert_SQL(self, start, end):
        if self.validate_excel_document():
            try:
                print 'The Excel Database is Valid'
                print "Now processing the file.........."

                sql_statement = """
INSERT INTO DreamsApp_client
(first_name, middle_name, last_name, dreams_id, dss_id_number, implementing_partner_id, date_of_birth, date_of_enrollment, marital_status_id, phone_number,
county_of_residence_id, sub_county_id, ward_id, informal_settlement, village, landmark, guardian_name, relationship_with_guardian, guardian_phone_number, guardian_national_id, is_date_of_birth_estimated, verification_document_id, verification_doc_no )
VALUES """

                rangeList = range(start, end)
                lastNumber = rangeList[-1]
                row_qry = ''
                for rowid in range(start, end):

                    if rowid != lastNumber:
                        row_qry += self.generate_row_insert_SQL(rowid) + ', \n'
                    else:
                        row_qry += " " + self.generate_row_insert_SQL(rowid)

                return Template('$insert $values').substitute(insert=sql_statement, values=row_qry)

            except Exception as e:
                tb = traceback.format_exc()
                print 'There was an error ' + tb
            return

    def get_enrollment_sheet_openpyxl(self):
        return xl.load_workbook(self.get_document_path(), read_only=True, data_only=True).get_sheet_by_name('Main Database')

    def get_enrollment_sheet(self):
        return self.get_wb().sheet_by_name('Main Database')

    def get_wb(self):
        return xlrd.open_workbook(self.get_document_path(), on_demand=True)

    def get_row_data(self, row_num):

        sheet = self.get_enrollment_sheet_openpyxl()
        cols = self.openpyxl_demographic_columns()

        # map fields that should mirror webapp's

        ver_doc = str(sheet.cell(row=row_num, column=cols.get('verification_doc')).value)
        ver_doc = ExcelDreamsMapping.verification_document().get(ver_doc)

        marital_status = str(sheet.cell(row=row_num, column=cols.get('marital_status')).value)
        marital_status = ExcelDreamsMapping.marital_status_codes().get(marital_status)

        county = str(sheet.cell(row=row_num, column=cols.get('county')).value)
        county = ExcelDreamsMapping.county().get(county)

        sub_county = str(sheet.cell(row=row_num, column=cols.get('sub_county')).value)
        sub_county = ExcelDreamsMapping.sub_county().get(sub_county)

        ward = str(sheet.cell(row=row_num, column=cols.get('ward')).value)
        ward = ExcelDreamsMapping.ward_by_name().get(ward)

        dob_raw = sheet.cell(row=row_num, column=cols.get('dob')).value
        if dob_raw is not None:
            dob_raw = datetime.datetime.strftime(dob_raw, '%Y-%m-%d')

        doe_raw = sheet.cell(row=row_num, column=cols.get('date_of_enrollment')).value
        if doe_raw is not None:
            doe_raw = datetime.datetime.strftime(doe_raw, '%Y-%m-%d')

        row_values = {
            'serial_No': str(sheet.cell(row=row_num, column=cols.get('serial_No')).value),
            'IP': str(sheet.cell(row=row_num, column=cols.get('IP')).value),
            'first_name': str(sheet.cell(row=row_num, column=cols.get('first_name')).value),
            'middle_name': str(sheet.cell(row=row_num, column=cols.get('middle_name')).value),
            'last_name': str(sheet.cell(row=row_num, column=cols.get('last_name')).value),
            'dob': dob_raw,
            'verification_doc': ver_doc,
            'verification_doc_other': str(sheet.cell(row=row_num, column=cols.get('verification_doc_other')).value),
            'verification_doc_no': str(sheet.cell(row=row_num, column=cols.get('verification_doc_no')).value),
            'date_of_enrollment': doe_raw,
            'marital_status': marital_status,
            'client_phone_no': str(sheet.cell(row=row_num, column=cols.get('client_phone_no')).value),
            'county': county,
            'sub_county': sub_county,
            'ward': ward,
            'informal_settlement': str(sheet.cell(row=row_num, column=cols.get('informal_settlement')).value),
            'village': str(sheet.cell(row=row_num, column=cols.get('village')).value),
            'land_mark': str(sheet.cell(row=row_num, column=cols.get('land_mark')).value),
            'dreams_id': str(sheet.cell(row=row_num, column=cols.get('dreams_id')).value),
            'dss_id': str(sheet.cell(row=row_num, column=cols.get('dss_id')).value),
            'caregiver_first_name': str(sheet.cell(row=row_num, column=cols.get('caregiver_first_name')).value),
            'caregiver_middle_name': str(sheet.cell(row=row_num, column=cols.get('caregiver_middle_name')).value),
            'caregiver_last_name': str(sheet.cell(row=row_num, column=cols.get('caregiver_last_name')).value),
            'caregiver_relationship': str(sheet.cell(row=row_num, column=cols.get('caregiver_relationship')).value),
            'caregiver_relationship_other': str(sheet.cell(row=row_num, column=cols.get('caregiver_relationship_other')).value),
            'caregiver_phone_no': str(sheet.cell(row=row_num, column=cols.get('caregiver_phone_no')).value),
            'caregiver_id_no': str(sheet.cell(row=row_num, column=cols.get('caregiver_id_no')).value),
        }
        return row_values


    def generate_row_insert_SQL(self, row_num):

        row_data = self.get_row_data(row_num)
        caregiver_fname = row_data.get('caregiver_first_name')
        caregiver_mname = row_data.get('caregiver_middle_name')
        caregiver_lname = row_data.get('caregiver_last_name')

        coded_rel = row_data.get('caregiver_relationship')
        other_rel = row_data.get('caregiver_relationship_other')
        date_of_birth_estimated = 0

        # django app has no field for other relationship. check which one has value

        if coded_rel != 'None' or other_rel != 'None':
            if other_rel != 'None':
                caregiver_relationship = other_rel
            else:
                caregiver_relationship = coded_rel
        else:
            caregiver_relationship = ''

        ver_doc = row_data.get('verification_doc')
        ver_doc_other = row_data.get('verification_doc_other')

        # TODO: Handle other verification documents. It is not currently in the Client's model. Code therefore picks only coded documents

        guardian_name = (caregiver_fname + " " if caregiver_fname != 'None' else "") + (caregiver_mname + " " if caregiver_mname != 'None' else "") + (caregiver_lname if caregiver_lname != 'None' else "")

        values_template = Template(
            '("$first_name", "$middle_name", "$last_name", "$dreams_id", "$dss_id_number", "$implementing_partner_id", "$date_of_birth", "$date_of_enrollment", "$marital_status_id", "$phone_number", \
    "$county_of_residence_id", "$sub_county_id", "$ward_id", "$informal_settlement", "$village", "$landmark", "$guardian_name", "$relationship_with_guardian", "$guardian_phone_number", "$guardian_national_id", "$is_date_of_birth_estimated", "$verification_doc_id", "$verification_doc_no" )').safe_substitute(
            first_name=row_data.get('first_name') if row_data.get('first_name') !='None' else '',
            middle_name=row_data.get('middle_name') if row_data.get('middle_name') !='None' else '',
            last_name=row_data.get('last_name') if row_data.get('last_name') !='None' else '',
            dreams_id=row_data.get('dreams_id'),
            dss_id_number=row_data.get('dss_id') if row_data.get('dss_id') !='None' else '',
            implementing_partner_id=row_data.get('IP') if row_data.get('IP') !='None' else '',
            date_of_birth=row_data.get('dob') if row_data.get('dob') !='None' else '0000-00-00',
            date_of_enrollment=row_data.get('date_of_enrollment') if row_data.get('date_of_enrollment') !='None' else '0000-00-00',
            marital_status_id=row_data.get('marital_status') if row_data.get('marital_status') !='None' else '',
            phone_number=row_data.get('client_phone_no') if row_data.get('client_phone_no') !='None' else '',
            county_of_residence_id=row_data.get('county'),
            sub_county_id=row_data.get('sub_county'),
            ward_id=row_data.get('ward'),
            informal_settlement=row_data.get('informal_settlement') if row_data.get('informal_settlement') !='None' else '',
            village=row_data.get('village') if row_data.get('village') !='None' else '',
            landmark=row_data.get('land_mark') if row_data.get('land_mark') !='None' else '',
            guardian_name=guardian_name,
            relationship_with_guardian=caregiver_relationship,
            guardian_phone_number=row_data.get('caregiver_phone_no') if row_data.get('caregiver_phone_no') !='None' else '',
            guardian_national_id=row_data.get('caregiver_id_no') if row_data.get('caregiver_id_no') !='None' else '',
            is_date_of_birth_estimated=date_of_birth_estimated,
            verification_doc_id=row_data.get('verification_doc'),
            verification_doc_no=row_data.get('verification_doc_no')
        )

        return values_template

    def openpyxl_demographic_columns(self):
        demographics = {
            'serial_No': 1,
            'IP': 3,
            'first_name': 4,
            'middle_name': 5,
            'last_name': 6,
            'dob': 7,
            'verification_doc': 8,
            'verification_doc_other': 9,
            'verification_doc_no': 10,
            'date_of_enrollment': 11,
            'marital_status': 16,
            'client_phone_no': 17,
            'county': 18,
            'sub_county': 19,
            'ward': 20,
            'informal_settlement': 22,
            'village': 23,
            'land_mark': 24,
            'dreams_id': 25,
            'dss_id': 26,
            'caregiver_first_name': 27,
            'caregiver_middle_name': 28,
            'caregiver_last_name': 29,
            'caregiver_relationship': 30,
            'caregiver_relationship_other': 31,
            'caregiver_phone_no': 32,
            'caregiver_id_no': 33,
        }

        return demographics

    def execute_SQL_Query(self, sql):
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            print cursor.rowcount
        except Exception as e:
            print 'There was an Error running the query\n'
            traceback.format_exc()

        return




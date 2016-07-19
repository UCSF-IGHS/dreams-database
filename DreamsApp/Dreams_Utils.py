from django.core.files.storage import default_storage
import openpyxl as xl


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
                print 'Loading the doc'
                row5 = self.get_row_data(5)

                print row5

                # for row in main_db_sheet.rows:
                #     for cell in row:
                #         print(cell.value)

            except:
                print 'There was an error'
            return

    def get_enrollment_sheet(self):
        return xl.load_workbook(self.get_document_path(), read_only=True).get_sheet_by_name('Main Database')

    def get_row_data(self, row_num):
        sheet = self.get_enrollment_sheet()
        cols = self.excel_demographic_columns()
        row_values = {
            'serial_No': sheet.cell(row=row_num, column=cols.get('serial_No')).value,
            'IP': sheet.cell(row=row_num, column=cols.get('IP')).value,
            'first_name': sheet.cell(row=row_num, column=cols.get('first_name')).value,
            'middle_name': sheet.cell(row=row_num, column=cols.get('middle_name')).value,
            'last_name': sheet.cell(row=row_num, column=cols.get('last_name')).value,
            'dob': sheet.cell(row=row_num, column=cols.get('dob')).value,
            'verification_doc': sheet.cell(row=row_num, column=cols.get('verification_doc')).value,
            'verification_doc_other': sheet.cell(row=row_num, column=cols.get('verification_doc_other')).value,
            'verification_doc_no': sheet.cell(row=row_num, column=cols.get('verification_doc_no')).value,
            'date_of_enrollment': sheet.cell(row=row_num, column=cols.get('date_of_enrollment')).value,
            'marital_status': sheet.cell(row=row_num, column=cols.get('marital_status')).value,
            'client_phone_no': sheet.cell(row=row_num, column=cols.get('client_phone_no')).value,
            'county': sheet.cell(row=row_num, column=cols.get('county')).value,
            'sub_county': sheet.cell(row=row_num, column=cols.get('sub_county')).value,
            'ward': sheet.cell(row=row_num, column=cols.get('ward')).value,
            'informal_settlement': sheet.cell(row=row_num, column=cols.get('informal_settlement')).value,
            'village': sheet.cell(row=row_num, column=cols.get('village')).value,
            'land_mark': sheet.cell(row=row_num, column=cols.get('land_mark')).value,
            'dreams_id': sheet.cell(row=row_num, column=cols.get('dreams_id')).value,
            'dss_id': sheet.cell(row=row_num, column=cols.get('dss_id')).value,
            'caregiver_first_name': sheet.cell(row=row_num, column=cols.get('caregiver_first_name')).value,
            'caregiver_middle_name': sheet.cell(row=row_num, column=cols.get('caregiver_middle_name')).value,
            'caregiver_last_name': sheet.cell(row=row_num, column=cols.get('caregiver_last_name')).value,
            'caregiver_relationship': sheet.cell(row=row_num, column=cols.get('caregiver_relationship')).value,
            'caregiver_relationship_other': sheet.cell(row=row_num, column=cols.get('caregiver_relationship_other')).value,
            'caregiver_phone_no': sheet.cell(row=row_num, column=cols.get('caregiver_phone_no')).value,
            'caregiver_id_no': sheet.cell(row=row_num, column=cols.get('caregiver_id_no')).value,
        }
        return row_values






    def excel_demographic_columns(self):

        demographics = {
            'serial_No': 1,
            'IP': 2,
            'first_name': 4,
            'middle_name': 5,
            'last_name': 6,
            'dob': 7,
            'verification_doc': 8,
            'verification_doc_other': 9,
            'verification_doc_no': 10,
            'date_of_enrollment': 11,
            'marital_status': 15,
            'client_phone_no': 16,
            'county': 17,
            'sub_county': 18,
            'ward': 19,
            'informal_settlement': 21,
            'village': 22,
            'land_mark': 23,
            'dreams_id': 24,
            'dss_id': 25,
            'caregiver_first_name': 26,
            'caregiver_middle_name': 27,
            'caregiver_last_name': 28,
            'caregiver_relationship': 29,
            'caregiver_relationship_other': 30,
            'caregiver_phone_no': 31,
            'caregiver_id_no': 32,
        }

        return demographics

    def excel_service_uptake_data(self):
        return


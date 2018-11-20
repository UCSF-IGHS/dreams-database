import traceback
import unicodecsv as unicodecsv
import MySQLdb
import MySQLdb.cursors as cursors
from django.conf import settings


class DreamsRawExportTemplateRenderer(object):
    def __init__(self):
        pass

    def get_connection(self):
        database = settings.DATABASES['default']
        return MySQLdb.connect(
            host=database['HOST'], user=database['USER'],
            passwd=database['PASSWORD'], db=database['NAME'],
            cursorclass=cursors.DictCursor)

    def get_export_rows(self, ip_list_str, sub_county, ward):
        cursor = self.get_connection().cursor()

        multiple_ip_sub_county_query = "SELECT * FROM flat_dreams_enrollment WHERE voided=0 AND sub_county_code = %s AND  implementing_partner_id IN %s "
        multiple_ip_ward_query = "SELECT * FROM flat_dreams_enrollment WHERE voided=0 AND ward_id = %s AND  implementing_partner_id IN %s "
        multiple_ip_default_query = "SELECT * FROM flat_dreams_enrollment WHERE voided=0 AND implementing_partner_id IN %s "

        single_ip_sub_county_query = "SELECT * FROM flat_dreams_enrollment WHERE voided=0 AND sub_county_code = %s AND implementing_partner_id = %s "
        single_ip_ward_query = "SELECT * FROM flat_dreams_enrollment WHERE voided=0 AND ward_id = %s AND implementing_partner_id = %s "
        single_ip_default_query = "SELECT * FROM flat_dreams_enrollment WHERE voided=0 AND implementing_partner_id = %s "

        cursor_results = None

        try:
            ip_tuple_l = ip_list_str
            if sub_county is not None and sub_county:
                sub_county = int(sub_county)

            if ward is not None and ward:
                ward = int(ward)

            if len(ip_tuple_l) > 1:
                ip_list = tuple(ip_tuple_l)

                if ward is not None and ward:
                    cursor.execute(multiple_ip_ward_query, [ward, ip_list])
                elif sub_county is not None and sub_county:
                    cursor.execute(
                        multiple_ip_sub_county_query, [sub_county, ip_list])
                else:
                    cursor.execute(multiple_ip_default_query, [ip_list])
            else:
                ip_list = ip_list_str[0]
                if ward is not None and ward:
                    cursor.execute(single_ip_ward_query, [ward, ip_list])
                elif sub_county is not None and sub_county:
                    cursor.execute(single_ip_sub_county_query, [sub_county, ip_list])
                else:
                    cursor.execute(single_ip_default_query, [ip_list])
            return cursor

        except Exception as e:
            print 'There was an Error running the query\n'
            traceback.format_exc()
        return

    def fetch_intervention_rows(self, ip_list_str, sub_county, ward):
        cursor = self.get_connection().cursor()

        multiple_ip_sub_county_query = """select
  i.client_id, i.dreams_id, CONCAT_WS(" ",i.first_name, i.middle_name, i.last_name) AS client_name, i.date_of_birth, i.implementing_partner, i.implementing_partner_id, i.county_of_residence,i.sub_county,
  i.ward, i.village, i.date_of_enrollment as date_of_enrollment, DATE(i.intervention_date) date_of_intervention, DATE(i.date_created) date_created, i.intervention as intervention_type, i.intervention_category, i.hts_result,
  i.pregnancy_test_result, i.client_ccc_number, i.date_linked_to_ccc,
  i.no_of_sessions_attended, i.comment, i.current_age, i.age_at_intervention
from stag_client_intervention i WHERE voided=0 AND i.sub_county_id = %s AND i.implementing_partner_id IN %s """

        multiple_ip_ward_query = """select
  i.client_id, i.dreams_id, CONCAT_WS(" ",i.first_name, i.middle_name, i.last_name) AS client_name, i.date_of_birth, i.implementing_partner,  i.implementing_partner_id,i.county_of_residence,i.sub_county,
  i.ward, i.village, i.date_of_enrollment as date_of_enrollment, DATE(i.intervention_date) date_of_intervention, DATE(i.date_created) date_created, i.intervention as intervention_type, i.intervention_category, i.hts_result,
  i.pregnancy_test_result, i.client_ccc_number, i.date_linked_to_ccc,
  i.no_of_sessions_attended, i.comment, i.current_age, i.age_at_intervention
from stag_client_intervention i WHERE voided=0 AND i.ward_id = %s AND i.implementing_partner_id IN %s """


        multiple_ip_default_query = """select
  i.client_id, i.dreams_id, CONCAT_WS(" ",i.first_name, i.middle_name, i.last_name) AS client_name, i.date_of_birth, i.implementing_partner,  i.implementing_partner_id,i.county_of_residence,i.sub_county,
  i.ward, i.village, i.date_of_enrollment as date_of_enrollment, DATE(i.intervention_date) date_of_intervention, DATE(i.date_created) date_created, i.intervention as intervention_type, i.intervention_category, i.hts_result,
  i.pregnancy_test_result, i.client_ccc_number, i.date_linked_to_ccc,
  i.no_of_sessions_attended, i.comment, i.current_age, i.age_at_intervention
from stag_client_intervention i WHERE voided=0 AND i.implementing_partner_id IN %s """

        single_ip_sub_county_query = """select
  i.client_id, i.dreams_id, CONCAT_WS(" ",i.first_name, i.middle_name, i.last_name) AS client_name, i.date_of_birth, i.implementing_partner,  i.implementing_partner_id,i.county_of_residence,i.sub_county,
  i.ward, i.village, i.date_of_enrollment as date_of_enrollment, DATE(i.intervention_date) date_of_intervention, DATE(i.date_created) date_created, i.intervention as intervention_type, i.intervention_category, i.hts_result,
  i.pregnancy_test_result, i.client_ccc_number, i.date_linked_to_ccc,
  i.no_of_sessions_attended, i.comment, i.current_age, i.age_at_intervention
from stag_client_intervention i WHERE voided=0 AND i.sub_county_id = %s AND i.implementing_partner_id = %s """


        single_ip_ward_query = """select
  i.client_id, i.dreams_id, CONCAT_WS(" ",i.first_name, i.middle_name, i.last_name) AS client_name, i.date_of_birth, i.implementing_partner,  i.implementing_partner_id,i.county_of_residence,i.sub_county,
  i.ward, i.village, i.date_of_enrollment as date_of_enrollment, DATE(i.intervention_date) date_of_intervention, DATE(i.date_created) date_created, i.intervention as intervention_type, i.intervention_category, i.hts_result,
  i.pregnancy_test_result, i.client_ccc_number, i.date_linked_to_ccc,
  i.no_of_sessions_attended, i.comment, i.current_age, i.age_at_intervention
from stag_client_intervention i WHERE voided=0 AND i.ward_id = %s AND i.implementing_partner_id = %s """


        single_ip_default_query = """select
  i.client_id, i.dreams_id, CONCAT_WS(" ",i.first_name, i.middle_name, i.last_name) AS client_name, i.date_of_birth, i.implementing_partner,  i.implementing_partner_id,i.county_of_residence,i.sub_county,
  i.ward, i.village, i.date_of_enrollment as date_of_enrollment, DATE(i.intervention_date) date_of_intervention, DATE(i.date_created) date_created, i.intervention as intervention_type, i.intervention_category, i.hts_result,
  i.pregnancy_test_result, i.client_ccc_number, i.date_linked_to_ccc,
  i.no_of_sessions_attended, i.comment, i.current_age, i.age_at_intervention
from stag_client_intervention i
WHERE voided=0 AND i.implementing_partner_id = %s """

        try:
            ip_tuple_l = ip_list_str
            if sub_county is not None and sub_county:
                sub_county = int(sub_county)

            if ward is not None and ward:
                ward = int(ward)

            if len(ip_tuple_l) > 1:
                ip_list = tuple(ip_tuple_l)

                if ward is not None and ward:
                    cursor.execute(multiple_ip_ward_query, [ward, ip_list])
                elif sub_county is not None and sub_county:
                    cursor.execute(
                        multiple_ip_sub_county_query, [sub_county, ip_list])
                else:
                    cursor.execute(multiple_ip_default_query, [ip_list])
            else:
                ip_list = ip_list_str[0]
                if ward is not None and ward:
                    cursor.execute(single_ip_ward_query, [ward, ip_list])
                elif sub_county is not None and sub_county:
                    cursor.execute(single_ip_sub_county_query, [sub_county, ip_list])
                else:
                    cursor.execute(single_ip_default_query, [ip_list])
            return cursor

        except Exception as e:
            raise e
        return

    def extract_service_layering_for_all_girls(self, ip_list_str, sub_county, ward):

        cursor = self.get_connection().cursor()
        multiple_ip_sub_county_query = "SELECT * FROM stag_individual_client_service_layering WHERE sub_county_id = %s AND  implementing_partner_id IN %s "
        multiple_ip_ward_query = "SELECT * FROM stag_individual_client_service_layering WHERE ward_id = %s AND  implementing_partner_id IN %s "
        multiple_ip_default_query = "SELECT * FROM stag_individual_client_service_layering WHERE implementing_partner_id IN %s "

        single_ip_sub_county_query = "SELECT * FROM stag_individual_client_service_layering WHERE sub_county_id = %s AND implementing_partner_id = %s "
        single_ip_ward_query = "SELECT * FROM stag_individual_client_service_layering WHERE ward_id = %s AND implementing_partner_id = %s "
        single_ip_default_query = "SELECT * FROM stag_individual_client_service_layering WHERE implementing_partner_id = %s "

        try:
            ip_tuple_l = ip_list_str
            if sub_county is not None and sub_county:
                sub_county = int(sub_county)

            if ward is not None and ward:
                ward = int(ward)

            if len(ip_tuple_l) > 1:
                ip_list = tuple(ip_tuple_l)

                if ward is not None and ward:
                    cursor.execute(multiple_ip_ward_query, [ward, ip_list])
                elif sub_county is not None and sub_county:
                    cursor.execute(
                        multiple_ip_sub_county_query, [sub_county, ip_list])
                else:
                    cursor.execute(multiple_ip_default_query, [ip_list])
            else:
                ip_list = ip_list_str[0]
                if ward is not None and ward:
                    cursor.execute(single_ip_ward_query, [ward, ip_list])
                elif sub_county is not None and sub_county:
                    cursor.execute(single_ip_sub_county_query, [sub_county, ip_list])
                else:
                    cursor.execute(single_ip_default_query, [ip_list])

            print "Query for individual service layering data was successful"
            return cursor

        except Exception as e:
            raise e
        return

    def prepare_enrolment_export_doc(self, response, ip_list_str, sub_county, ward, show_PHI):
        try:
            cursor_data = self.get_export_rows(ip_list_str, sub_county, ward)
            col_names = [x[0] for x in cursor_data.description]

            if not show_PHI:
                phi_cols = ['first_name', 'middle_name', 'last_name', 'verification_doc_no', 'phone_number',
                            'dss_id_number', 'guardian_name', 'guardian_phone_number', 'guardian_national_id']
                col_names = list(set(col_names) - set(phi_cols))

            writer = unicodecsv.DictWriter(response, fieldnames=col_names, extrasaction='ignore')
            writer.writeheader()

            for row in cursor_data:
                writer.writerow(row)

        except Exception as e:
           raise e
        return

    def get_intervention_excel_doc(self, response, ip_list_str, sub_county, ward, show_PHI):

        try:
            cursor_data = self.fetch_intervention_rows(ip_list_str, sub_county, ward)
            col_names = [x[0] for x in cursor_data.description]

            if not show_PHI:
                phi_cols = ['client_name']
                col_names = list(set(col_names) - set(phi_cols))

            writer = unicodecsv.DictWriter(response, fieldnames=col_names, extrasaction='ignore')
            writer.writeheader()

            for row in cursor_data:
                writer.writerow(row)

        except Exception as e:
            raise e
        return

    def get_individual_layering_report(self, response, ip_list_str, sub_county, ward, show_PHI):

        try:
            cursor_data = self.extract_service_layering_for_all_girls(ip_list_str, sub_county, ward)
            col_names = [x[0] for x in cursor_data.description]

            if not show_PHI:
                phi_cols = ['first_name', 'middle_name', 'last_name']
                col_names = list(set(col_names) - set(phi_cols))

            writer = unicodecsv.DictWriter(response, fieldnames=col_names, extrasaction='ignore')
            writer.writeheader()

            for row in cursor_data:
                writer.writerow(row)

        except Exception as e:
            raise e
        return

    def get_intervention_excel_transferred_in_doc(self, response, ip, from_intervention_date, to_intervention_date, show_PHI):

        try:
            cursor_data = self.fetch_intervention_transferred_in_rows(ip, from_intervention_date, to_intervention_date)
            col_names = [x[0] for x in cursor_data.description]

            if not show_PHI:
                phi_cols = ['first_name', 'middle_name', 'last_name']
                col_names = list(set(col_names) - set(phi_cols))

            writer = unicodecsv.DictWriter(response, fieldnames=col_names, extrasaction='ignore')
            writer.writeheader()

            for row in cursor_data:
                writer.writerow(row)

        except Exception as e:
            raise e
        return

    def fetch_intervention_transferred_in_rows(self, ip, from_intervention_date, to_intervention_date):
        cursor = self.get_connection().cursor()

        query = """select
          i.client_id, i.dreams_id, CONCAT_WS(" ",i.first_name, i.middle_name, i.last_name) AS client_name, i.date_of_birth, 
          i.implementing_partner,  i.implementing_partner_id,i.county_of_residence,i.sub_county,
          i.ward, i.village, i.date_of_enrollment as date_of_enrollment, DATE(i.intervention_date) date_of_intervention, 
          DATE(i.date_created) date_created, i.intervention as intervention_type, i.intervention_category, i.hts_result,
          i.pregnancy_test_result, i.client_ccc_number, i.date_linked_to_ccc,
          i.no_of_sessions_attended, i.comment, i.current_age, i.age_at_intervention
          from stag_client_intervention i
          WHERE i.voided=0 AND i.transferred_client=1 
          """
        params = []

        if ip is not None:
            query += " AND i.implementing_partner_id = %s "
            params.append(ip.id)
        if from_intervention_date is not None and from_intervention_date:
            query += " AND i.intervention_date >= %s "
            params.append(from_intervention_date)
        if to_intervention_date is not None and to_intervention_date:
            query += " AND i.intervention_date <= %s "
            params.append(to_intervention_date)

        try:
            cursor.execute(query, params)
            print "Query was successful"
            return cursor

        except Exception as e:
            print 'There was an Error running the query: {} \n'.format(e)
            traceback.format_exc()

        return

import unicodecsv as unicodecsv
import MySQLdb
import MySQLdb.cursors as cursors
import logging
from django.conf import settings
from datetime import datetime
from DreamsApp.constants import RAW_ENROLMENT_EXPORT_COLUMNS, RAW_INTERVENTION_EXPORT_COLUMNS, \
    INDIVIDUAL_CLIENT_SERVICE_LAYERING_COLUMNS, INTERVENTION_TRANSFERRED_IN_COLUMNS


class DreamsRawExportTemplateRenderer(object):
    def __init__(self):
        pass

    def get_connection(self):
        database = settings.DATABASES['default']
        return MySQLdb.connect(
            host=database['HOST'], user=database['USER'],
            passwd=database['PASSWORD'], db=database['NAME'],
            port=int(database['PORT']),
            cursorclass=cursors.DictCursor)

    def get_export_rows(self, ip_list, county, sub_county, ward, from_date, to_date):
        cursor = self.get_connection().cursor()

        multiple_ip_county_query = "SELECT {} FROM flat_dreams_enrollment WHERE voided=0 AND county_of_residence_id = %s AND implementing_partner_id IN %s ".format(RAW_ENROLMENT_EXPORT_COLUMNS)
        multiple_ip_county_query = self.get_query_string_with_enrollment_date_filters(multiple_ip_county_query, from_date, to_date)

        multiple_ip_sub_county_query = "SELECT {} FROM flat_dreams_enrollment WHERE voided=0 AND sub_county_code = %s AND implementing_partner_id IN %s ".format(RAW_ENROLMENT_EXPORT_COLUMNS)
        multiple_ip_sub_county_query = self.get_query_string_with_enrollment_date_filters(multiple_ip_sub_county_query, from_date, to_date)

        multiple_ip_ward_query = "SELECT {} FROM flat_dreams_enrollment WHERE voided=0 AND ward_id = %s AND implementing_partner_id IN %s ".format(RAW_ENROLMENT_EXPORT_COLUMNS)
        multiple_ip_ward_query = self.get_query_string_with_enrollment_date_filters(multiple_ip_ward_query, from_date, to_date)

        multiple_ip_default_query = "SELECT {} FROM flat_dreams_enrollment WHERE voided=0 AND implementing_partner_id IN %s ".format(RAW_ENROLMENT_EXPORT_COLUMNS)
        multiple_ip_default_query = self.get_query_string_with_enrollment_date_filters(multiple_ip_default_query, from_date, to_date)

        single_ip_county_query = "SELECT {} FROM flat_dreams_enrollment WHERE voided=0 AND county_of_residence_id = %s AND implementing_partner_id = %s ".format(RAW_ENROLMENT_EXPORT_COLUMNS)
        single_ip_county_query = self.get_query_string_with_enrollment_date_filters(single_ip_county_query, from_date, to_date)

        single_ip_sub_county_query = "SELECT {} FROM flat_dreams_enrollment WHERE voided=0 AND sub_county_code = %s AND implementing_partner_id = %s ".format(RAW_ENROLMENT_EXPORT_COLUMNS)
        single_ip_sub_county_query = self.get_query_string_with_enrollment_date_filters(single_ip_sub_county_query, from_date, to_date)

        single_ip_ward_query = "SELECT {} FROM flat_dreams_enrollment WHERE voided=0 AND ward_id = %s AND implementing_partner_id = %s ".format(RAW_ENROLMENT_EXPORT_COLUMNS)
        single_ip_ward_query = self.get_query_string_with_enrollment_date_filters(single_ip_ward_query, from_date, to_date)

        single_ip_default_query = "SELECT {} FROM flat_dreams_enrollment WHERE voided=0 AND implementing_partner_id = %s ".format(RAW_ENROLMENT_EXPORT_COLUMNS)
        single_ip_default_query = self.get_query_string_with_enrollment_date_filters(single_ip_default_query, from_date, to_date)

        try:
            county = int(county) if county else None
            sub_county = int(sub_county) if sub_county else None
            ward = int(ward) if ward else None

            if len(ip_list) > 1:
                ip_list = tuple(ip_list)

                if ward:
                    cursor.execute(multiple_ip_ward_query, [ward, ip_list])
                elif sub_county:
                    cursor.execute(
                        multiple_ip_sub_county_query, [sub_county, ip_list])
                elif county:
                    cursor.execute(multiple_ip_county_query, [county, ip_list])
                else:
                    cursor.execute(multiple_ip_default_query, [ip_list])
            else:
                ip_list = ip_list[0]
                if ward:
                    cursor.execute(single_ip_ward_query, [ward, ip_list])
                elif sub_county:
                    cursor.execute(single_ip_sub_county_query, [sub_county, ip_list])
                elif county:
                    cursor.execute(single_ip_county_query, [county, ip_list])
                else:
                    cursor.execute(single_ip_default_query, [ip_list])
            return cursor

        except Exception as e:
            logging.error(
                "Exception {} {} ".format(e, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            raise e

    def fetch_intervention_rows(self, ip_list, county, sub_county, ward, from_date, to_date):
        
        cursor = self.get_connection().cursor()

        multiple_ip_county_query = "SELECT {} FROM stag_client_intervention i WHERE voided=0 AND i.county_of_residence_id = %s AND i.current_implementing_partner_id IN %s ".format(RAW_INTERVENTION_EXPORT_COLUMNS)
        multiple_ip_county_query = self.get_query_string_with_intervention_date_filters(multiple_ip_county_query, from_date, to_date)

        multiple_ip_sub_county_query = "SELECT {} FROM stag_client_intervention i WHERE voided=0 AND i.sub_county_id = %s AND i.current_implementing_partner_id IN %s ".format(RAW_INTERVENTION_EXPORT_COLUMNS)
        multiple_ip_sub_county_query = self.get_query_string_with_intervention_date_filters(multiple_ip_sub_county_query, from_date, to_date)

        multiple_ip_ward_query = "SELECT {} FROM stag_client_intervention i WHERE voided=0 AND i.ward_id = %s AND i.current_implementing_partner_id IN %s ".format(RAW_INTERVENTION_EXPORT_COLUMNS)
        multiple_ip_ward_query = self.get_query_string_with_intervention_date_filters(multiple_ip_ward_query, from_date, to_date)

        multiple_ip_default_query = "SELECT {} FROM stag_client_intervention i WHERE voided=0 AND i.current_implementing_partner_id IN %s ".format(RAW_INTERVENTION_EXPORT_COLUMNS)
        multiple_ip_default_query = self.get_query_string_with_intervention_date_filters(multiple_ip_default_query, from_date, to_date)

        single_ip_county_query = "SELECT {} FROM stag_client_intervention i WHERE voided=0 AND i.county_of_residence_id = %s AND i.current_implementing_partner_id = %s ".format(RAW_INTERVENTION_EXPORT_COLUMNS)
        single_ip_county_query = self.get_query_string_with_intervention_date_filters(single_ip_county_query, from_date, to_date)

        single_ip_sub_county_query = "SELECT {} FROM stag_client_intervention i WHERE voided=0 AND i.sub_county_id = %s AND i.current_implementing_partner_id = %s ".format(RAW_INTERVENTION_EXPORT_COLUMNS)
        single_ip_sub_county_query = self.get_query_string_with_intervention_date_filters(single_ip_sub_county_query, from_date, to_date)

        single_ip_ward_query = "SELECT {} FROM stag_client_intervention i WHERE voided=0 AND i.ward_id = %s AND i.current_implementing_partner_id = %s ".format(RAW_INTERVENTION_EXPORT_COLUMNS)
        single_ip_ward_query = self.get_query_string_with_intervention_date_filters(single_ip_ward_query, from_date, to_date)

        single_ip_default_query = "SELECT {} FROM stag_client_intervention i WHERE voided=0 AND i.current_implementing_partner_id = %s ".format(RAW_INTERVENTION_EXPORT_COLUMNS)
        single_ip_default_query = self.get_query_string_with_intervention_date_filters(single_ip_default_query, from_date, to_date)

        try:
            county = int(county) if county else None
            sub_county = int(sub_county) if sub_county else None
            ward = int(ward) if ward else None

            if len(ip_list) > 1:
                ip_list = tuple(ip_list)

                if ward:
                    cursor.execute(multiple_ip_ward_query, [ward, ip_list])
                elif sub_county:
                    cursor.execute(
                        multiple_ip_sub_county_query, [sub_county, ip_list])
                elif county:
                    cursor.execute(multiple_ip_county_query, [county, ip_list])
                else:
                    cursor.execute(multiple_ip_default_query, [ip_list])
            else:
                ip_list = ip_list[0]
                if ward:
                    cursor.execute(single_ip_ward_query, [ward, ip_list])
                elif sub_county:
                    cursor.execute(single_ip_sub_county_query, [sub_county, ip_list])
                elif county:
                    cursor.execute(single_ip_county_query, [county, ip_list])
                else:
                    cursor.execute(single_ip_default_query, [ip_list])
            return cursor

        except Exception as e:
            raise e

    def extract_service_layering_for_all_girls(self, ip_list, county, sub_county, ward, from_date, to_date):

        cursor = self.get_connection().cursor()
        multiple_ip_county_query = "SELECT {} FROM stag_individual_client_service_layering_intervention_date WHERE county_of_residence_id = %s AND  implementing_partner_id IN %s ".format(INDIVIDUAL_CLIENT_SERVICE_LAYERING_COLUMNS)
        multiple_ip_county_query = self.get_query_string_with_intervention_date_filters(multiple_ip_county_query, from_date, to_date)

        multiple_ip_sub_county_query = "SELECT {} FROM stag_individual_client_service_layering_intervention_date WHERE sub_county_id = %s AND  implementing_partner_id IN %s ".format(INDIVIDUAL_CLIENT_SERVICE_LAYERING_COLUMNS)
        multiple_ip_sub_county_query = self.get_query_string_with_intervention_date_filters(multiple_ip_sub_county_query, from_date, to_date)

        multiple_ip_ward_query = "SELECT {} FROM stag_individual_client_service_layering_intervention_date WHERE ward_id = %s AND  implementing_partner_id IN %s ".format(INDIVIDUAL_CLIENT_SERVICE_LAYERING_COLUMNS)
        multiple_ip_ward_query = self.get_query_string_with_intervention_date_filters(multiple_ip_ward_query, from_date, to_date)

        multiple_ip_default_query = "SELECT {} FROM stag_individual_client_service_layering_intervention_date WHERE implementing_partner_id IN %s ".format(INDIVIDUAL_CLIENT_SERVICE_LAYERING_COLUMNS)
        multiple_ip_default_query = self.get_query_string_with_intervention_date_filters(multiple_ip_default_query, from_date, to_date)

        single_ip_county_query = "SELECT {} FROM stag_individual_client_service_layering_intervention_date WHERE county_of_residence_id = %s AND implementing_partner_id = %s ".format(INDIVIDUAL_CLIENT_SERVICE_LAYERING_COLUMNS)
        single_ip_county_query = self.get_query_string_with_intervention_date_filters(single_ip_county_query, from_date, to_date)

        single_ip_sub_county_query = "SELECT {} FROM stag_individual_client_service_layering_intervention_date WHERE sub_county_id = %s AND implementing_partner_id = %s ".format(INDIVIDUAL_CLIENT_SERVICE_LAYERING_COLUMNS)
        single_ip_sub_county_query = self.get_query_string_with_intervention_date_filters(single_ip_sub_county_query, from_date, to_date)

        single_ip_ward_query = "SELECT {} FROM stag_individual_client_service_layering_intervention_date WHERE ward_id = %s AND implementing_partner_id = %s ".format(INDIVIDUAL_CLIENT_SERVICE_LAYERING_COLUMNS)
        single_ip_ward_query = self.get_query_string_with_intervention_date_filters(single_ip_ward_query, from_date, to_date)

        single_ip_default_query = "SELECT {} FROM stag_individual_client_service_layering_intervention_date WHERE implementing_partner_id = %s ".format(INDIVIDUAL_CLIENT_SERVICE_LAYERING_COLUMNS)
        single_ip_default_query = self.get_query_string_with_intervention_date_filters(single_ip_default_query, from_date, to_date)

        try:
            county = int(county) if county else None
            sub_county = int(sub_county) if sub_county else None
            ward = int(ward) if ward else None

            if len(ip_list) > 1:
                ip_list = tuple(ip_list)

                if ward:
                    cursor.execute(multiple_ip_ward_query, [ward, ip_list])
                elif sub_county:
                    cursor.execute(
                        multiple_ip_sub_county_query, [sub_county, ip_list])
                elif county:
                    cursor.execute(multiple_ip_county_query, [county, ip_list])
                else:
                    cursor.execute(multiple_ip_default_query, [ip_list])
            else:
                ip_list = ip_list[0]
                if ward:
                    cursor.execute(single_ip_ward_query, [ward, ip_list])
                elif sub_county:
                    cursor.execute(single_ip_sub_county_query, [sub_county, ip_list])
                elif county:
                    cursor.execute(single_ip_county_query, [county, ip_list])
                else:
                    cursor.execute(single_ip_default_query, [ip_list])

            return cursor

        except Exception as e:
            raise e

    def prepare_enrolment_export_doc(self, response, ip_list_str, county, sub_county, ward, show_PHI, from_date, to_date):
        try:
            cursor_data = self.get_export_rows(ip_list_str, county, sub_county, ward, from_date, to_date)
            col_names = [x[0] for x in cursor_data.description]

            if not show_PHI:
                phi_cols = ['first_name', 'middle_name', 'last_name', 'verification_doc_no', 'phone_number',
                            'dss_id_number', 'guardian_name', 'guardian_phone_number', 'guardian_national_id']
                col_names = [item for item in col_names if item not in phi_cols]

            writer = unicodecsv.DictWriter(response, fieldnames=col_names, extrasaction='ignore')
            writer.writeheader()

            for row in cursor_data:
                writer.writerow(row)

        except Exception as e:
           raise e
        return

    def get_intervention_export_doc(self, response, ip_list_str, county, sub_county, ward, show_PHI, from_date, to_date):

        try:
            cursor_data = self.fetch_intervention_rows(ip_list_str, county, sub_county, ward, from_date, to_date)
            col_names = [x[0] for x in cursor_data.description]

            if not show_PHI:
                phi_cols = ['client_name']
                col_names = [item for item in col_names if item not in phi_cols]

            writer = unicodecsv.DictWriter(response, fieldnames=col_names, extrasaction='ignore')
            writer.writeheader()

            for row in cursor_data:
                writer.writerow(row)

        except Exception as e:
            raise e
        return

    def get_individual_export_doc(self, response, ip_list_str, county, sub_county, ward, show_PHI, from_date, to_date):

        try:
            cursor_data = self.extract_service_layering_for_all_girls(ip_list_str, county, sub_county, ward, from_date, to_date)
            col_names = [x[0] for x in cursor_data.description]

            if not show_PHI:
                phi_cols = ['first_name', 'middle_name', 'last_name']
                col_names = [item for item in col_names if item not in phi_cols]

            writer = unicodecsv.DictWriter(response, fieldnames=col_names, extrasaction='ignore')
            writer.writeheader()

            for row in cursor_data:
                writer.writerow(row)

        except Exception as e:
            raise e
        return

    def get_intervention_transferred_in_doc(self, response, ip, from_intervention_date, to_intervention_date, show_PHI):

        try:
            cursor_data = self.fetch_intervention_transferred_in_rows(ip, from_intervention_date, to_intervention_date)
            col_names = [x[0] for x in cursor_data.description]

            if not show_PHI:
                phi_cols = ['first_name', 'middle_name', 'last_name']
                col_names = [item for item in col_names if item not in phi_cols]

            writer = unicodecsv.DictWriter(response, fieldnames=col_names, extrasaction='ignore')
            writer.writeheader()

            for row in cursor_data:
                writer.writerow(row)

        except Exception as e:
            raise e
        return

    def fetch_intervention_transferred_in_rows(self, ip, from_intervention_date, to_intervention_date):
        cursor = self.get_connection().cursor()
        query = "SELECT {} FROM stag_client_intervention i WHERE i.voided=0 AND i.transferred_client=1".format(INTERVENTION_TRANSFERRED_IN_COLUMNS)
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
            return cursor

        except Exception as e:
            raise e


    def get_query_string_with_enrollment_date_filters(self, query_string, start_date, end_date):

        if start_date and end_date:
            query_string += 'AND date_of_enrollment BETWEEN "{}" AND "{}"'.format(start_date, end_date)
        elif start_date and not end_date:
            query_string += 'AND date_of_enrollment > "{}"'.format(start_date)
        elif not start_date and end_date:
            query_string += 'AND date_of_enrollment < "{}"'.format(end_date)
        return query_string

    def get_query_string_with_intervention_date_filters(self, query_string, start_date, end_date):

        if start_date and end_date:
            query_string += 'AND intervention_date BETWEEN "{}" AND "{}"'.format(start_date, end_date)
        elif start_date and not end_date:
            query_string += 'AND intervention_date > "{}"'.format(start_date)
        elif not start_date and end_date:
            query_string += 'AND intervention_date < "{}"'.format(end_date)
        return query_string


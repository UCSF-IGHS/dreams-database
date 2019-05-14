import sys
import MySQLdb
import MySQLdb.cursors as cursors
from typing import TextIO

file_cols = (
    'Dreams ID',
    'First Name',
    'Last Name',
    'IP',
)

conn_params = {
    'NAME': 'dreams_local_env',
    'USER': 'root',
    'PASSWORD':"reambi1000!",
    'HOST':'localhost',
    'PORT':'3306',
}

TRANSFER_COMPLETED_STATUS = 2

INSERT_CLIENT_TRANSFER_TRANSFER_QUERY = 'INSERT INTO DreamsApp_clienttransfer ( client_id, start_date, date_created, \
                            transfer_reason, completed_by_id, destination_implementing_partner_id, initiated_by_id, \
                            source_implementing_partner_id, transfer_status_id ) SELECT c.id, now( ), now( ), \
                            "{}", {}, {}, {}, {}, {} FROM DreamsApp_client c WHERE c.dreams_id \
                            in ({})'

UPDATE_CLIENTS_TRANSFER_QUERY = 'UPDATE DreamsApp_client c SET c.implementing_partner_id = {} ' \
                                'WHERE c.dreams_id in ({}); '


class TransferClients:

    def __init__(self):
        pass

    def initialize_params(self, params: list) -> dict:
        return {
            'transfer_file_path' : params[1],
            'source_ip_id': params[2],
            'destination_ip_id': params[3],
            'transfer_reason': params[4],
            'client_performing_transfer_id': params[5],
        }

    def validate_dreams_ids(self, conn: cursors, file: TextIO, has_header: bool = True) -> bool:
        if has_header:
            self.validate_header(file, file_cols, has_header)
        return self.validate_clients(conn, file, has_header)

    def connect(self, params: dict) -> cursors:
        return MySQLdb.connect(
            host=params['HOST'], user=conn_params['USER'],
            passwd=params['PASSWORD'], db=conn_params['NAME'],
            port=int(params['PORT']),
            cursorclass=cursors.DictCursor)

    def load_file(self, path: str) -> TextIO:
        return open(path, "r")

    def validate_header(self, file: TextIO, file_cols: tuple, has_header: bool) -> None:
        if has_header:
            header = str(file.readline())
            if hash(header[:-1].upper()) != hash(','.join(file_cols).upper()):
                raise Exception('Invalid header columns')

    def validate_clients(self, conn: cursors, file: TextIO, has_header: bool) -> tuple:
        validated_dreams_ids = []
        file.seek(0)
        lines = file.readlines()[1:] if has_header else file.readlines()
        for line in lines:
            db_line = self.get_db_line(conn, line.split(',')[0]).fetchone()
            if sorted(line.upper()[:-1]) == sorted(
                    ','.join([str(value) for value in db_line.values() if value is not None]).upper()):
                validated_dreams_ids.append(line.split(',')[0])
            else:
                raise Exception('Invalid record for {}'.format(line.split(',')[0]))
        return tuple(validated_dreams_ids)

    def get_db_line(self, conn: cursors, dreams_id: str) -> str:
        query = 'SELECT dreams_id, first_name, last_name, implementing_partner_id \
                  FROM DreamsApp_client WHERE dreams_id = "{}"'.format(dreams_id)
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor

    def transfer_clients(self, conn: cursors, dreams_ids: tuple, user_initiating_transfer: int, source_ip: str,
                         destination_ip: str, transfer_reason: str) -> None:
        try:
            concatenated_dreams_ids = '"' + '","'.join(list(dreams_ids)) + '"'
            update_ip_query = INSERT_CLIENT_TRANSFER_TRANSFER_QUERY.format(transfer_reason, user_initiating_transfer,
                                                                           destination_ip, user_initiating_transfer,
                                                                           source_ip, TRANSFER_COMPLETED_STATUS,
                                                                           concatenated_dreams_ids)
            insert_into_transfers_query = UPDATE_CLIENTS_TRANSFER_QUERY.format(destination_ip, concatenated_dreams_ids)
            cursor = conn.cursor()
            cursor.execute(update_ip_query)
            cursor.execute(insert_into_transfers_query)
            conn.commit()
            print('Transfer completed')
        except MySQLdb.Error as e:
            print("Error. Performing rollback. {}".format(e))
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

transfer_clients = TransferClients()
params = transfer_clients.initialize_params(sys.argv)
conn = transfer_clients.connect(conn_params)
file = transfer_clients.load_file(params['transfer_file_path'])
dreams_ids = transfer_clients.validate_dreams_ids(conn, file)
transfer_clients.transfer_clients(conn, dreams_ids, params['client_performing_transfer_id'],
                                  params['source_ip_id'], params['destination_ip_id'], params['transfer_reason'])

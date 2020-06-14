import datetime
import sqlite3


conn = sqlite3.connect('Shipping_Units (2).db')
curs = conn.cursor()


class Shipment:
    """docstring for Shipment"""

    def __init__(self,
                 client,
                 width,
                 length,
                 height,
                 gross_weight,
                 purpose,
                 on_hand_number=None,
                 create_date=datetime.datetime.today().strftime('%Y-%m-%d'),
                 release_date=None,
                 mawb=None,
                 hawb=None):
        self.client = client
        self.width = width
        self.length = length
        self.height = height
        self.gross_weight = gross_weight
        self.purpose = purpose
        self.on_hand_number = on_hand_number
        self.create_date = create_date
        self.release_date = release_date
        self.mawb = mawb
        self.hawb = hawb

    def __str__(self):
        return (
            f'''
            This shipment belongs to client: {self.client}
            Dimensions: {self.width} x {self.length} x {self.height}
            Gross Weight: {self.gross_weight} lbs
            On Hand Number: {self.on_hand_number}
            Purpose: {self.purpose}
            Created on: {self.create_date}
            Released on: {self.release_date}
            '''
        )

    def volume_weight(self):
        return str(round(
            (self.width * self.length * self.height) / 366, 1)) + " kg/vol"

    def lbs_to_kg(self):
        return round(self.gross_weight / 2.204)

    def add_shipment(self):
        curs.execute(
            'INSERT INTO shipments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                self.on_hand_number, self.client, self.width, self.length,
                self.height, self.gross_weight, self.purpose,
                self.create_date, self.release_date, self.mawb, self.hawb)
        )
        return conn.commit()

    def delete_shipment(self):
        curs.execute('DELETE FROM shipments WHERE on_hand_number = ?', (
            self.on_hand_number,))
        return conn.commit()

    def update_shipment(self, client, width, length,
                        height, gross_weight, purpose):
        curs.execute(
            '''
            UPDATE shipments
            SET client = ?,
            width = ?,
            length = ?,
            height = ?,
            gross_weight = ?,
            purpose = ?
            WHERE on_hand_number = ?
            ''', (client, width, length, height, gross_weight, purpose,
                  self.on_hand_number))
        return conn.commit()

    def release_shipment(self, MAWB, HAWB):
        curs.execute(
            '''
            UPDATE shipments
            SET release_date = ?,
            MAWB = ?,
            HAWB = ?
            WHERE on_hand_number = ?
            ''', (datetime.datetime.today().strftime('%Y-%m-%d'),
                  MAWB, HAWB, self.on_hand_number))
        return conn.commit()

    def add_to_consolidation(self, MAWB, HAWB):
        curs.execute(
            '''
            UPDATE shipments
            SET MAWB = ?,
            HAWB = ?,
            WHERE on_hand_number = ?
            ''', (MAWB, HAWB, self.on_hand_number))
        return conn.commit()

    def update_MAWB(self, MAWB, HAWB, unit_count,
                    gross_weight, volume_weight, date):
        curs.execute(
            '''
            INSERT INTO consols VALUES ?, ?, ?, ?, ?, ?
            ''', (MAWB, HAWB, unit_count, gross_weight, volume_weight, date))
        return conn.commit()

    @staticmethod
    def fetch_all_records(quantity=50):
        curs.execute(
            'SELECT * FROM shipments ORDER BY create_date DESC LIMIT ?',
            (quantity,)
        )
        return curs.fetchall()

    @staticmethod
    def shipment_count():
        curs.execute('SELECT * FROM shipments')
        return len(curs.fetchall())

    @staticmethod
    def find_one_record(on_hand_number):
        curs.execute('SELECT * FROM shipments WHERE on_hand_number = ?',
                     (on_hand_number,))
        param = curs.fetch()
        return Shipment(*param)

    @staticmethod  # decorator for export to csv?
    def fetch_all_records_in_date(first_date, second_date):
        curs.execute(
            'SELECT * FROM shipments WHERE create_date BETWEEN ? AND ?',
                    (first_date, second_date)
        )
        return curs.fetchall()

    @staticmethod
    def view_all_units_inhouse():
        curs.execute('SELECT * FROM shipments WHERE release_date IS NULL')
        return curs.fetchall()

    @staticmethod
    def view_mawbs():
        curs.execute('SELECT * FROM consols')
        return curs.fetchall()


if __name__ == '__main__':
    test = Shipment('TSB', 48, 40, 60, 460, 'Export', 10003)
    test2 = Shipment('Gems', 48, 40, 60, 400, 'Export', 10004)
    print(test)
    print(test.volume_weight())
    test.add_shipment()
    test2.add_shipment()
    conn.close()

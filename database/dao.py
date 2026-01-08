from database.DB_connect import DBConnect
from model.stato import Stato
class DAO:
    @staticmethod
    def get_anni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT YEAR(s_datetime) as anno FROM sighting WHERE YEAR(s_datetime)>=1910 AND YEAR(s_datetime)<=2014 ORDER BY anno asc """

        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_forme(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT shape FROM sighting WHERE YEAR(s_datetime)=%s"""

        cursor.execute(query,(anno,))

        for row in cursor:
            if row["shape"]:
                result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM state"""

        cursor.execute(query)

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_archi_stati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT state1,state2
                    FROM neighbor 
                    WHERE state1<state2"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["state1"],row["state2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_pesi(anno,forma):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT upper(state) as id, count(*) as n
                    FROM sighting
                    WHERE YEAR(s_datetime)=%s AND shape=%s
                    GROUP BY state"""

        cursor.execute(query,(anno,forma,))

        for row in cursor:
            result[row["id"]] = row["n"]

        cursor.close()
        conn.close()
        return result







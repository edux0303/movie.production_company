from database.DB_connect import DBConnect
from model.casa import Casa

class DAO:
    @staticmethod
    def getNodi(anno, minimo):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT m.production_company AS nome,
                          COUNT(DISTINCT m.id) AS numero,
                          SUM(r.total_votes) AS voti
                   FROM movie m, ratings r
                   WHERE m.id = r.movie_id
                     AND m.year = %s
                     AND m.production_company IS NOT NULL
                   GROUP BY m.production_company
                   HAVING COUNT(DISTINCT m.id) >= %s"""
        cursor.execute(query, (anno, minimo))
        for row in cursor:
            result.append(Casa(row["nome"], row["numero"], int(row["voti"])))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getCoppia(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
        SELECT DISTINCT m.production_company AS nome, g.genre AS genre
        FROM movie m, genre g
        WHERE g.movie_id = m.id AND m.year = %s  AND m.production_company IS NOT NULL 
        """
        cursor.execute(query,(anno,))
        for row in cursor:
            result.append((row["nome"], row["genre"]))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT year AS anno
                   FROM movie
                   ORDER BY year"""
        cursor.execute(query)
        for row in cursor:
            result.append(row["anno"])
        cursor.close()
        cnx.close()
        return result

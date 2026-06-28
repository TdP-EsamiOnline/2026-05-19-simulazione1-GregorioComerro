from database.DB_connect import DBConnect
from model.artist import Artist
from model.genere import Genere


class DAO():

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from Genre g"

        cursor.execute(query)

        for row in cursor:
            results.append(Genere(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(idGenre):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId, a.Name 
                    from Artist a , Album al, Track t 
                    where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId 
                    and t.GenreId = %s"""

        cursor.execute(query, (idGenre,))

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(idGenre):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct ar1.ArtistId as id1, ar2.ArtistId as id2
                    from Invoice i1, InvoiceLine il1, Track t1, Album a1, Artist ar1,
                         Invoice i2, InvoiceLine il2, Track t2, Album a2, Artist ar2
                    where i1.InvoiceId = il1.InvoiceId
                    and i1.CustomerId = i2.CustomerId 
                    and il1.TrackId = t1.TrackId 
                    and t1.AlbumId = a1.AlbumId 
                    and a1.ArtistId = ar1.ArtistId 
                    and i2.InvoiceId = il2.InvoiceId
                    and il2.TrackId = t2.TrackId 
                    and t2.AlbumId = a2.AlbumId 
                    and a2.ArtistId = ar2.ArtistId 
                    and ar1.ArtistId < ar2.ArtistId 
                    and t1.GenreId = %s
                    and t2.GenreId = %s"""

        cursor.execute(query, (idGenre, idGenre))

        for row in cursor:
            results.append((row["id1"], row["id2"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPopularities(idGenre):
        conn = DBConnect.get_connection()
        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """
            select ar.ArtistId, count(*) as popolarita
            from Artist ar, Album al, Track t, InvoiceLine il, Invoice i
            where ar.ArtistId = al.ArtistId
            and al.AlbumId = t.AlbumId
            and t.TrackId = il.TrackId
            and il.InvoiceId = i.InvoiceId
            and t.GenreId = %s
            group by ar.ArtistId
            order by popolarita  desc
        """

        cursor.execute(query, (idGenre,))

        for row in cursor:
            results[row["ArtistId"]] = row["popolarita"]

        cursor.close()
        conn.close()
        return results
from database.DB_connect import DBConnect
from model.actor import Actor

class DAO():

    # PUNTO 1 ----------------------------------------------------------
    # L’utente seleziona dal corrispondente menù a tendina un range di rating  (tabella Ratings).
    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select distinct(r.avg_rating)
                    from ratings r 
                    order by r.avg_rating"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return result
    # FINE PUNTO 1 ------------------------------------------------------

    # PUNTO 2 ----------------------------------------------------------
    # I vertici sono gli attori che hanno recitato nei film che
    # hanno ricevuto una valutazione nel range definito dall’utente
    @staticmethod
    def getAllActorsByRange(rating1, rating2):
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select distinct rm.name_id  as ActorID,  n.name as Name, n.date_of_birth as birth_date
                    from names n , ratings r , role_mapping rm , movie m 
                    where r.avg_rating >= %s
                    and r.avg_rating <= %s
                    and m.id = rm.movie_id
                    and m.id = r.movie_id 
                    and n.id = rm.name_id 
                    and n.date_of_birth  is not null"""

        cursor.execute(query, (rating1, rating2,))

        for row in cursor:
            result.append(Actor(**row))

        cursor.close()
        conn.close()
        return result

    #  Esiste un arco tra due attori se hanno recitato almeno in uno stesso film.
    #  Il peso è pari alla somma degli incassi dei film in comune.
    @staticmethod
    def getAllEdges(rating1, rating2):

        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select rm1.name_id as Actor1, rm2.name_id as Actor2, sum( cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned)) as Weight
                    from movie m, role_mapping rm1, role_mapping rm2, ratings r, names n1, names n2
                    where m.id = rm1.movie_id
                    and m.id = rm2.movie_id
                    and m.id = r.movie_id
                    and rm1.name_id = n1.id
                    and rm2.name_id = n2.id
                    and n1.date_of_birth IS NOT NULL
                    and n2.date_of_birth IS NOT NULL
                    and rm1.name_id < rm2.name_id
                    and r.avg_rating >= %s
                    and r.avg_rating <= %s
                    and m.worlwide_gross_income is not null
                    and m.worlwide_gross_income like '$%'
                    group by rm1.name_id, rm2.name_id"""

        cursor.execute(query, (rating1, rating2,))

        for row in cursor:
            result.append((row["Actor1"], row["Actor2"], row["Weight"]))

        cursor.close()
        conn.close()
        return result

    """
    - Estrazione (SELECT): Restituisce l'ID del primo attore (Actor1), l'ID del secondo attore (Actor2) e 
    la somma degli incassi dei loro film in comune (Weight).

    - Pulizia Dati (CAST/REPLACE): Converte il testo dell'incasso (es. "$ 12,156") in un numero intero, rimuovendo il 
    simbolo $ e le virgole per poter eseguire la somma.

    - Incrocio Dati (JOIN): Collega le tabelle dei film, dei voti, dei ruoli e dei nomi per trovare i film in cui i due
     attori hanno recitato insieme.

    - Filtri Applicati (WHERE): Considera solo attori con data di nascita registrata.
    Evita i duplicati e l'auto-accoppiamento (grazie a rm1.name_id < rm2.name_id).
    Filtra i film in base a un voto medio minimo e massimo (%s).
    Considera solo i film con incasso valido in dollari.
    
    - Raggruppamento (GROUP BY): Unisce i dati per coppia di attori, in modo che se hanno fatto più film insieme, 
    il loro incasso totale viene sommato in un'unica riga.
    """


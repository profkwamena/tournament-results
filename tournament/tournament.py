import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a db connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the db."""
    conn = connect()
    cursor = conn.cursor()
    return cursor.execute("truncate table match;")


def deletePlayers():
    """Remove all the player records from the db."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("truncate table players cascade;")
    return conn.commit()


def countPlayers():
    """Returns how many players registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select count(*) from players")
    result = cursor.fetchone()
    return result[0]   


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The db names a unique serial id number for the player.  (This
    could be handled by your SQL database scheme, its not handled by Python.)
  
    
      name: The players name doesnt have to be unique.
    """
    conn = connect()
    cursor = conn.cursor()
    name_sanitized = name.replace("'","''")
    cursor.execute("insert into players (name) values (%s);", (name_sanitized,))
    return conn.commit()


def playerStandings():
    """Returns a list of the players and their different win stats.

    The first name on the list should be a player with a win or two players who are tied.

    Returns:
      A list of tuples which should contain the players name their id and how many matches they have won or lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select * from player_standings;")
    result = cursor.fetchall()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into match (winner, loser) values (%s, %s);", (winner, loser,))
    return conn.commit()

 
def swissPairings():
    """This should return a list of players for the next match    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select id, name from player_standings order by wins desc;")
    rows = cursor.fetchall()
    pairings_list = []
    if (len(rows) > 1):
        count = 0
        for row in rows:
            if (count < 1):
                id1 = row[0]
                name1 = row[1]
                count += 1
            else:
                id2 = row[0]
                name2 = row[1]
                pairings_list.append([id1, name1, id2, name2])
                count = 0

    return [tuple(list) for list in pairings_list]

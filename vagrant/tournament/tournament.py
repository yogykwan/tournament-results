#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    d = connect()
    c = d.cursor()
    c.execute('delete from matches;')
    d.commit()
    d.close()


def deletePlayers():
    """Remove all the player records from the database."""
    d = connect()
    c = d.cursor()
    c.execute('delete from players;')
    d.commit()
    d.close()


def countPlayers():
    """Returns the number of players currently registered."""
    d = connect()
    c = d.cursor()
    c.execute('select count(*) from players;')
    res = c.fetchone()
    d.close()
    return res[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    d = connect()
    c = d.cursor()
    c.execute('insert into players (name) values (%s);', (name,))
    d.commit()
    d.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    d = connect()
    c = d.cursor()
    
    # get # of wins of each player
    query_wins = """
        select players.id, players.name, count(matches.id) as wins
        from players left join matches on players.id = matches.winner
        group by players.id
        """
    
    # get # of matches of each player
    query_matches ="""
        select players.id, count(matches.id) as matches
        from players left join matches on players.id = matches.winner or players.id = matches.loser
        group by players.id
        """

    # join wins and matches into one table
    query_join = """
        select query_wins.id, name, wins, matches
        from ({query_wins}) as query_wins join ({query_matches}) as query_matches on query_wins.id = query_matches.id
        order by wins desc
        """.format(query_wins = query_wins, query_matches = query_matches)
    c.execute(query_join)
    res = c.fetchall()
    d.close()
    return res


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    d = connect()
    c = d.cursor()
    c.execute('insert into matches (winner, loser) values ({winner}, {loser});'.format(winner = winner, loser = loser))
    d.commit()
    d.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairs = []
    players = playerStandings()
    cnt = countPlayers()
    for i in range(0, cnt, 2):
        pairs.append((players[i][0], players[i][1], players[i + 1][0], players[i + 1][1]))
    return pairs


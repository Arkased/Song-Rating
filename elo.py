# -*- coding: utf-8 -*-

def _expected(A, B):
    """
    Calculate expected score of A in a match against B
    :param A: Elo rating for player A
    :param B: Elo rating for player B
    """
    return 1 / (1 + 10 ** ((B - A) / 400))


def _elo(old, exp, score, k=32):
    """
    Calculate the new Elo rating for a player
    :param old: The previous Elo rating
    :param exp: The expected score for this match
    :param score: The actual score for this match
    :param k: The k-factor for Elo (default: 32)
    """
    return old + int(k * (score - exp))

def update(song1, song2, score, k=32):
    expA = _expected(song1.elo, song2.elo)
    expB = 1 - expA
    
    song1.elo = _elo(song1.elo, expA, score, k)
    song2.elo = _elo(song2.elo, expB, 1-score, k)
    
# -*- coding: utf-8 -*-

_n = 400


def _expected(a, b):
    """
    Calculate expected score of a in a match against b
    :param a: Elo rating for player a
    :param b: Elo rating for player b
    """
    q_a = _q(a)
    q_b = _q(b)
    return q_a / (q_a + q_b)


def _q(a):
    """
    Calculates the relative expected score, which can be understood as absolute power.
    :param a: Elo rating of some player
    :return: q-value
    """
    return 10 ** (a / _n)


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
    """
    Updates the elos of song1 and song2 after match between song1 and song2
    :param song1: first song
    :param song2: second song
    :param score: score of song1, 0 for loss 1 for win
    :param k: weight of the match
    :return: void
    """
    assert 0 <= score <= 1

    exp_a = _expected(song1.elo, song2.elo)
    exp_b = 1 - exp_a
    
    song1.elo = _elo(song1.elo, exp_a, score, k)
    song2.elo = _elo(song2.elo, exp_b, 1-score, k)
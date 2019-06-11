# -*- coding: utf-8 -*-
from song import Song

_n = 400
_BONUS_BASE = 3 ** .5


def _expected(a, b):
	"""
	Calculate expected score of a in a match against b
	:param a: Elo rating for player a
	:param b: Elo rating for player b
	:return: expected score of a
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
	:return: the new elo
	"""
	return old + int(k * (score - exp))


def update(song_a: Song, song_b: Song, score, min_k=20):
	"""
	Updates the elos of song1 and song_b after match between song1 and song_b
	:param song_a: first song
	:param song_b: second song
	:param score: score of song1, 0 for loss 1 for win
	:param min_k: minimum weight of the match, to be scaled up by abnormal performance
	"""
	assert 0 <= score <= 1

	k_a = min_k * _BONUS_BASE ** abs(song_a.calc_perf_z())
	k_b = min_k * _BONUS_BASE ** abs(song_b.calc_perf_z())
	print("k:", k_a, k_b)

	exp_a = _expected(song_a.elo, song_b.elo)
	exp_b = 1 - exp_a

	song_a.elo = _elo(song_a.elo, exp_a, score, k_a)
	song_b.elo = _elo(song_b.elo, exp_b, 1 - score, k_b)

	song_a.update_recent(exp_a, score)
	song_b.update_recent(exp_b, 1 - score)

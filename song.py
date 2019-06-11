# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 18:43:07 2019

@author: kevin
"""


class Song:
	INIT_ELO = 1200

	def __init__(self, name, artist, elo=INIT_ELO, recent_total_prob=None, recent_score=0, num_recent=0):
		self.elo = elo
		self.artist = artist
		self.name = name
		self.recent_total_prob = recent_total_prob
		self.recent_score = recent_score
		self.num_recent = num_recent

	def __lt__(self, other):
		return self.elo < other.elo

	def args(self):
		return self.name + ',' + self.artist + ',' + str(self.elo)

	def __repr__(self):
		return 'Song(' + self.name + ', ' + self.artist + ', ' + str(self.elo) + ')'

	def __str__(self):
		return self.name + ' by ' + self.artist  # + ' (' + str(self.elo) + ')'

	def update_recent(self, p, score):
		if self.recent_total_prob is None:
			self.recent_total_prob = p
			self.recent_score = score
			self.num_recent = 1
		else:
			self.recent_total_prob += p
			self.recent_score += score
			self.num_recent += 1

	def reset_recent(self):
		self.recent_total_prob = None
		self.recent_score = 0
		self.num_recent = 0

	def calc_perf_z(self):
		if self.recent_total_prob is None:
			return 0

		n = self.num_recent
		mu = self.recent_total_prob
		p = mu / n
		x = self.recent_score
		q = 1 - p

		print(x, mu)

		return (x - mu) / (n * p * q) ** .5

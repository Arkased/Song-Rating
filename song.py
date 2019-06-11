# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 18:43:07 2019

@author: kevin
"""


class Song:
	INIT_ELO = 1200
	NUM_TRACKED_RECENT = 10

	def __init__(self, name, artist, elo=INIT_ELO):
		self.elo = int(elo)
		self.artist = artist
		self.name = name
		self.recent_total_prob = []
		self.recent_score = []
		self.num_recent = 0

	def __lt__(self, other):
		return self.elo < other.elo

	def __repr__(self):
		return 'Song(' + self.name + ', ' + self.artist + ', ' + str(self.elo) + ')'

	def __str__(self):
		return self.name + ' by ' + self.artist  # + ' (' + str(self.elo) + ')'

	def update_recent(self, p, score):
		"""
		Updates tracked recent matches, removing the oldest one if limit is reached.
		:param p: probability of winning (float in range [0,1])
		:param score: actual score
		"""
		assert 0 <= self.num_recent <= self.NUM_TRACKED_RECENT

		if not self.recent_total_prob:
			self.recent_total_prob = [p]
			self.recent_score = [score]
			self.num_recent = 1
			return

		# Remove oldest if limit is reached
		if self.num_recent == self.NUM_TRACKED_RECENT:
			self.recent_total_prob = self.recent_total_prob[1:]
			self.recent_score = self.recent_score[1:]
			self.num_recent -= 1
		self.recent_total_prob.append(p)
		self.recent_score.append(score)
		self.num_recent += 1

	def reset_recent(self):
		"""
		Resets tracked recent matches, removing all.
		"""
		self.recent_total_prob = []
		self.recent_score = []
		self.num_recent = 0

	def calc_perf_z(self):
		"""
		Calculates the z-score of recent matches, using total score and the normal distribution to approximate
		repeated matches.
		:return: z-score
		"""
		if not self.recent_total_prob:
			return 0

		n = self.num_recent
		mu = sum(self.recent_total_prob)
		p = mu / n
		x = sum(self.recent_score)
		q = 1 - p

		return (x - mu) / (n * p * q) ** .5

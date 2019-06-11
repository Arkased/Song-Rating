# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 18:48:43 2019

@author: kevin
"""

from csv import reader, writer
from song import Song
import numpy as np
from elo import update

_MIN_K = 20
DEFAULT_FILE = 'songs.csv'
COMPETE_RANGE = 20  # all_songs can compete against other all_songs within +-COMPETE_RANGE/2 places


def import_songs(file=DEFAULT_FILE):
	"""
	Imports songs from a .csv file. Format should be song_name, artist, elo_rating with no header columns. I used
	http://www.playlist-converter.net/ to convert my Spotify playlist into the desired format, after manually removing
	the header row and quotes.
	:param file: .csv file from which to import
	"""
	global all_songs
	with open(file, newline='\n', encoding='utf-8') as csvfile:
		inp = list(reader(csvfile))

	all_songs = [Song(*row) for row in inp if row]
	all_songs.sort()


def export_songs(file=DEFAULT_FILE, print_output=False):
	"""
	Exports songs to a .csv file, sorted based on rating (ascending) with new ratings. Overwrites files.
	:param file: .csv file onto which to write
	:param print_output: whether or not to print the array to console
	"""
	song_data = [[song.name, song.artist, str(song.elo)] for song in all_songs]
	if print_output:
		print(song_data)
	with open(file, 'w', newline='\n', encoding='utf-8') as f:
		write = writer(f)
		write.writerows(song_data)


def raterate():
	"""
	Rates songs by comparing each to a neighbor (defined based on constant COMPETE_RANGE).
	"""
	while True:
		i1 = int(np.random.random() * num_songs)
		i2 = i1 + int(((np.random.random() - .5) * COMPETE_RANGE))
		_check_indecies(i1, i2)


def raterate_fixed(song1):
	"""
	Rates a fixed song against its neighbors.
	:param song1: song to rate
	"""
	while True:
		i1 = all_songs.index(song1)
		i2 = i1 + int(((np.random.random() - .5) * COMPETE_RANGE))

		_check_indecies(i1, i2)


def raterate_min_percentile(percentile: float):
	"""
	Rates songs above a certain percentile.
	:param percentile:
	:return:
	"""
	assert 0 <= percentile <= 100

	scale_factor = 1 - percentile / 100
	new_range = num_songs * scale_factor
	shift = num_songs * percentile / 100

	while True:
		i1 = int(np.random.random() * new_range + shift)
		i2 = i1 + int(((np.random.random() - .5) * int(COMPETE_RANGE * scale_factor)))

		_check_indecies(i1, i2)


def _check_indecies(i1: int, i2: int):
	"""
	Checks to ensure the indecies for comparison are different (different songs) and within range.
	:param i1: first index
	:param i2: second index
	"""
	if i2 < 0 or i2 >= num_songs:
		return

	if i1 == i2:
		# Edge cases
		if i1 == 0:
			i2 += 1
		elif i1 + 1 == num_songs:
			i2 -= 1
		# General case
		elif np.random.random() > .5:
			i2 += 1
		else:
			i2 -= 1
	_compare(all_songs[i1], all_songs[i2])


def _compare(song1: Song, song2: Song):
	"""
	Compares two songs, printing their names to console and adjusting their ratings based on input.
	:param song1: first song
	:param song2: second song
	"""
	print(song1)
	print('vs.')
	print(song2)

	update(song1, song2, _get_input(), _MIN_K)
	print('Elo:', song1.elo, song2.elo)
	print()

	all_songs.remove(song1)
	all_songs.remove(song2)
	_insert([song1, song2])


def _get_input():
	"""
	Function to handle input from console. Handles invalid input and exits on 'e'.
	:return: valid input, a float in the interval [0,1], or none of exits
	"""
	inp = input()
	if inp == 'e':
		export_songs()
		raise SystemExit
	if inp == '2':
		inp = '0'
	try:
		score = float(inp)
		assert 0 <= score <= 1
		return score
	except (ValueError, AssertionError):
		print("invalid input, type 'e' to exit")
		return _get_input()


def _insert(songs: list):
	"""
	Inserts a collection elements into all_songs, updating all_songs.
	:param songs: elements to insert
	"""
	global all_songs
	songs.sort()

	list_a = all_songs[::-1]
	list_b = songs[::-1]
	new_list = []

	while list_a and list_b:
		if list_a[-1] < list_b[-1]:
			new_list.append(list_a.pop())
		else:
			new_list.append(list_b.pop())

	if list_a:
		new_list.extend(list_a[::-1])
	else:
		new_list.extend(list_b[::-1])

	all_songs = new_list


import_songs()
num_songs = len(all_songs)
# raterate()

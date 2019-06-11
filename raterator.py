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
COMPETE_RANGE = 10  # all_songs can compete against other all_songs within +-COMPETE_RANGE/2 places


def import_songs(file=DEFAULT_FILE):
	global all_songs
	with open(file, newline='\n', encoding='utf-8') as csvfile:
		inp = list(reader(csvfile))

	all_songs = [Song(row[0], row[1], int(row[2])) for row in inp]


def export_songs(file=DEFAULT_FILE, print_output=True):
	song_data = [[song.name, song.artist, str(song.elo)] for song in all_songs]
	if print_output:
		print(song_data)
	with open(file, 'w', newline='\n', encoding='utf-8') as f:
		write = writer(f)
		write.writerows(song_data)


def _get_input():
	inp = input()
	if inp == 'e':
		# export_songs()
		raise SystemExit
	if inp == '2':
		inp = '0'
	try:
		score = float(inp)
		assert 0 <= score <= 1
		return score
	except ValueError or AssertionError:
		print("invalid inp")
		return _get_input()


def compare(song1: Song, song2: Song):
	print(song1)
	print('vs.')
	print(song2)

	update(song1, song2, _get_input(), _MIN_K)
	print('Elo:', song1.elo, song2.elo)
	print()

	all_songs.delete(song1)
	all_songs.delete(song2)
	insert([song1, song2])


def insert(songs: list):
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


def raterate():
	i1 = int(np.random.random() * num_songs)
	i2 = i1 + int(((np.random.random() - .5) * COMPETE_RANGE))

	if i1 != i2 and 0 <= i2 < num_songs:
		compare(all_songs[i1], all_songs[i2])

	raterate()


def raterate_fixed(song1: Song):
	i1 = all_songs.index(song1)
	i2 = i1 + int(((np.random.random() - .5) * COMPETE_RANGE))

	if i1 != i2 and 0 <= i2 < num_songs:
		compare(song1, all_songs[i2])

	raterate_fixed(song1)


import_songs()
all_songs = [2, 4, 6, 8, 10]
num_songs = len(all_songs)
# raterate()

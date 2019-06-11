# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 18:48:43 2019

@author: kevin
"""

from csv import reader, writer
from song import Song
import numpy as np
from elo import update

k = 22  # to be removed
DEFAULT_FILE = 'songs.csv'
COMPETE_RANGE = 10  # songs can compete against other songs within +-COMPETE_RANGE/2 places


def import_songs(file=DEFAULT_FILE):
    global songs
    with open(file, newline='\n', encoding='utf-8') as csvfile:
        inp = list(reader(csvfile))

    songs = [Song(row[0], row[1], int(row[2])) for row in inp]


def export_songs(file=DEFAULT_FILE, print_output=True):
    song_data = [[song.name, song.artist, str(song.elo)] for song in songs]
    if print_output:
        print(song_data)
    with open(file, 'w', newline='\n', encoding='utf-8') as f:
        write = writer(f)
        write.writerows(song_data)


def raterate():
    inp = ''
    while inp != 's':
        i1 = int(np.random.random() * num_songs)
        i2 = i1 + int(((np.random.random() - .5) * COMPETE_RANGE))
        if i2 < 0:
            i2 = 0
        elif i2 >= num_songs:
            i2 = num_songs - 1
        if i1 != i2:
            song1 = songs[i1]
            song2 = songs[i2]

            print(song1)
            print('vs.')
            print(song2)

            update(song1, song2, _get_input(), k)
            print(song1.elo)
            print(song2.elo)
            songs.sort()


def _get_input():
    inp = input()
    if inp == 'k':  # to be removed
        print('k=?')
        global k
        k = int(input())
        return _get_input()
    if inp == 'e':
        export_songs()
        raise SystemExit
    if inp == '2':
        inp = '0'
    try:
        score = float(inp)
        assert 0 <= inp <= 1
        return score
    except ValueError or AssertionError:
        print("invalid inp")
        return _get_input()


import_songs()
num_songs = len(songs)
raterate()

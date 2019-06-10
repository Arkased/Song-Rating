# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 18:48:43 2019

@author: kevin
"""

from csv import reader, writer
from song import Song
import numpy as np
from elo import update

k = 22
DEFAULT_FILE = 'songs.csv'
DELTA = 10
def import_songs(file=DEFAULT_FILE):
    with open(file, newline = '\n', encoding='utf-8') as csvfile:
        inp = list(reader(csvfile))
    
    return [Song(row[0], row[1], int(row[2])) for row in inp]

def export_songs(file=DEFAULT_FILE):
    song_data = [[song.name, song.artist, str(song.elo)] for song in songs]
    print(song_data)
    with open(file, 'w', newline = '\n', encoding='utf-8') as f:
        write = writer(f)
        write.writerows(song_data)
    #np.savetxt(file, song_data, delimiter = ",", newline = '\n', encoding='utf-8')

#songs = import_songs()
num_songs = len(songs)

#i1 = int(.8 * num_songs)
#song1 = songs[i1]
def raterate():
    inp = ''
    while inp != 's':
        global song1
        i1 = int(np.random.random() * num_songs)
        #i1 = songs.index(song1)
        i2 = i1 + int(((np.random.random() - .5) * DELTA))
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
            update(song1, song2, get_input(), k)
            print(song1.elo)
            print(song2.elo)
            songs.sort()
        
def get_input():
    inp = input()
    if inp == 'k':
        print('k=?')
        global k
        k = int(input())
        return get_input()
    if inp == 'e':
        export_songs()
        raise Exception('exiting')
    if inp == '2':
        inp = '0'
    inp = float(inp)
    assert 0 <= inp <= 1
    return inp
    
def clean(song):
    song.name = song.name.replace(',', '')
    song.artist = song.artist.replace(',', '')
    return song
    
raterate()
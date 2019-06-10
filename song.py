# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 18:43:07 2019

@author: kevin
"""

from elo import update

class Song:
    
    INIT_ELO = 1200
    
    def __init__(self, name, artist, elo = INIT_ELO):
        self.elo = elo
        self.artist = artist
        self.name = name
        
    def __lt__(self, other):
        return self.elo < other.elo
    
    def args(self):
        return self.name + ',' + self.artist + ',' + str(self.elo)
    
    def __repr__(self):
        return 'Song(' + self.name + ', ' + self.artist + ', ' + str(self.elo) + ')'
    
    def __str__(self):
        return self.name + ' by ' + self.artist #+ ' (' + str(self.elo) + ')'
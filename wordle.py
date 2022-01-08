#%%
########################
### IMPORT LIBRARIES ###
########################
import pandas as pd
import numpy as np
import time

#%%
#################
### WORD FREQ ###
#################

# Import dictionary of word frequencies 
word_freq = pd.read_json('word_freq.json',typ='series').to_frame().reset_index()
word_freq['word_len'] = word_freq['index'].str.len()
word_freq.columns = ['word', 'freq', 'word_len']
word_freq = word_freq[word_freq.word_len == 5.0]

# Scale word frequency to a value between 0 and 1
a, b = 0, 1
x, y = word_freq.freq.min(), word_freq.freq.max()
word_freq['freq_norm'] = (word_freq.freq - x) / (y - x) * (b - a) + a
word_freq['word'] = word_freq['word'].str.upper()

# %%
####################
### READ IN DATA ###
####################

info = True

# Read in CSV
scrabble_words = pd.read_csv('scrabble_dictionary.txt')
scrabble_words = scrabble_words[['Collins Scrabble Words (2019). 279']]
scrabble_words['word_len'] = scrabble_words['Collins Scrabble Words (2019). 279'].str.len()
scrabble_words.columns = ['word', 'word_len']
scrabble_words['key'] = 0

scrabble_words['word'] = scrabble_words['word']

# Subset Data to only 5 letter words
scrabble_words = scrabble_words[scrabble_words.word_len == 5.0]

# FOR THE FIRST RUN ONLY: 
# Get rid of the 10 worst letters, best performing of this group is 'BARES' for 5.01 avg on (5:1) ratio
if not info:
    scrabble_words = scrabble_words[~scrabble_words.word.str.contains('Z|Q|J|X|K|V|B|Y|W|G')]
    scrabble_words['1'] = scrabble_words['word'].str[0]
    scrabble_words['2'] = scrabble_words['word'].str[1]
    scrabble_words['3'] = scrabble_words['word'].str[2]
    scrabble_words['4'] = scrabble_words['word'].str[3]
    scrabble_words['5'] = scrabble_words['word'].str[4]
    scrabble_words = scrabble_words[scrabble_words['5'] != 'S']

## BEST WORD: SORES, if words not ending in S, BEST WORD: SIREE

####################################
### IF YOU HAVE WORD INFORMATION ###
####################################

if info: 
    scrabble_words['1'] = scrabble_words['word'].str[0]
    scrabble_words['2'] = scrabble_words['word'].str[1]
    scrabble_words['3'] = scrabble_words['word'].str[2]
    scrabble_words['4'] = scrabble_words['word'].str[3]
    scrabble_words['5'] = scrabble_words['word'].str[4]

    ### Green Tile
    scrabble_words = scrabble_words[scrabble_words['1'] == 'S']

    ### Yellow Tile
    scrabble_words = scrabble_words[scrabble_words.word.str.contains('A')]

    ### Grey/Yellow Tile 
    # If you know that no position is a certain letter
    scrabble_words = scrabble_words[~scrabble_words.word.str.contains('I')]
    # If you know only that a specific position is not a certain letter
    scrabble_words = scrabble_words[scrabble_words['1'] != 'T']

#%%
##################
### CROSS JOIN ###
##################

# Generate Cartesian Product
# This will generate a data where each row has, in separate columns, two words such that all pairs of two words get their own row
scrabble_words_cj = scrabble_words.merge(scrabble_words, on='key', how='outer')[['word_x', 'word_len_x', 'word_y']]
scrabble_words_cj.columns = ['word_x', 'word_len', 'word_y']

# For rapid development, shorten the dataset
# scrabble_words_cj = scrabble_words_cj.head(50)

# Separate out letters for word x - each letter is its own column
scrabble_words_cj['x1'] = scrabble_words_cj['word_x'].str[0]
scrabble_words_cj['x2'] = scrabble_words_cj['word_x'].astype(str).str[1]
scrabble_words_cj['x3'] = scrabble_words_cj['word_x'].astype(str).str[2]
scrabble_words_cj['x4'] = scrabble_words_cj['word_x'].astype(str).str[3]
scrabble_words_cj['x5'] = scrabble_words_cj['word_x'].astype(str).str[4]

# Same for word y
scrabble_words_cj['y1'] = scrabble_words_cj['word_y'].astype(str).str[0]
scrabble_words_cj['y2'] = scrabble_words_cj['word_y'].astype(str).str[1]
scrabble_words_cj['y3'] = scrabble_words_cj['word_y'].astype(str).str[2]
scrabble_words_cj['y4'] = scrabble_words_cj['word_y'].astype(str).str[3]
scrabble_words_cj['y5'] = scrabble_words_cj['word_y'].astype(str).str[4]

#%%
#######################
### CHECK FOR TILES ###
#######################

# Start timer
start = time.time()

# Check for Green Tiles
scrabble_words_cj['x1_green'] = np.where((scrabble_words_cj['x1'] == scrabble_words_cj['y1']), 1, 0)
scrabble_words_cj['x2_green'] = np.where((scrabble_words_cj['x2'] == scrabble_words_cj['y2']), 1, 0)
scrabble_words_cj['x3_green'] = np.where((scrabble_words_cj['x3'] == scrabble_words_cj['y3']), 1, 0)
scrabble_words_cj['x4_green'] = np.where((scrabble_words_cj['x4'] == scrabble_words_cj['y4']), 1, 0)
scrabble_words_cj['x5_green'] = np.where((scrabble_words_cj['x5'] == scrabble_words_cj['y5']), 1, 0)

scrabble_words_cj['num_unique_green'] = scrabble_words_cj['x1_green'] + scrabble_words_cj['x2_green'] + scrabble_words_cj['x3_green'] + scrabble_words_cj['x4_green'] + scrabble_words_cj['x5_green']

# Check for Yellow Tiles
scrabble_words_cj['x1_yellow'] = np.where((scrabble_words_cj['x1'] == scrabble_words_cj['y1']) | (scrabble_words_cj['x1'] == scrabble_words_cj['y2']) |(scrabble_words_cj['x1'] == scrabble_words_cj['y3']) | (scrabble_words_cj['x1'] == scrabble_words_cj['y4']) | (scrabble_words_cj['x1'] == scrabble_words_cj['y5']), scrabble_words_cj['x1'], '')
scrabble_words_cj['x2_yellow'] = np.where((scrabble_words_cj['x2'] == scrabble_words_cj['y1']) | (scrabble_words_cj['x2'] == scrabble_words_cj['y2']) |(scrabble_words_cj['x2'] == scrabble_words_cj['y3']) | (scrabble_words_cj['x2'] == scrabble_words_cj['y4']) | (scrabble_words_cj['x2'] == scrabble_words_cj['y5']), scrabble_words_cj['x2'], '')
scrabble_words_cj['x3_yellow'] = np.where((scrabble_words_cj['x3'] == scrabble_words_cj['y1']) | (scrabble_words_cj['x3'] == scrabble_words_cj['y3']) |(scrabble_words_cj['x3'] == scrabble_words_cj['y2']) | (scrabble_words_cj['x3'] == scrabble_words_cj['y4']) | (scrabble_words_cj['x3'] == scrabble_words_cj['y5']), scrabble_words_cj['x3'], '')
scrabble_words_cj['x4_yellow'] = np.where((scrabble_words_cj['x4'] == scrabble_words_cj['y1']) | (scrabble_words_cj['x4'] == scrabble_words_cj['y4']) |(scrabble_words_cj['x4'] == scrabble_words_cj['y2']) | (scrabble_words_cj['x4'] == scrabble_words_cj['y3']) | (scrabble_words_cj['x4'] == scrabble_words_cj['y5']), scrabble_words_cj['x4'], '')
scrabble_words_cj['x5_yellow'] = np.where((scrabble_words_cj['x5'] == scrabble_words_cj['y1']) | (scrabble_words_cj['x5'] == scrabble_words_cj['y5']) |(scrabble_words_cj['x5'] == scrabble_words_cj['y2']) | (scrabble_words_cj['x5'] == scrabble_words_cj['y3']) | (scrabble_words_cj['x5'] == scrabble_words_cj['y4']), scrabble_words_cj['x5'], '')
scrabble_words_cj['x1_yellow'] = np.where(scrabble_words_cj['x1_green'] < 1, scrabble_words_cj['x1_yellow'], '')
scrabble_words_cj['x2_yellow'] = np.where(scrabble_words_cj['x2_green'] < 1, scrabble_words_cj['x2_yellow'], '')
scrabble_words_cj['x3_yellow'] = np.where(scrabble_words_cj['x3_green'] < 1, scrabble_words_cj['x3_yellow'], '')
scrabble_words_cj['x4_yellow'] = np.where(scrabble_words_cj['x4_green'] < 1, scrabble_words_cj['x4_yellow'], '')
scrabble_words_cj['x5_yellow'] = np.where(scrabble_words_cj['x5_green'] < 1, scrabble_words_cj['x5_yellow'], '')

# Get unique letters that generate yellow tiles
scrabble_words_cj['unique_yellow'] = scrabble_words_cj['x1_yellow'] + scrabble_words_cj['x2_yellow'] + scrabble_words_cj['x3_yellow'] + scrabble_words_cj['x4_yellow'] + scrabble_words_cj['x5_yellow']
scrabble_words_cj['unique_yellow'] = scrabble_words_cj.unique_yellow.apply(lambda x: "".join(sorted(set(x))))

# Count number of unique yellow tiles 
scrabble_words_cj['num_unique_yellow']  = scrabble_words_cj['unique_yellow'].str.len()

#%%
######################
### WEIGHT RESULTS ###
######################
scrabble_words_cj['guess_strength'] = (5 * scrabble_words_cj['num_unique_green']) + (scrabble_words_cj['num_unique_yellow'])

# %%
#####################
### GROUP BY WORD ###
#####################
words_pointed = scrabble_words_cj.groupby('word_x')['guess_strength'].mean().reset_index()
words_pointed = words_pointed.merge(word_freq, left_on = 'word_x', right_on = 'word', how='left')
words_pointed['freq_norm'] = words_pointed['freq_norm'].fillna(words_pointed.freq_norm.min())

#%%
#####################################
### GENERATE WORD RECOMMENDATIONS ###
#####################################

words_pointed['guess_strength_plus_freq'] = words_pointed['guess_strength'] * words_pointed['freq_norm']
words_pointed.sort_values(by = 'guess_strength_plus_freq', ascending = False).head(25)

# If you want to ignore word frequencies run this
#words_pointed.sort_values(by = 'weighted_tile_avg', ascending = False).head(25)
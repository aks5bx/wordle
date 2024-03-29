# Wordle Solver

## Introduction

Wordle is a game that took the world by storm in early 2022. The game is quite simple, and was featured, and later added to, the New York Times. The game itself can be found online [here](https://www.nytimes.com/games/wordle/index.html). This repository contains my attempt at a data-driven solution to play Wordle! 

### Files 

- Python Code: `wordle.py`
- Scrabble Dictionary: `scrabble_dictionary.txt`
- Word Frequency Data: `word_freq.json`

## Game Background
The board interface is shown below:

<p align="center">
<img src="https://github.com/aks5bx/wordle/blob/main/wordle.png" width="350" height="500"/>
</p>

The rules to this game are quite simple. In fact, the Wordle website puts the rules quite succinctly, shown below:

<p align="center">
<img src="https://github.com/aks5bx/wordle/blob/main/wordlerules.png" width="550" height="600"/>
</p>

## How the Program Works 

### Overview 

The approach taken here is a "greedy" approach that treats each guess as its own bayesian-style optimization problem. General performance is noted in the Recommendation Strength section. The drawbacks of this approach are detailed in the Final Remarks section. 

The code for this project was finalized in early January of 2022. As such, many similar attempts available online were not taken into consideration nor built upon for this project. 

### Data Source 

The program is fed two datasets. One is a dataset of around 250,000 scrabble words and the other is a dataset of thousands of english words along with the number of appearances for those words in a selection of texts. 

### Pre-Processing 

This project required a fair amout of pre-processing in order to function. In fact, most of this project involves manipulating the data to get to a point where we could drive high-quality recommendations. To start off, I had a table of 250,000 words that had the following structure: 

Index | Word |
--- | ---
0 | ALPHA 
1 | BETA 
2 | GAMMA
3 | LAMBDA
4 | SIGMA

However, to make this dataset more usable, I had to make some modifications. I threw out any words that were not five letters long (the Wordle word is always 5 letters long) and also created a new field for each individual letter. The result of these modifications took this structure: 

Index | Word | 1 | 2 | 3 | 4 | 5 |
--- | --- | --- | --- | --- | --- | ---
0 | ALPHA | A | L | P | H | A 
2 | GAMMA | G | A | M | M | A
4 | SIGMA | S | I | G | M | A

Next, I utilized the CROSS-JOIN table join (or cartesian join) to create a new dataframe that had the following structure: 

Index | Word_X | x1 | x2 | x3 | x4 | x5 | Word_Y | y1 | y2 | y3 | y4 | y5 |
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
0 | ALPHA | A | L | P | H | A | GAMMA | G | A | M | M | A
1 | ALPHA | A | L | P | H | A | SIGMA | S | I | G | M | A
2 | GAMMA | G | A | M | M | A | ALPHA | A | L | P | H | A 
3 | GAMMA | G | A | M | M | A | SIGMA | S | I | G | M | A 
4 | SIGMA | S | I | G | M | A | ALPHA | A | L | P | H | A 
5 | SIGMA | S | I | G | M | A | GAMMA | G | A | M | M | A

With this structure, I was able to simulate a guess for the Wordle game. For example, index 0 represents guessing the word "alpha" when the mystery Wordle word was actually "gamma." From here, I was able to gather the yellow tiles, grey tiles, and green tiles that would have resulted from such a guess. In the example of guessing "alpha" for the mystery word "gamma" we would have a yellow tile in position 1, a grey tile in position 2, a grey tile in position 3, a grey tile in position 4, and a green tile in position 5. 

### Bayesian Statistics Approach

I took inspiration from bayesian statistics to approach this problem. Here, I treated each guess as a probability optimization problem with a prior and a known distribution. The prior represents the information gleaned from previous guesses. The known distribution represents the computed value of a guess given the prior. 

Let's continue the example from above, where our target word is GAMMA and our first guess is ALPHA. We make our first guess by selecting the word that gives us the most value given our prior. For our first guess, our prior is nothing. But for our second guess, we would select the word that yields the most value given the information provided to us from our first guess ALPHA (and the corresponding yellow, grey, and green tiles that result).  

### Generating Recommendations 

#### Initial Steps

The intuition behind generating recommendations was that if a word is a good guess for many words, that word is a good guess for an unknown word. In order to implement this intuition, I first generated a weighted average for how good a guess each word was. In order to do this I took the following steps:
- For each guess word-answer word pair of words, I calculated a score for how good of a guess the specific guess word was by taking an average of the number of yellow tiles and green tiles the guess generated (let's call this "Guess Strength")
- I grouped all of the scores by word so that for each word, I had the average Guess Strength for each word across all guess word-answer word pairs it was a part of 
- I then sorted all of the words by Guess Strength 

#### Weighting Green and Yellow Tiles

My initial attempt evenly weighted the value of a green and yellow tile. After some experimenting, I noticed that green tiles were actually more valuable in finding the mystery word than yellow tiles. So, I made a modification and told the bot to prioritize finding green tiles. I did this by simply adding a weight to the value of a green tile before calculating Guess Strength. 

#### Utilizing Information

At this point, I was able to generate a list of words that, on average, were good guesses for an unknown mystery word. However, after each guess, we receive valuable information from Wordle about our mystery word. This added information gets incorporated into our next guess as if we are updating a prior in some Bayesian computation. In order to factor that information in, I added a block of code to the beginning of my program to filter my list of words based on the information I received. For example, if I uncovered a green tile in position 1 using the letter 'T', I told my program to only consider words that had a 'T' in the first position. This ties into the Bayesian Statistics inspiration. We are continually updating our prior to zero in on our answer. 

#### Factoring in Word Frequencies 

Now, my program was able to solve some Wordle problems. However, I noticed that for one particular puzzle, it took the program more than the alloted six attempts to get to the correct answer. The reason this was happening was because the program was guessing incredible obscure words as its top guesses. The program does not think like a human, but the creator of Wordle does (people would be upset if the Wordle word was some word they had never heard of). In order to meet this reality, I imported a list of word frequencies into my program. I weighted Guess Strength by the frequency of the word - so even if a word generated a lot of yellow and green tiles, if it was an incredibly obscure word (unlikely to be the mystery word), it would get penalized. This significantly improved the performance. 

## Results & Discussion

### Recommendation Strength 

After trying this out for about a week or so, it seems that this program is able to solve the Wordle in about four tries (give or take). Specifically, taking a median of about 50 words gives us a median of four guesses until a success. 

The program is especially effective when unsual letters (v, j, etc) are introduced because this allows the program to significantly reduce the number of words it needs to consider. 

The program tends to struggle when unusual words with fairly common letters are the target word (this is not a five letter word, but an example of such a word could be _LYME_ with four reasonably common letters but an overall word that is not as common). 

### Lessons Learned 

- Contrary to some opinions on the internet, double lettering (the idea of using words that have repeat letters, like GORGE with a double G) is actually sometimes a good move (especially in cases where the letters are common letters like s, t, a, e, o, etc) because it increases the probability of getting a green tile
- Green tiles are huge - three green tiles gets you almost 99% of the way there to solving the word. I would say 1 green tile is worth roughly 2.5 yellow tiles just based off of my intuition
- Your starting word doesn’t matter that much! As long as it’s decent the starting word is actually not that big a deal, it’s mostly how you use the information (FWIW the program thinks the best first word is SORES - if you specify that the word does not end in 'S' the program likes SIREE)

### Final Remarks 

There are plenty of ways to make this programmatically more efficient. Notably, instead of trying to optimize some sort of point value determined by green and yellow tiles, one could train a model to guess many different target words to more accurately compute a generalizable and optimal optimization. I suspect that training a simple recurrent neural network with a BERT-based tokenizer and a loss function that minimizes the number of guesses would be quite effective. 

The key here is that instead of trying to maximize the probability of each guess being the correct target word, we would simply try to minimize the expected value of number of guesses. So, we could have a second guess that has a 0 probability of being the target word. But, that second guess could hypothetically set up a third guess with a 99% probability of being the target word. To contrast, the current method would not allow for such a second guess and instead it would prioritize a series of guesses where the probability of being the target word went, say, 20% --> 30% over the aforementioned 0% --> 99% (even though the probability of success after three guesses favors the 0 --> 99 approach).  

I don’t think this program “solves” Wordle. I think humans are generally better than this program (though a better program could change that) because Wordle is a human game by humans for humans. Given that the creator is a human who chooses human words, we have an advantage because we guess words that other humans know and use. I think the program gives interesting insights into the game though, but the mystery, in my opinion is still alive. 


## Links

- New York Times Profile: https://www.nytimes.com/2022/01/03/technology/wordle-word-game-creator.html
- Game: https://www.powerlanguage.co.uk/wordle/

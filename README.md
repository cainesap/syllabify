# Syllabify

Automatically convert plain text into phonemes (US English pronunciation) and syllabify.

Adapted from [the repository](https://github.com/anthonysgevans/syllabify) set up by Anthony Evans with some key changes, itemised below:

* Ported to Python 3 from Evans' Python 2 code;
* Correction of key onset and coda rules which affect consonant clusters and involve the 'maximise onsets principle';
* Removal of all ambisyllabicity from onset and coda rules, since it's not uncontroversial;
* Removal of 'test' (demo) option from syllable script.

Please see Anthony Evans' README file for a detailed background to the project.


## Set up

Requires [Python 3](https://www.python.org/downloads) (Anthony Evans used Python 2: if that's what you prefer, see his repo).

Refers to the [CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) of North American English word pronunciations. Version 0.7b was the current one at time of writing, but it throws a UnicodeDecodeError, so we're still using version 0.7a (amended to remove erroneous 'G' from SUGGEST and related words). Please see the dictionary download website to obtain the current version, add the `cmudict-N.nx(.phones|.symbols)*` files to the `CMU_dictionary` directory, remove the '.txt' suffixes, and update the line `VERSION = 'cmudict-n.nx'` in `cmuparser3.py`


## Usage

One word at a time:
```
python3 syllable3.py linguistics
```

Or several (space-separated):
```
python3 syllable3.py colourless green ideas
```

Or as preprocessing for the [wordseg](http://wordseg.readthedocs.io) program, `wordseg_prep' takes a [CHILDES](http://childes.talkbank.org) corpus (e.g. Brown) and syllabifies infant-directed speech (i.e. excluding CHI utterances) in phonemic format, with appropriate phone, syllable and word delimiters per wordseg defaults:
```
python3 wordseg_prep.py $CORPUSPATH
```


## Rules

1. If an onset contains a cluster of three consonants, the first consonant must be /S/.
2. /NG/ cannot appear in an onset
3. /V DH Z ZH/ cannot form part of onset clusters
4. /T D TH/ adjoined with /L/ cannot form an onset cluster
5. /H/ cannot appear in a coda
6. /LG/ is not a permissible coda cluster

Onset Maximalism ”Where there is a choice always assign as many consonants as
possible to the onset, and as few as possible to the coda. However, remember that
every word must also consist of a sequence of well formed syllables ”


## Output

For each transcribed word, the CMU dictionary returns a phoneme string that is not
partitioned into syllables. If we are to create a system that can compare phonological
units we will need to model the rules of syllabification.

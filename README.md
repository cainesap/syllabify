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


## Output

If the input word is found in the dictionary, a phonemic, syllabified transcript is returned. For example, for the word _linguistics_:
```
{o: L , n: IH [st:0 ln:short], c: NG }
{o: G W , n: IH [st:1 ln:short], c: empty}
{o: S T , n: IH [st:0 ln:short], c: K S }
```
There's one syllable per line. Each syllable is made up of an 'o' onset, 'n' nucleus, and 'c' coda. Phonemes are space-separated and capitalized in [ARPAbet](https://en.wikipedia.org/wiki/ARPABET) format. In line with phonological theory, the nucleus must have content, whereas the onset and coda may be empty. Within the vocalic content of the nucleus there's also an indication whether the syllable is stressed ('st':0 or 1), and whether the length ('ln') is short or long.


## Contact

If you have queries or feedback please contact `apc38` at `cam.ac.uk`

_Andrew Caines, September 2017_

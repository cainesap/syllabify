# syllabify
Automatically convert plain text into phonemes (US English pronunciation) and syllabify
# Syllabify

Syllabify partitions phoneme strings into syllables by modelling the rules of syllable
formation. The module implements Onset Maximalism and enforces the phonotactic rules of the English language. 

Syllabify can be tested from the command line by executing **syllable.py**. It will transcribe, and
return the syllable structure of 100 words chosen at random from a descriptive dictionary
packaged with this project.


## About Syllables

Words can be deconstructed into utterances, each utterance is a phone. Phones in turn can
be grouped into Consonant types and Vowel types. Vowels have a stress property and
can either carry primary stress, secondary stress or no stress. Vowels also have a length
property, they can either be long vowels like /AH/ in cat, or short vowels like /I/ in kit.

We can use a pronouncing dictionary to get a phonemic representation of a word. Carnegie
Melon University have produced an open source dictionary of North Amercian pronun-
ciations. The dictionary maps to over 125,000 phonemic transcriptions, and for some
entries contains multiple phonemic representations.

Consonants and vowels can group together to form a phonological unit called a syllable.
Syllables are formed of two parts: an onset and a rime. The rime of a syllable decom-
poses into two further parts: the nucleus and a coda.

The nucleus is the only mandatory part of the syllable and is usually accommodated by
a vowel. if the onset and coda sections exist they have to be occupied by consonants,
which can either be singular of exist in clusters of 2 or 3.

Under some conditions, there are certain combinations of consonants that cannot appear
in coda and onset. These rules are called phonotactic constraints:

1. If an onset contains a cluster of three consonants, the first consonant must be /S/.
2. /NG/ cannot appear in an onset
3. /V DH Z ZH/ cannot form part of onset clusters
4. /T D TH/ adjoined with /L/ cannot form an onset cluster
5. /H/ cannot appear in a coda
6. /LG/ is not a permissible coda cluster

Syllables must adhere to these rules if they to be well formed. A further principle that is used to partition a phoneme string into well formed syllables: Onset Maximalism:

Onset Maximalism ”Where there is a choice always assign as many consonants as
possible to the onset, and as few as possible to the coda. However, remember that
every word must also consist of a sequence of well formed syllables ”

For each transcribed word, the CMU dictionary returns a phoneme string that is not
partitioned into syllables. If we are to create a system that can compare phonological
units we will need to model the rules of syllabification.


## syllable.py

The syllable.py module has access to several data structures defined in syllable_types.py:
Syllable The public facing data container of the syllable data structure. It has getter
methods for onset, nucleus and coda Cluster objects as well as boolean methods to
test onset, nucleus and coda elements.

- **Rime** A constituent of the Syllable data object, the Rime class is a wrapper for the
nucleus and coda segment of the Syllable.

- **Cluster** The data container that holds groups raw Consonants and Vowels.
Consonant A wrapper for Consonant phoneme characters.

- **Vowel** A wrapper for Vowel phoneme characters.

- **Empty** Any syllable segments not populated with Consonants or Vowels are given in-
stantiations of the Empty class.

The syllable module has a method called factory that produces well-formed syllable
objects. factory defines three further sub-methods: phoneme_fact, cluster_fact and syllable fact. phoneme fact tokenizes a string of phoneme characters into appropriate Vowel
and Consonant Objects. cluster_fact combines Vowel and Consonant objects into groups
of like types, and syllable_fact models syllable forming rules adjusting the phonemic com-
position of Cluster Objects and assigning them to appropriate syllable regions.

The syllable.py module has one public method: generate(word) which takes as argument
a string word. The method retrieves a list of phoneme representations of the argument
word and maps the factory function to each phoneme string. The method returns a list
of well-formed Syllable objects.

The syllable module can be executed from the command line. 

## cmuparser.py

The CMU dictionary is used to transcribe words into their phoneme representation. The
CMU dictionary is a single text file. The module cmuparser.py
parses the file into into a python dictionary data structure.

The module contains a class called CMUDictionary which is a wrapper for a python
dictionary. A CMUDictionary object maps strings, representing word indexes, to Tran-
scription objects. Each transcription object can hold multiple phoneme representations
of the same word index. Each phoneme representation has its data container, which is a
member of the Phoneme class.

This module has one public interface method: CMUtranscribe(word), that takes as ar-
gument a string key and returns either a list of phonemes that represent the argument,
or a None value.

The cmuparser can be tested from the command line. It will transcribe 100 words chosen
at random from a descriptive dictionary packaged with this project.


'''
    Parses CMU dictionary into Python Dictionary
    AC 2017-08-10: updated from Py2 original for Py3
    changes other than print() statements noted
'''
import os, re, random, types, functools

# Settings 
CMU_DIR = './CMU_dictionary' 
# Version 
VERSION = 'cmudict.0.7a'
# Path
PATH_TO_DICTIONARY = os.path.join(CMU_DIR, (VERSION))

## Py2 -> Py3 problem: attempted fix for 'basestring' check in original script
## breaks: comment out check on basestring
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

## original class
class CMUDictionary(object):
    
    def __init__(self, path_to_dictionary = PATH_TO_DICTIONARY):
        
        self.regexp = re.compile(r'''
                        (?P<Comment>;;;.*) # ;;; denotes Comment: to be ignore
                        |(?P<Word>'?\w+[^\(\)]*) # Not interested in first charcter
                        (?P<Alternative> \(\d+\))? # (digit) denotes that another 
                        (?P<Seperator> \s\s) # Seperator: to be ignored
                        (?P<Phoneme> [^\n]+) # The remainder 
                     ''', re.VERBOSE)
        
        # import CMU dictionary
        try:
            self.cmudict_file = open(path_to_dictionary)
        except IOError as e:  # syntax change for Py3
            print (e, 'file not found, check settings...')
        # create Python CMU dictionary
        self._cmudict = self._create_dictionary() 
        self.cmudict_file.close()
    
    def __getitem__(self, key):
        #if not isinstance(key, basestring):
            #raise KeyError('key must be of type: basestring')
        try:
            return self._cmudict[key.upper()]  # ack: Dimitrios Alikaniotis https://gist.github.com/dimalik/440abc458fbcf4470171274d95efe67e
            #return self._cmudict[key.encode('utf-8').upper()]
        except (KeyError, UnicodeDecodeError):
            return None
    
    def _create_dictionary(self):
        dict_temp = {}
        for line in self.cmudict_file.readlines():    
            match = re.match(self.regexp, line)
            if match:
                dict_temp = self._update_dictionary(match, dict_temp)
        return dict_temp
    
    def _update_dictionary(self, match, dictionary):
        if match.group('Word') == None:
            # No word found, do nothing
            return dictionary
        
        if match.group('Word') and (match.group('Alternative') == None):
            # This is a new word
            # Create an an entry, and instantiate a Transcription object
            dictionary[match.group('Word')] = Transcription(match.group('Phoneme'))
            return dictionary
        
        if match.group('Word') and match.group('Alternative'):
            # There is an alternative phenome representation of the metched word
            # Append phenome rep. to dictioanry entry for this word
            dictionary[match.group('Word')].append(match.group('Phoneme'))            
            return dictionary

class Transcription(object):
    # load dictionary
    # the phoneme transcription of the word
    def __init__(self, phoneme, word=None):
        self.representation = [Phoneme(phoneme)]
    def __len__(self):
        return len(self.representation)
    def __str__(self):
        return '[' + functools.reduce(lambda x,y: str(x) + str(y) + ', ', self.representation, '') + ']'  # note functools to deal with reduce in Py3
    def append(self, phoneme):
        self.representation.append(Phoneme(phoneme))
    def get_phonemic_representations(self):
        # return all the phonemes that can represent this word
        return [x.phoneme for x in self.representation] 

class Phoneme(object):
    def __init__(self, phoneme):
        self.phoneme = phoneme
    def __str__(self):
        return str(self.phoneme)


## create dictionary
cmudict = CMUDictionary()


def CMUtranscribe(word):
    try:
        return cmudict[word].get_phonemic_representations()
    except AttributeError:
        # Entry not found
        return None


def test(word):
    return CMUtranscribe(word)

def test():
    ''' Test Function - prints the transcription of 100 words '''
    words = open('./CMU_dictionary/american-english')
    words = words.readlines()
    
    for i in range(100): 
        word = random.choice(words)[:-1]
        syllable = CMUtranscribe(word)
        if syllable: 
            transcriptions = 0
            for ph in syllable : 
                transcriptions += 1
                word += '\n' 
                word += str(transcriptions) + (': ' + ph)
            word += '\n'
            print(word)

if __name__ == '__main__':
    print(test())

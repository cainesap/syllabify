import re, csv, os, nltk
import syllable3 as sy
from nltk.corpus import cmudict
from nltk.corpus.reader import CHILDESCorpusReader


## 1) load corpus
# Emma
#corpus_root = nltk.data.find('C:\\Users\\Emma\\AppData\\Roaming\\nltk_data\\corpora\\Brown')
#brown = CHILDESCorpusReader(corpus_root, '.*\\.*.xml')
# Andrew
corpus_root = nltk.data.find('/Users/apc38/Dropbox/workspace/Corpora/CHILDES/xml/BrownXML')
brown = CHILDESCorpusReader(corpus_root, '.*/.*.xml')
fileidlist = brown.fileids()

## 2) make a list of all participants other than children
partislist = brown.participants(fileidlist)
plist = []
patt = re.compile('CHI')
for pdict in partislist:
    for p in pdict.keys():
        if patt.match(p):
            print('ignoring child')
        else:
            print('not a child, this is', p)
            if p not in plist:
                plist.append(p)
                print('added to list, list is now', len(plist), 'items long')

## 3) for each file, get sentences and phoneticize using CMU pronunciation dictionary
transcr = cmudict.dict()
phonsents = []
syllsents = []
sents = []
errorcount = 0
wordcount = 0
## regex to match 'thank_you' token
thanks = re.compile('thank_you')
for fid in fileidlist:
    sentslist = brown.sents(fid, speaker=plist)
    #print (fid, len(sentslist))
    for sent in sentslist:
        print(sent)
        sents.append(sent)
        sent = [w.lower() for w in sent]
        phon = []
        syll = ''  # syllabification will be a string
        ## check for 'thank_you' token in sentence and split if necessary
        for i, w in enumerate(sent):
            if thanks.match(w):
                sent[i]='thank'
                sent.insert(i+1, 'you')
        ## for each word in sentence, syllabify if in dictionary
        for w in sent:
            if w in transcr:
                #print(w)
                phon.append(transcr[w][0])
                wordcount+=1
                ## syllabify
                syllables = sy.generate(w)
                try:  # formatting per wordseg defaults: space between phones, ";esyll" between syllables, ";eword" between words
                    for syllable in syllables:
                        for syllable0 in syllable:
                            stripped = re.sub('[a-z0-9{}\[\]:,]', '', str(syllable0))  # phones only, no stress markers
                            stripped = re.sub('\s{2,}', ' ', stripped)  # reduce multi-spaces to single space
                            syll = syll + stripped + ';esyll'  # add to syllabified string with space between syllables
                    syll = re.sub(';esyll$', ';eword', syll)  # replace final syllable delimiter with word delimiter
                except:  # if no syllabification, skip
                    print("** Syllabification of", w, "not possible **")
                    errorcount+=1
            else:
                errorcount+=1
        phonsents.append(phon)
        syll = syll.strip()
        syllsents.append(syll)
        print(syll)

print('number of words not in dictionary =', errorcount)               
print('number of words =', wordcount)

## 4) save all sentence types to csv files
#with open('C:\\Users\\Emma\\Documents\\0School work\\0Uni\\0Work\\browncorpussentenses.csv', 'w') as myfile:
#    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#    wr.writerows(sents)

#with open('C:\\Users\\Emma\\Documents\\0School work\\0Uni\\0Work\\browncorpusphonsents.csv', 'w') as myfile:
#    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#    wr.writerows(phonsents)

#with open('C:\\Users\\Emma\\Documents\\0School work\\0Uni\\0Work\\browncorpussyllablesents.csv', 'w') as myfile:
#    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#    wr.writerows(syllsents)

''' 
	Data types for syllabification 
'''

import functools

VOWEL_TYPES = {
	# Short Vowels
	'AO' : { 'length' : 'short' }, 
	'UW' : { 'length' : 'short' }, 
	'EH' : { 'length' : 'short' }, 
	'AH' : { 'length' : 'short' }, 
	'AA' : { 'length' : 'short' }, 
	'IY' : { 'length' : 'short' }, 
	'IH' : { 'length' : 'short' }, 
	'UH' : { 'length' : 'short' }, 
	'AE' : { 'length' : 'short' }, 

	# Long Vowels
	'AW' : { 'length' : 'long' },
	'AY' : { 'length' : 'long' },
	'ER' : { 'length' : 'long' },
	'EY' : { 'length' : 'long' },
	'OW' : { 'length' : 'long' },
	'OY' : { 'length' : 'long' },	
}


'''Represents groups of phonemes. Clusters contain either Vowels, or Consonants - never both'''
class Cluster(object):
	def __init__(self, phoneme = None):
		self.phoneme_list = []
		if phoneme: 
			self.add_phenome(phoneme)
		# all phonemes have a string representation 
		self.comparator = self.get_phoneme_string()

	def get_phoneme(self):
		return self.phoneme_list
	
	def get_phoneme_string(self):
		# syllable without an onset, or coda has a phenome of '' empty string 
		string = ''
		for ph in self.phoneme_list: 
			string += ph.phoneme
		return string

	def add_phenome(self, phoneme):
		self.phoneme_list.append(phoneme)
		self._update_comparator()

	def add_phoneme(self, phoneme):
		self.phoneme_list.append(phoneme)
		self._update_comparator()

	def _update_comparator(self):
		self.comparator = self.get_phoneme_string()

	def get_stress(self):
		if self.type() == Vowel: 
			# mapping function that returns the stress value of a Vowel
			func_stress = lambda x: x.stress
			# return the maximum stress value in the cluster
			return functools.reduce(lambda x,y: x if int(x) > int(y) else y, map(func_stress, self.phoneme_list),0)  # updated for Py3
	
	'''returns the type of the phoneme cluster: either Vowel, or Consonant'''
	def type(self):
		if self.phoneme_list == []:
		 	return None
		else:
			return type(self.phoneme_list[-1])

	# Boolean Methods	
	def is_short(self):
		if self.type() == Vowel: 
			# Rule for determining if vowel is short
			return (len(self.phoneme_list) == 1 and self.phoneme_list[0].length == 'short')
	def is_long(self):
		return not self.is_short()
	
	def has_phoneme(self):
		return bool(self.phoneme_list != [])

	''' compare cluster objects '''
	def __eq__(self, cls_obj):
		return self.comparator == cls_obj.comparator
	def __ne__(self, cls_obj):
		return self.comparator != cls_obj.comparator
	def __nonzero__(self):
		return self.phoneme_list != []

	# Representation
	def __str__(self):
		return functools.reduce(lambda x,y: str(x) + str(y), self.phoneme_list,'')

''' container for the empty syllable cluster '''
class Empty(object):
	def __init__(self):
		self.phoneme = None
		self.comparator = None
	def __str__(self):
		return 'empty'
	def has_phoneme(self):
		return False
	def __nonzero__(self):
		return False
	def __eq__(self, cls_obj):
		return self.comparator == cls_obj.comparator
	def __ne__(self, cls_obj):
		return self.comparator != cls_obj.comparator

''' groups phenomes into syllables '''
class Syllable(object):
	# defaults were all set to None
	def __init__(self, onset=Empty(), nucleus=Empty(), coda=Empty()):
		self.onset = onset
		self.rime = Rime(nucleus, coda)
	# Setters
	def set_onset(self, cluster):
		self.onset = cluster
	def set_nucleus(self, cluster):
		self.rime.set_nucleus(cluster)
	def set_coda(self, cluster):
		self.rime.set_coda(cluster)
	# Getters
	def get_onset(self):
		return self.onset
	def get_nucleus(self):
		return self.rime.get_nucleus()
	def get_coda(self):
		return self.rime.get_coda()
	def get_stress(self):
		return self.rime.get_stress()
	def get_rime(self):
		return self.rime

	# Boolean Methods 
	def is_light(self):
		return self.is_short() and self.coda_is_empty()
	def is_short(self):
		return self.rime.nucleus.is_short()

	def has_onset(self):
		return bool(self.onset.has_phoneme())
	def onset_is_empty(self):
		return not self.has_onset()
	
	def has_nucleus(self):
		return self.rime.has_nucleus()
	def nucleus_is_empty(self):
		return not self.has_nucleus()
	
	def has_coda(self):
		return self.rime.has_coda()
	def coda_is_empty(self):
		return not self.rime.has_coda()
		
	# Representation
	def __str__(self):
		return '{o: ' + str(self.get_onset()) + ', n: ' + str(self.get_nucleus()) + ', c: ' + str(self.get_coda()) + '}'

''' Rime Class '''
class Rime:
	def __init__(self, nucleus=None, coda=None):
		self.nucleus = nucleus
		self.coda = coda
	# Setters
	def set_nucleus(self, cluster):
		self.nucleus = cluster
	def set_coda(self, cluster):
		self.coda = cluster

	# Boolean Methods
	def has_nucleus(self):
		return bool(self.nucleus.has_phoneme())
	def has_coda(self):
		return bool(self.coda.has_phoneme())
	
	def get_nucleus(self):
		return self.nucleus
	def get_coda(self):
		return self.coda
	def get_stress(self):
		return self.nucleus.get_stress()


''' Represents an individual phoneme that has been classified as a vowel '''
class Vowel(object):
	def __init__(self, **features):
		# phoneme string
		self.phoneme = features['Vowel']
		# retireves appropriate entry from vowel types dictionary
		# for this particular phoneme
		self.vowel_features = VOWEL_TYPES[self.phoneme]
		# stress string
		self.stress = features['Stress']
		# length of vowel (short, or long)
		self.length = self.vowel_features['length']
	# Representation
	def __str__(self):
		return '%s [st:%s ln:%s]' %  (self.phoneme, self.stress, self.length)

''' Represents an individual phoneme that has been classified as a consonant '''
class Consonant(object):
	def __init__(self, **features):
		self.phoneme = features['Consonant']
		
	def __str__(self):
		return '%s ' % self.phoneme


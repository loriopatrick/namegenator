import random

vowels = ('a', 'e', 'i', 'o', 'u', 'y')
consonances = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't',
               'v', 'w', 'x', 'z')

tops = ('t', 'i', 'd', 'f', 'j', 'h', 'k', 'l', 'b')
bots = ('q', 'y', 'p', 'g', 'j')
flats = ('a', 'c', 'e', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'y', 'z')

syllables = ('ing', 'ti', 'po', 'tle', 'fac', 'li', 'ern', 'er', 'ri', 'sion', 'day', 'fer',
             'lo', 'eve', 'a', 'be', 'vi', 'ny', 'gen', 'men', 'ly', 'per', 'el', 'pen',
             'ic', 'min', 'ies', 'ed', 'to', 'est', 'pre', 'land', 'mon', 'ket', 'i', 'pro',
             'la', 'tive', 'light', 'op', 'lec', 'es', 'ac', 'lar', 'car', 'ob', 'out', 'main',
             're', 'ad', 'pa', 'ci', 'of', 'rec', 'mar', 'tion', 'ar', 'ture', 'mo', 'pos', 'ro',
             'mis', 'in', 'ers', 'for', 'an', 'tain', 'sen', 'my', 'e', 'ment', 'is', 'aus', 'den',
             'side', 'nal', 'con', 'or', 'mer', 'pi', 'ings', 'tal', 'ness', 'y', 'tions', 'pe',
             'se', 'mag', 'tic', 'ning', 'ter', 'ble', 'ra', 'ten', 'ments', 'ties', 'ex',
             'der', 'so', 'tor', 'set', 'ward', 'nu', 'al', 'ma', 'ta', 'ver', 'some', 'age', 'oc',
             'de', 'na', 'as', 'ber', 'sub', 'ba', 'pres', 'com', 'si', 'col', 'can', 'sur', 'but',
             'sup', 'o', 'un', 'fi', 'dy', 'ters', 'cit', 'te', 'di', 'at', 'ful', 'et', 'tu',
             'cle', 'ted', 'en', 'dis', 'get', 'it', 'af', 'co', 'tem', 'an', 'ca', 'low', 'mu',
             'au', 'cov', 'tin', 'ty', 'cal', 'ni', 'no', 'cy', 'daq', 'tri', 'ry', 'man', 'par',
             'ple', 'fa', 'dif', 'tro', 'u', 'ap', 'son', 'cu', 'im', 'ence', 'up')

char_swaps = (
	('k', 'c'),
	('a', 'e', 'i'),
	('o', 'u'),
	('q', 'k'),
	('y', 'z', 'x'),
	('w', 'v')
)

chunk_swaps = (
	('qu', 'k', 'q'),
	('ck', 'k')
)
type_cuts = (
	('vvc', '*vc', 1),
	('vcvcv', 'vc*cv', 1),
	('vccv', 'v*cv', 1),
	('cvv', 'cv*', 1),
    ('cvc', 'cv*', 2)
)

word_file = open('/usr/share/dict/words')
words = word_file.read().split('\n')
word_file.close()
words = words[:len(words) - 1]

def get_height(char):
	if char in bots:
		return 1
	if char in tops:
		return 2
	return 0


def word_rating(word, previous=None):
	score = - pow(len(word) - 3, 2)
	pos = 0
	for c in word:
		char_type = get_height(c)

		# we don't like aallaa or aappaa
		if pos and char_type and pos != len(word) - 1:
			score -= 5

		# we like laa or paa
		if not pos and char_type:
			score += 5
			if previous:
				p_end_type = get_height(previous[len(previous) - 1])

				# we like ql and lp to join words
				if p_end_type != char_type:
					score += 10
				# we don't like ll pp to join words
				elif p_end_type == char_type:
					score -= 5
			# we like laa
			elif char_type == 2:
				score += 5

		# we like aal or aap
		if pos == len(word) - 1 and char_type:
			score += 20
			if previous:
				p_end_type = get_height(previous[len(previous) - 1])
				# we like a swap in height
				if p_end_type != char_type:
					score += 5

		pos += 1

	for syllable in syllables:
		if word.find(syllable) > -1:
			score += 2

	return - score

def randomise_word(word):
	rand = random.Random()

	for c in word:
		for swap in char_swaps:
			if rand.randint(0, 1) and c in swap:
				replace = swap[rand.randint(0, len(swap) - 1)]
				word = word.replace(c, replace)
				break

	for swap in chunk_swaps:
		for chunk in swap:
			if word.find(chunk) > -1:
				word = word.replace(chunk, swap[rand.randint(0, len(swap) - 1)])
				break
	return word


def shorten_word(word):
	rand = random.Random()

	v_string = ''
	for c in word:
		v_type = 'c'
		if c in vowels:
			v_type = 'v'
		v_string += v_type

	for cut in type_cuts:
		if rand.randint(0, cut[2]) and v_string.find(cut[0]) > -1:
			v_string = v_string.replace(cut[0], cut[1])

	res = ''
	for i in range(len(word)):
		if v_string[i] != '*':
			res += word[i]

	return res


def get_variations(word):
	rand = random.Random()

	words = [word]
	def reforge(fn):
		word = fn(words[rand.randint(0, len(words) - 1)])
		if word not in words:
			words.append(word)

	for i in range(0, 500):
		reforge(randomise_word)
		reforge(shorten_word)
		def combine(word):
			return shorten_word(randomise_word(word))
		reforge(combine)

	return words

def top_combine(words):
	rand = random.Random()
	res = None

	def sort():
		def key(word):
			return word_rating(word, res)
		words.sort(key=key)
		words.reverse()

	sort()
	res = words.pop()
	l = rand.randint(1, len(words))

	for i in range(l):
		sort()
		res += words.pop()

	return res



def build_domains(keywords):
	variations = []

	for keyword in keywords:
		vs = get_variations(keyword.lower())
		vs.sort(key=word_rating)
		variations.append(vs)

	rand = random.Random()
	def get_rand_words():
		res = []
		for vs in variations:
			res.append(vs[rand.randint(0, len(vs) / 2 - 1)])
		return res

	res = []
	for x in range(800):
		item = top_combine(get_rand_words())
		if item not in res:
			res.append(item)

	return res



domains = build_domains(['ad', 'video', 'custom'])
domains.sort(key=len)

print domains

#variants = get_variations('decanal')
#variants.sort(key=word_rating)

#print '\n'.join(variants)
#for word in words[500:1000]:
#	print word, get_variations(word)

#print 'decanal', randomise_word('decanal')

#words.sort(key=word_rating)
#rand = random.Random()
#start = rand.randint(0, 1000)
#print '\n'.join(words)

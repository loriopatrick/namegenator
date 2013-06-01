import random
import socket

vowels = ('a', 'e', 'i', 'o', 'u', 'y')
consonances = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't',
               'v', 'w', 'x', 'z')

tops = ('t', 'i', 'd', 'f', 'j', 'h', 'k', 'l', 'b')
bots = ('q', 'y', 'p', 'g', 'j')
flats = ('a', 'c', 'e', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'y', 'z')

char_swaps = (
	('k', 'c'),
	('a', 'e'),
	('o', 'u'),
	('q', 'k'),
	('z', 'x'),
	('w', 'v'),
    ('m', 'n')
)

type_cuts = (
	('vvc', '*vc', 3),
	('vcvcv', 'vc*cv', 3),
	('vccv', 'v*cv', 10),
	('cvv', 'cv*', 3),
    ('cvc', 'cv*', 5)
)

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

	return - score

def randomise_word(word):
	rand = random.Random()
	for pos in range(len(word)):
		for swap in char_swaps:
			if rand.randint(0, 1) and word[pos] in swap:
				replace = swap[rand.randint(0, len(swap) - 1)]
				if rand.randint(0, 10):
					word = word.replace(word[pos], replace)
				else:
					word_list = list(word)
					word_list[pos] = replace
					word = ''.join(word_list)
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

	for i in range(0, 50):
		reforge(randomise_word)
		reforge(shorten_word)

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
	l = rand.randint(1, min(len(words), 3))

	for i in range(l):
		sort()
		res += words.pop()

	return res

def build_names(keywords):
	variations = []

	for keyword in keywords:
		vs = get_variations(keyword.lower())
		vs.sort(key=word_rating)
		variations.append(vs)

	rand = random.Random()
	def get_rand_words():
		res = []
		for vs in variations:
			word = vs[rand.randint(0, len(vs) - 1)]
			if rand.randint(0, 1):
				word = shorten_word(word)
			if rand.randint(0, 10):
				word = randomise_word(word)
			res.append(word)
		return res

	res = []
	for x in range(500):
		item = top_combine(get_rand_words())
		if item not in res:
			res.append(item)

	return res

def try_extensions(base):
	extensions = ['.com', '.net']
	res = []
	for ext in extensions:
		domain = base + ext
		if check_domain(domain):
			res.append(domain)

	return res

def check_domain(domain):
	sock = socket.socket()
	sock.connect(('whois.internic.net', 43))
	sock.send('%s\n' % domain)

	response = ''
	while response.find(domain) == -1:
		response += sock.recv(512).lower()

	registered = response.find('no match for ') == -1
	sock.close()
	return registered

if __name__ == '__main__':
	names = build_names(['computer', 'system', 'build', 'custom', 'personal'])
	print names
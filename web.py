import name
import json
from flask import Flask, request, send_file

app = Flask(__name__, static_folder='web')
app.debug = True

@app.route('/api/calc/scramble', methods=['GET'])
def names():
	keywords = request.args.get('keywords', None)
	if keywords is None or not len(keywords):
		return '{"error":"Parameter "keywords" is required. Example: ?keywords=funny,apple,monkey"}'

	keywords = keywords.split(',')

	fn = name.build_names
	if len(keywords) == 1:
		def single(words):
			return name.get_variations(words[0])
		fn = single

	domains = fn(keywords)
	domains.sort(key=name.word_rating)

	return json.dumps({
		'keywords':keywords,
		'results':domains
	})

@app.route('/')
def redirect():
	return send_file('web/index.html')

if __name__ == '__main__':
	app.run(port=8080)
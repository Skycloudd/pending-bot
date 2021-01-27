import json
import requests


def open_json(filename):
	with open(f'{filename}.json', 'r') as f:
		return json.load(f)

def write_json(filename, data):
	with open(f'{filename}.json', 'w+') as f:
		json.dump(data, f, indent=4)

def make_request(url):
	r = requests.get(url)
	return json.loads(r.text)

import requests
import json

from utility_functions import *


api = 'https://www.speedrun.com/api/v1'


def get_pending_count(ids):
	counts = {"games": [], "total": 0}

	for id in ids:
		total = 0

		offset = 0
		while True:
			url = f'{api}/runs?game={id}&status=new&max=200&offset={offset}'
			data = make_request(url)

			total += len(data["data"])

			next = False

			for link in data["pagination"]["links"]:
				if link["rel"] == 'next':
					next = True

			if not next:
				counts["games"].append(
					{
						"runs": total
					}
				)
				break

			offset += 200

	total_runs = sum([game["runs"] for game in counts["games"]])
	counts["total"] = total_runs

	return counts


def check_id(id):
	url = f'{api}/games/{id}'
	data = make_request(url)
	if "status" in data and "message" in data:
		return False
	else:
		return True


def abbr_to_id(abbreviation):
	url = f'{api}/games?abbreviation={abbreviation}'
	data = make_request(url)

	game_id = None
	for game in data["data"]:
		game_id = game["id"]

	return game_id


def id_to_abbr(id):
	url = F'{api}/games/{id}'
	data = make_request(url)

	return data["data"]["abbreviation"]


def id_to_name(id):
	url = F'{api}/games/{id}'
	data = make_request(url)

	return data["data"]["names"]["international"]
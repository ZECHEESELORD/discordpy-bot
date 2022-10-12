import requests
import time
import json
import os

#variables to change.
username = "LinearTime"
HYPIXEL_API_KEY = os.environ['HYPIXEL_API_KEY']
URL = os.environ['URL_LINEARTIME']

previous_state = ""

def usernametoUUID(username):
	mcAPI = requests.get("https://api.mojang.com/users/profiles/minecraft/{}".format(username)).json()
	return(mcAPI['id'])

uuid = usernametoUUID(username)

def notify(message):
	data = {}
	data["content"] = message
	data['username'] = "Harold"

	output = requests.post(URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
	try:
		output.raise_for_status()
	except requests.exceptions.HTTPError as err:
		print(err)
	else:
		print("Discord notified that player {} is {}".format(username, previous_state))

try:
	while True:
		data = requests.get("https://api.hypixel.net/player?key={}&uuid={}".format(HYPIXEL_API_KEY, uuid)).json()

		if(data['player']['lastLogin'] < data['player']['lastLogout']):
			if previous_state != "offline":
				previous_state = "offline"
				notify("> `{}` is **offline**. Harold, You can come online! [:red_circle:]".format(username))
		else:
			if previous_state != "online":
				previous_state = "online"
				notify("> `{}` is **online**. Do not come on! [:green_circle:]".format(username))
		time.sleep(30)
except KeyboardInterrupt:
	print("\n\nStopping from keyboard interrupt!")

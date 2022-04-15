import time
import requests

list_of_stations = []
list_of_piers = []
list_of_stops = []

def menu():
	number = -1
	while (number != 0 or number != 1 or number != 2):
		print("""\nWelcome to TFL unified API
0 - Rail \n1 - River""")
		number = int(input(">>>"))
		print(f"You have selected {number}")
		if (number == 0):
			tube()
		elif (number == 1):
			river()

def tube():
	generate_tube()
	play(list_of_stations)

def river():
	generate_river()
	play(list_of_piers)

def play(list_of_stations : list):

	number_of_players = int(input("Enter number of players: "))
	player_names = []
	player_points = [0] * number_of_players
	playing = True
	for i in range(0, number_of_players):
		name = str(input(f"Please enter name for player {i + 1} \n>>>"))
		player_names.append(name)

	correct_guesses = []
	who_guessed = []

	while(playing):
		for i in range(0, number_of_players):
			incorrect = 0
			if (playing):
				turn = True
				while (turn):
					if (incorrect > 2):
						list_of_stations = [i for i in list_of_stations if i not in correct_guesses]
						print(f"{player_names[i]} looses!")
						player_points[i] = 0
						playing = False
						missed = str(input(f"Would you like to see {len(list_of_stations)} missed stations?\nPress ENTER"))
						if missed == "":
							for s in list_of_stations:
								time.sleep(0.05)
								print(s)
							break
					print(f"\nEnter guess for player: {player_names[i]} \n- A guess of 'Mornington Crescent' will forfeit the game!")
					if (incorrect == 2):
						print("- If you get this wrong you loose!")
					guess = str(input(f">>>"))
					if (guess == "Mornington Crescent"):
						correct_guesses.append(guess)		
						list_of_stations = [i for i in list_of_stations if i not in correct_guesses]
						print(f"{player_names[i]} looses!")
						player_points[i] = 0
						playing = False
						missed = str(input(f"Would you like to see {len(list_of_stations)} missed stations?\nPress ENTER"))
						if missed == "":
							for s in list_of_stations:
								time.sleep(0.05)
								print(s)
							break
					elif (guess in list_of_stations):
						if (guess not in correct_guesses):
							print("Correct")
							player_points[i] += 1
							correct_guesses.append(guess)
							who_guessed.append(i)
							turn = False
						else:
							print(f"{guess} has already been guessed by player: {player_names[who_guessed[correct_guesses.index(guess)]]}!")
							player_points[i] -= 1
					else:
						print("This is not a valid station, please check spelling or choose another!")
						player_points[i] -= 1
						incorrect += 1

def generate_tube():
	global list_of_stations 
	tube_stoppoints = []
	overground_stoppoints = []
	dlr_stoppoints = []
	tfl_rail_stoppoints = []

	print("Loading...")

	response = requests.get(f"https://api.tfl.gov.uk/Stoppoint/mode/tube")
	raw_data = response.json()
	for stop in raw_data['stopPoints']:
		tube_stoppoints.append(stop['commonName'])
	tube_stoppoints = [x.removesuffix(" Station") for x in tube_stoppoints]
	tube_stoppoints = [x.removesuffix(" Underground") for x in tube_stoppoints]

	""" OLD
	response = requests.get(f"https://api.tfl.gov.uk/line/mode/tube/status")
	raw_data = response.json()
	for tubeLine in raw_data:
		get_request = requests.get(f"https://api.tfl.gov.uk/line/{tubeLine['id']}/stoppoints")
		stopPoints = get_request.json()
		for stop in stopPoints:
			tube_stoppoints.append(stop['commonName'])
	"""

	response = requests.get(f"https://api.tfl.gov.uk/Stoppoint/mode/overground")
	raw_data = response.json()
	for stop in raw_data['stopPoints']:
		overground_stoppoints.append(stop['commonName'])
	overground_stoppoints = [x.removesuffix(" Station") for x in overground_stoppoints]
	overground_stoppoints = [x.removesuffix(" Rail") for x in overground_stoppoints]
	
	response = requests.get(f"https://api.tfl.gov.uk/Stoppoint/mode/dlr")
	raw_data = response.json()
	for stop in raw_data['stopPoints']:
		dlr_stoppoints.append(stop['commonName'])
	dlr_stoppoints = [x.removesuffix(" Station") for x in dlr_stoppoints]
	dlr_stoppoints = [x.removesuffix(" DLR") for x in dlr_stoppoints]

	response = requests.get(f"https://api.tfl.gov.uk/Stoppoint/mode/tflrail")
	raw_data = response.json()
	for station in raw_data['stopPoints']:
		tfl_rail_stoppoints.append(station['commonName'])
	tfl_rail_stoppoints = [x.removesuffix(" Station") for x in tfl_rail_stoppoints]
	tfl_rail_stoppoints = [x.removesuffix(" Rail") for x in tfl_rail_stoppoints]

	list_of_stations = tube_stoppoints + overground_stoppoints + dlr_stoppoints + tfl_rail_stoppoints
	list_of_stations = clean_array(list_of_stations)

def generate_river():
	global list_of_piers

	river_bus_stoppoints = []

	print("Loading...")

	response = requests.get(f"https://api.tfl.gov.uk/Stoppoint/mode/river-bus")
	raw_data = response.json()
	for pier in raw_data['stopPoints']:
		river_bus_stoppoints.append(pier['commonName'])
	river_bus_stoppoints = [x.removesuffix(".") for x in river_bus_stoppoints]
	river_bus_stoppoints = [x.removesuffix(" Pier") for x in river_bus_stoppoints]

	list_of_piers = river_bus_stoppoints # +
	list_of_piers = clean_array(list_of_piers)

def clean_array(arr : list) -> list:
	arr = remove_duplicates(arr)
	arr = remove_character(arr, '(')
	arr = remove_character(arr, '/')
	arr.sort()
	arr = remove_duplicates(arr) # For some reason doesn't work unless duplicates are removed twice
	return arr

def remove_duplicates(arr : list) -> list:
	return list(dict.fromkeys(arr))

def remove_character(arr : list, char : str) -> list:
	for i in range(0, len(arr)):
		if (char in arr[i]):
			arr[i] = arr[i][:arr[i].index(char)-1]
	return arr

menu()
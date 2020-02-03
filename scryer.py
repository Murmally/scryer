# Standard libraries
import sys
import os
import math
import re

# Library used to parse information from *.SC2Replay files: https://github.com/ggtracker/sc2reader
import sc2reader

# Counter dictionaries used to track replay's status
from counters import *
from loader import get_files_to_parse, format_replay_header

lastTime = 0;
time_coefficient = 0.714

# TODO: rozlisit WarpGate a Gateway
# TODO: check_user_input
# TODO: propagovat zmeny v counterech

def check_user_input():
	regex = sys.argv[1]
	if len(sys.argv) != 2:
		print("Wrong argumenets! Use format MM:SS")
		exit(-1)

# functions used to format output to console


# returns true only for UnitDiedEvent, UnitDoneEvent, UnitBornEvent, UnitTypeChangedEvent, UpgradeCompleteEvent
def is_event_relevant(event):
	relevant_events = ["UnitDiedEvent", "UnitDoneEvent", "UnitBornEvent", "UnitInitEvent", "UnitTypeChangedEvent"] #, "UpgradeCompleteEvent"
					   #"UnitInitEvent", "CommandEvent", "DataCommandEvent", "GameEvent", "PlayerLeaveEvent", "ResourceRequestEvent",
					   #"ResourceRequestFulfillEvent", "ResourceTradeEvent", "BasicCommandEvent"]
	for aux in relevant_events:
		if event.name == aux:
			return True
	return False
# CreepTumorQueen = creep tumor in the making
def is_unit_relevant(unit):
	ignored_units = ["KD8Charge", "AdeptPhaseShift", "MineralField750", "CreepTumorBurrowed", "Changeling", "ChangelingZergling", "ChangelingZerglingWings",
	 "RavagerCocoon", "Locust", "LocustMPFlying", "LocustMPPrecursor", "Interceptor", "Broodling", "Egg", "CreepTumorQueen", "BanelingCocoon"]
	for ignored_unit in ignored_units:
		if ignored_unit == unit:
			return False
	return True


# checks whether the event has occured later than user set it to
def check_time(time, event):
	global time_coefficient
	aux = time.split(':')
	in_time = int(aux[0]) * 60 + int(aux[1])
	fixed_time = event.second * time_coefficient
	return in_time >= fixed_time

# debugging and reserach purposes
def print_event_object_attributes(event):
	was_mentioned = {"UnitDiedEvent": 0, "UnitDoneEvent": 0, "UnitBornEvent": 0, "UnitTypeChangedEvent": 0, "UpgradeCompleteEvent": 0, "UnitInitEvent": 0,
	 "CommandEvent": 0, "DataCommandEvent": 0, "GameEvent": 0, "PlayerLeaveEvent": 0, "ResourceRequestEvent": 0, "ResourceRequestFulfillEvent": 0, "ResourceTradeEvent": 0, "BasicCommandEvent": 0}

	if event.name == "UnitDoneEvent":
		print(event.name + ": " + str(dir(event)))
		print()
	else:
		return
	for name in was_mentioned:
		if name == event.name:
			if was_mentioned[name] == 0:
				print(event.name + ": " + str(dir(event)))
				print()
				was_mentioned[name] = 1


# SC2Replay doesn't use real-time, but its own unit of time - frame
# By conducting several experiments I figured that 1 frame ~ 0.714 seconds
def get_real_time(num_of_frames):
	global time_coefficient
	temp = time_coefficient * num_of_frames
	sec = str(round(temp%60, 0)).split('.')[0]
	if len(sec) == 1:
		sec = "0" + sec
	return "{}:{}".format(str(math.floor(temp/60)).split('.')[0], sec)



def get_unit_name(unit):
	ret = str(unit).split('[')[0].strip()
	return ret 

def get_player_name(event):
	try:
		xd = event.unit.owner.name
	except:
		return None
	return str(event).split(' ')[4].strip()

def print_UnitDoneEvent_info(event, time, player_name):
	unit_name = get_unit_name(event.unit)
	if is_unit_relevant(unit_name) == False: return
	print("{}  {}'s {} done".format(time, player_name, unit_name))

def print_UnitBornEvent_info(event, time, player_name):
	unit_name = get_unit_name(event.unit)
	if is_unit_relevant(unit_name) == False: return
	print("{}  {} completed {}".format(time, player_name, unit_name))

def print_UnitDiedEvent_info(event, time):
	unit_name = get_unit_name(event.unit)
	if is_unit_relevant(unit_name) == False: return
	if event.killer == None: return
	if event.killer.name == event.unit.owner.name:
		print("{}  {}'s {} died".format(time, event.unit.owner.name, unit_name))
	print("{}  {} killed {}'s {}".format(time, event.killer.name, event.unit.owner.name, unit_name))

def print_event_info(event):
	time = get_real_time(event.second)
	name = get_player_name(event)
	if name == None: 
		return

	if event.name == "UnitDoneEvent":
		print_UnitDoneEvent_info(event, time, name)
	elif event.name == "UnitBornEvent":
		print_UnitBornEvent_info(event, time, name)
	elif event.name == "UnitDiedEvent":
		print_UnitDiedEvent_info(event, time)

# TODO - aktualizace counteru
def update_counters(event, counters):
	name = get_player_name(event)
	if name == None:
		return
	unit_name = get_unit_name(event.unit)
	if is_unit_relevant(unit_name) == False: 
		return
	if event.name == "UnitDiedEvent":
			change_counter_value(counters[name], event.unit.name, False)
	elif event.name == "UnitBornEvent" or event.name == "UnitDoneEvent" or event.name == "UnitInitEvent" or event.name == "UnitTypeChangedEvent":
		change_counter_value(counters[name], event.unit.name, True)
	return




# Second most-important function
def print_status(replay, time, counters):
	for event in replay.events:
		if is_event_relevant(event):
			if hasattr(event, 'second'):
				if event.second == 0:
					continue
				if check_time(time, event) == False:
					break 		# in case the event occured later than user's threshold
			update_counters(event, counters)
			if event.name == "UnitInitEvent" or event.name == "UnitTypeChangedEvent":
				print(event)
			#print_event_info(event) # detailed description of the game
	return


def main():
	check_user_input()
	replays = get_files_to_parse()
	arr = list()
	for replay in replays:
		print(format_replay_header(replay))
		counters = init_counters(replay)
		print_status(replay, sys.argv[1], counters)
		print_counter_content(counters)
	print("Done! Exiting...")
	return



if __name__ == '__main__':
	main()

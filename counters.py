def init_zerg_counter():
	counter = {
		'Baneling': 0,
		'BroodLord': 0,
		'Corruptor': 0,
		'Drone': 12,
		'Hydralisk': 0,
		'Infestor': 0,
		'Larva': 3,
		'Lurker': 0,
		'Mutalisk': 0,
		'NydusWorm': 0,
		'Overlord': 1,
		'Overseer': 0,
		'Queen': 0,
		'Ravager': 0,
		'Roach': 0,
		'SwarmHost': 0,
		'Ultralisk': 0,
		'Viper': 0,
		'Zergling': 0,
		'BanelingNest': 0,
		'CreepTumor': 0,
		'EvolutionChamber': 0,
		'Extractor': 0,
		'GreaterSpire': 0,
		'Hatchery': 1,
		'Hive': 0,
		'HydraliskDen': 0,
		'InfestationPit': 0,
		'Lair': 0,
		'LurkerDen': 0,
		'NydusNetwork': 0,
		'RoachWarren': 0,
		'SpawningPool': 0,
		'SpineCrawler': 0,
		'Spire': 0,
		'SporeCrawler': 0,
		'UltraliskCavern': 0
		}
	return counter

def init_terran_counter():
	counter = {
		'Banshee': 0,
		'Battlecruiser': 0,
		'Cyclone': 0,
		'Ghost': 0,
		'Hellbat': 0,
		'Hellion': 0,
		'Liberator': 0,
		'Marauder': 0,
		'Marine': 0,
		'Medivac': 0,
		'MULE': 0,
		'Raven': 0,
		'Reaper': 0,
		'SCV': 12,
		'SiegeTank': 0,
		'Thor': 0,
		'Viking': 0,
		'WidowMine': 0,
		'WidowMineBurrowed': 0,
		'Armory': 0,
		'Barracks': 0,
		'BarracksFlying': 0,
		'BarracksReactor': 0,
		'BarracksTechLab': 0,
		'Bunker': 0,
		'CommandCenter': 1,
		'EngineeringBay': 0,
		'Factory': 0,
		'FactoryFlying': 0,
		'FactoryTechLab': 0,
		'FactoryReactor': 0,
		'FusionCore': 0,
		'GhostAcademy': 0,
		'MissileTurret': 0,
		'OrbitalCommand': 0,
		'PlanetaryFortress': 0,
		'Reactor': 0,
		'Refinery': 0,
		'SensorTower': 0,
		'Starport': 0,
		'StarportFlying': 0,
		'StarportTechLab': 0,
		'StarportReactor': 0,
		'SupplyDepot': 0,
		'SupplyDepotLowered': 0,
	}
	return counter

def init_protoss_counter():
	counter = {
		'Adept': 0,
		'Archon': 0,
		'Carrier': 0,
		'Colossus': 0,
		'DarkTemplar': 0,
		'Disruptor': 0,
		'HighTemplar': 0,
		'Immortal': 0,
		'Mothership': 0,
		'Observer': 0,
		'Oracle': 0,
		'Phoenix': 0,
		'Probe': 12,
		'Sentry': 0,
		'Stalker': 0,
		'Tempest': 0,
		'VoidRay': 0,
		'WarpPrism': 0,
		'Zealot': 0,
		'Assimilator': 0,
		'CyberneticsCore': 0,
		'DarkShrine': 0,
		'FleetBeacon': 0,
		'Forge': 0,
		'Gateway': 0,
		'Nexus': 1,
		'PhotonCannon': 0,
		'Pylon': 0,
		'RoboticsBay': 0,
		'RoboticsFacility': 0,
		'ShieldBattery': 0,
		'Stargate': 0,
		'TemplarArchives': 0,
		'TwilightCouncil': 0,
		'WarpGate': 0
	}
	return counter

# TODO
# Determines, whether given unit is a structure with addon
# Returns name of the default building
def is_terran_addon(unit):
	return

def get_default_name(unit):
	

	if unit == "LurkerBurrowed":
		return "Lurker"
	return unit

# TODO fuckton of business logic
# if is_addon_building:
#	decrement_base_building()
def change_counter_value(counter, unit, is_increment):
	unit = get_default_name(unit)
	if unit != "" and unit != None:
		if is_increment:
			counter[unit] += 1
			print("Incrementing " + unit)

		else:
			print("Decrementing " + unit)
			counter[unit] -= 1
	return
 


def print_counter_content(counters):
	for counter in counters:
		print(counter)
		for item in counters[counter]:
			cnt = counters[counter].get(item)
			if cnt == 0:
				continue
			print(item + ": " + str(cnt))
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")



def init_counters(replay):
	counters = {}
	for team in replay.teams:
		for player in team:
			if(player.pick_race[0] == "Z"):
				counters[player.name] = init_zerg_counter()
			elif (player.pick_race[0] == "P"):
				counters[player.name] = init_protoss_counter()
			elif (player.pick_race[0] == "T"):
				counters[player.name] = init_terran_counter()
	return counters


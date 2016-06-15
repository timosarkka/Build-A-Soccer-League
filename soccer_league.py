#!/usr/bin/env python

""" This script sorts 18 youth soccer league players to 3 different teams.
The script ensures that there are the same no. of experienced players per team
and that the average height of each team is within 1 inch of each other. 
It then prints out a personalized letter for the guardians of the children.
Letters will be saved to disk as 'firstname_lastname.txt' (child's name)."""

import csv

__author__ = "Timo Särkkä"
__copyright__ = "Copyright 2016, Timo Särkkä"
__version__ = "1.0"

# Noticed that the time definitions need to be here, otherwise an exception occurs
times = {'Dragons': 'March 17, 1pm', 'Sharks': 'March 17, 3pm', 'Raptors': 'March 18, 1pm'}

# A function to read each player's data from the .csv-file row by row
# Assigns data to an individual dictionary, 18 in total
# These dictionaries are then appended to a single list, which is returned
# NOTE! Also checked that this works if rows are shuffled
def read_players():
	with open('soccer_players.csv') as csvfile:
		playerreader = csv.DictReader(csvfile, delimiter=',')
		player_list = []
		for row in playerreader:
			player_list.append(row)
		return(player_list)

# A help function to generate the needed teams as dictionaries
# Team will be assigned a name and an empty list of players
# Teams are then returned
def make_team(name):
	team = {'name': name, 'players': []}
	return team

# This function sorts players to two lists, experienced an new players
# Helps to add the players later on equally to teams
# Returns both lists
def sort_players(player_list, players_exp, players_new):
	for player in player_list:
		if player['Soccer Experience'] == 'YES':
			players_exp.append(player)
		else:
			players_new.append(player)
	return players_exp, players_new

# A function to assign the players  to teams
# Experienced players are assigned first, then the new players
# Returns the full league, which is a list of all the team dictionaries
# filled with players.
# NOTE! Checked that this works, even if there are new players added,
# as least long as it is possible to divide them evenly to teams...
def assign_teams(league, players_exp, players_new):
	# i = the number of experienced players in total divided by the number of teams
	# j = the number of total players per team
	i = (len(players_exp) / len(league))
	j = ((len(players_new)+len(players_exp))/len(league))
	# The for loop continues until each team is full of players.
	for team in league:
		# The first while-loop is continued until we reach the max. number of 
		# experienced players allowed to be joined to one team. 
		while (len(team['players']) < i):
			team['players'].append(players_exp.pop(0))
		# The second loop continues until the max. number of players for each
		# team is reached.
		while (len(team['players']) < j):
			team['players'].append(players_new.pop(0))
	return league

# Writes an automated letter for each of the children's guardians
def write_letter(team):
	# For each player in the team dictionaries, this function is carried out
	for player in team['players']:
		# Formation of the filenames 'firstname_lastname.txt'
		first_name, last_name = player['Name'].split()
		file_name = first_name.lower() + "_" + last_name.lower() + ".txt"
		# Writing of the file
		with open(file_name, 'w+') as f:
			f.write("Dear {},\n\nI have the pleasure to announce that your little ".format(player['Guardian Name(s)']))
			f.write("puffmunchkin, {}, has been accepted ".format(player['Name']))
			f.write("to the junior soccer league team {}.\n\n".format(team['name']))
			f.write("Important! The first practice will take place on {} ".format(times[team['name']]))
			f.write("at Imaginary Stadium. Please bring your soccer gear with you.\n\n")
			f.write("With best regards,\n\n")
			f.write("Your coach Timo")
	return

# The main program function
def main():
	# Necessary lists are initialized
	league = []
	players_exp = []
	players_new = []
	
	# Team names and practice times are assigned to suitable collectibles.
	teams = ['Sharks', 'Dragons', 'Raptors']
	
	# Teams are generated with the necessary data
	for name in teams:
		league.append(make_team(name))
	
	# Reads players to a list
	player_list = read_players()
	
	# Sorts players to experienced and new
	sort_players(player_list, players_exp, players_new)
	
	# Assigns players to teams
	assign_teams(league, players_exp, players_new)
	
	# Writes the automated letters
	for team in league:
		write_letter(team)

if __name__ == '__main__':
	main()
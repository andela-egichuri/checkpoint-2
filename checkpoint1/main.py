import user
import room
import json
import random
import os

d_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(d_path, "data")


user_data = os.path.join(d_path, "data/users.json")
room_data = os.path.join(d_path, "data/rooms.json")
alloc_data = os.path.join(d_path, "data/Allocations.txt")


def check_files():
	'''
	Create the data files if they don't exist
	'''
	try:
		with open(user_data) as file:
			pass
	except IOError:
		with open(user_data, 'w+') as file:
			data = {"users": {"fellows": {},"staff": {}}}
			file.write(json.dumps(data, indent=4, sort_keys=True))

	try:
		with open(room_data) as file:
			pass
	except IOError:
		with open(room_data, "w+") as file:
			data = {"rooms": {"living": {},"office": {}}}
			file.write(json.dumps(data, indent=4, sort_keys=True))

	try:
		with open(alloc_data) as file:
			pass
	except IOError:
		with open(alloc_data, 'w+') as file:
			pass


def readInput(filename, src):
	'''
	This function reads the data entered using a text file and passes
	it to the saveRoom() function
	'''
	try:
		with open(filename, 'r') as f:
			if src == "rooms":
				for line in f:
					newroom = room.Room()
					words = line.split("\t")
					newroom.room_type = words[1].upper().strip()
					newroom.name = words[0].upper().strip()
					newroom.room_id = newroom.name[0:3].lower() + str((random.randint(10,100)))
					newroom.saveRoom()

			elif src == "users":
				for line in f:
					newuser = user.User()
					words = line.split("\t")
					newuser.user_type = words[1].upper().strip()
					newuser.user_name = words[0].upper().strip()
					if newuser.user_type == "F":
						newuser.accomodation = words[2].upper().strip()
					else:
						newuser.accomodation = "N/A"
					newuser.user_id = newuser.user_name[0:3].lower() + str((random.randint(10,100)))
					newuser.saveUser()
	except IOError as e:
		print "File not found"


def allocate(room_type, member):
	'''
	Checks if there are available rooms
	'''
	space = room.Room()
	available_rooms = space.available(room_type)
	if len(available_rooms) <= 0:
		if room_type == "O":
			print "Sorry, there are no more available office spaces"
		elif room_type == "L":
			print "Sorry, there are no more available living spaces"
	else:

		#Add members to rooms if there is space available
		rand_room = random.choice(available_rooms)
		space.addMember(rand_room, room_type, member)


def allocateAll(user_type):
	'''
	Gets unallocated users
	'''
	users = user.User()
	to_allocate = users.unallocated(user_type)

	#Allocate office spaces
	for member in to_allocate["office"]:
		allocate("O", member)

	#Allocate living spaces only to fellows
	if user_type == "F":
		for member in to_allocate["living"]:
			user_details =  users.getUser(member)
			if user_details["accomodation"] == "Y":
				allocate("L", member)


def home():
	'''
	Menu options for the system
	'''
	os.system('clear')
	print "MENU OPTIONS"
	print "********************************************************************"

	print "Select an option below to continue"
	selection = raw_input("1: Add users \n2: Add rooms \n3: View all allocations \n4: View allocations per room \
	 \n5: View all users in the system \n6: View users pending space allocation \
	 \n7: Allocate living and office space to users\n8: View available rooms\n9: Reset data \n10: Exit\n:")
	while selection not in str(range(1, 11)):
		selection = raw_input("Try again:\nPlease enter a number between 1 - 10\n:")
	return selection


def addUsers():
	'''
	Give the option to either enter user data manually or from a file
	'''
	print "\n"
	print "ADD USERS"
	print "********************************************************************"
	source = raw_input("1: Add user data manually \n2: to select an existing file \n3: Cancel\n:")


	while source != "1" and source != "2" and source != "3":
		source = raw_input("Try again.\n1: Add user data manually \n2: to select an existing file: \n3: Cancel\n:")


	if source == "1":
		newuser = user.User()
		newuser.addUser()
	elif source == "2":
		data_file = raw_input("Enter file name (including the file extension)\n")
		readInput(data_path + "/" + data_file, "users")
	elif source == "3":
		menu()


def addRooms():
	'''
	Give the option to either enter room data manually or from a file
	'''
	print "\n"
	print "ADD ROOMS"
	print "********************************************************************"
	source = raw_input("1: to add user data manually \n2: to select an existing file\n3: Cancel\n:")

	while source != "1" and source != "2" and source != "3":
		source = raw_input("Try again.\n1: to add user data manually \n2: to select an existing file:\n3: Cancel\n:")

	if source == "1":
		newroom = room.Room()
		newroom.addRoom()
	elif source == "2":
		data_file = raw_input("Enter file name (including the file extension)\n")
		readInput(data_path + "/" + data_file, "rooms")
	elif source == "3":
		menu()



def showUsers():
	'''
	Display users
	'''
	users = user.User()
	print "View USERS"
	print "********************************************************************"
	user_type = raw_input("Select User Type\n S: Staff \n F: Fellow \n C: Cancel \n:").upper()

	while user_type != "F" and user_type != "S" and user_type != "C":
		user_type = raw_input("Try again.\n S: Staff \n F: Fellow \n C: Cancel \n:").upper()

	if user_type == "C":
		menu()
	else:
		print users.listUsers(user_type)
	action = raw_input("\n1: Continue \n:")
	while action != "1" and action != "2":
		action = raw_input("Try again\n1: Continue \n:")
	if action == "1":
		menu()


def menu():
	'''
	Menu options
	'''
	check_files()
	try:
		selection
	except NameError:
		selection = ""
	while True:

		# Add users
		if selection == "1":
			addUsers()

		# Add rooms
		elif selection == "2":
			addRooms()

		# View all allocations
		elif selection == "3":
			print "\n"
			to_print = ""
			room_inst = room.Room()
			roomlist = room_inst.rooms("O")
			roomlist = roomlist + room_inst.rooms("L")
			for roomid in roomlist:
				userlist = ""
				users = user.User()
				room_details = room_inst.getRoom(roomid)
				room_members = room_details["occupants"]
				if len(room_details["occupants"]) > 0:
					to_print = to_print + room_details["name"] + " (" + room_details["room_type"] + ")\n"
				for member in room_members:
					user_details =  users.getUser(member)
					userlist = userlist + user_details["username"] + ", "
				if len(room_details["occupants"]) > 0:
					to_print = to_print + userlist + "\n\n"
			print to_print
			action = raw_input("\n1: Print\n2: Continue \n:")
			while action != "1" and action != "2":
				action = raw_input("Try again.\n1: Print\n2: Continue \n:")
			if action == "1":
				print "Printing to Allocations.txt"
				with open(data_path + "/Allocations.txt", "w+") as file:
					file.write(to_print)
				menu()
			elif action == "2":
				menu()

		# Print members per room
		elif selection == "4":
			print "\n"
			os.system('clear')
			room_type = raw_input("Enter Room Type: \n 1: Office space \n 2: Living space \n:")

			while room_type != "1" and room_type != "2":
				room_type = raw_input("Try again. Enter Room Type:\n 1: Office space \n 2: Living space \n:")
			if room_type == "1":
				rtype = "O"
			elif room_type == "2":
				rtype = "L"
			print "\n"
			print "Select one room from the list below"
			room_inst = room.Room()
			roomlist = room_inst.rooms(rtype)
			for each in roomlist:
				theroom = room_inst.getRoom(each)
				print " " + theroom["name"] + "\t(Room ID: " + theroom["roomID"] + ")"
			selected = raw_input("\nEnter Room ID \n:").lower()
			for roomid in roomlist:
				users = user.User()
				if roomid == selected:
					room_details = room_inst.getRoom(selected)
					room_members = room_details["occupants"]
					for member in room_members:
						user_details =  users.getUser(member)
						print user_details["username"]
			action = raw_input("\n1: Continue \n:")
			while action != "1":
				action = raw_input("Try again:\n1: Continue \n:")
			if action == "1":
				menu()

		# Print users
		elif selection == "5":
			showUsers()

		# View unallocated users
		elif selection == "6":
			user_type = raw_input("\n S: Staff \n F: Fellow \n C: Cancel \n:").upper()
			while user_type != "F" and user_type != "S" and user_type != "C":
				user_type = raw_input("Try again.\nS: Staff \nF: Fellow \n C: Cancel \n:").upper()

			if user_type == "C":
				menu()
			else:
				users = user.User()
				users.view_unallocated(user_type)
			action = raw_input("\n1: Continue \n:")
			while action != "1":
				action = raw_input("Try again:\n1: Continue \n:")
			if action == "1":
				menu()

		# Allocate rooms
		elif selection == "7":
			user_type = raw_input("\n S: Staff \n F: Fellow \n C: Cancel \n:").upper()
			while user_type != "F" and user_type != "S" and user_type != "C":
				user_type = raw_input("Try again.\nS: Staff \nF: Fellow \n C: Cancel \n:").upper()

			if user_type == "C":
				menu()
			else:
				#allocate = allocation.Allocation()
				allocateAll(user_type)
			action = raw_input("\n1: Continue \n:")
			while action != "1":
				action = raw_input("Try again\n1: Continue \n:")
			if action == "1":
				menu()

		#Display available spaces per room
		elif selection == "8":
			space = room.Room()
			print "\n"
			print "AVAILABLE OFFICE SPACES"
			print "*****************************************************"
			availableOffices = space.available("O")
			for each in availableOffices:
				details = space.getRoom(each)
				av = 6 - len(details["occupants"])
				print details["name"] + ": " + str(av) + " Spaces"
			print "\n"
			print "AVAILABLE LIVING SPACES"
			print "*****************************************************"
			availableLiving = space.available("L")
			for each in availableLiving:
				details = space.getRoom(each)
				av = 4 - len(details["occupants"])
				print details["name"] + ": " + str(av) + " Spaces"
			action = raw_input("\n1: Continue \n:")
			while action != "1":
				action = raw_input("Try again\n1: Continue \n:")
			if action == "1":
				menu()

		#Reset data files
		elif selection == "9":
			print ("This will delete the user and room data in the system.")
			print ("Are you sure you want to continue?")
			action = raw_input("\n1: Yes \n2: Cancel\n:")
			while action != "1" and action != "2":
				action = raw_input("Try again\n1: Yes \n2: Cancel\n:")
			if action == "1":
				os.remove(user_data)
				os.remove(room_data)
				os.remove(alloc_data)
				print("Files Removed!")
				check_files()
				menu()
			elif action == "2":
				menu()

		elif selection == "10":
			break

		else:
			selection = home()


menu()

import os
import unittest
import json
import random
from checkpoint1.room import Room
from checkpoint1.user import User


class TestAppMethods(unittest.TestCase):

	'''
	This class tests the methods implemented which are expected to return data
	or write to files
	'''

	@classmethod
	def setUpClass(cls):
		'''
		 Setup the testing class
		'''
		cls.room_inst = Room(os.path.dirname(os.path.abspath(__file__)))
		cls.test_users = User(os.path.dirname(os.path.abspath(__file__)))
		d_path = os.path.dirname(os.path.abspath(__file__))
		user_data = os.path.join(d_path, "data/users.json")
		room_data = os.path.join(d_path, "data/rooms.json")
		alloc_data = os.path.join(d_path, "data/Allocations.txt")

		with open(user_data, 'w+') as file:
			# Initialize test user data into data files
			data = {
				"users": {
					"fellows": {
						"tes23": {
							"accomodation": "Y",
							"username": "Test User"
						}
					},
					"staff": {
						"tes24": {
							"accomodation": "N/A",
							"username": "Test Staff"
						}
					}
				}
			}
			file.write(json.dumps(data, indent=4, sort_keys=True))

		with open(room_data, "w+") as file:
			# Initialize test room data into data files
			data = {
				"rooms": {
					"living": {
						"roo12": {
							"name": "Room Test",
							"occupants" : []
						}
					},
					"office": {
						"off13": {
							"name": "office Test",
							"occupants" : []
						}
					}
				}
			}
			file.write(json.dumps(data, indent=4, sort_keys=True))

		with open(alloc_data, 'w+') as file:
			pass


	def test_save_room(self):
		'''
		 Tests the function saving rooms adds one room to the data file
	 	'''
		count_before = len(self.room_inst.rooms("O")) + len(self.room_inst.rooms("L"))
		self.room_inst.room_type = "O"
		self.room_inst.name = "Room Testing"
		self.room_inst.room_id = "rid01"
		self.room_inst.saveRoom()
		count_after = len(self.room_inst.rooms("O")) + len(self.room_inst.rooms("L"))
		self.assertGreater(count_after, count_before)

	def test_rooms_list(self):
		''' 
		Tests that the rooms function returns a list of all room IDs given
	 	the room type. (In this case O is passed for Offices)		'''
		room_list = self.room_inst.rooms("O")
		self.assertIsInstance(room_list, list)

	def test_available_rooms(self):
		''' 
		Tests the function checking for available rooms 
		'''
		available_rooms = self.room_inst.available("O")
		self.assertIsInstance(available_rooms, list)

	
	def test_get_room(self):
		'''
		Tests the function getRoom which returns the details of a given room
		'''
		get_room = self.room_inst.getRoom("rid01")
		self.assertIsInstance(get_room, dict)

	def test_room_members(self):
		'''
		Tests the function that returns the members of a given room
		'''
		room_members = self.room_inst.members("use12", "L")
		self.assertIsInstance(room_members, list)

	def test_unallocated(self):
		'''
		Tests that the function returns a dictionary of unallocated users
		'''
		unallocated_users = self.test_users.unallocated("F")
		self.assertIsInstance(unallocated_users, dict)

	def test_allocate(self):
		'''
		Tests allocation adds one member to a given room
		'''
		unallocated = self.test_users.unallocated("F")
		available_rooms = self.room_inst.available("O")
		rand_room = random.choice(available_rooms)
		before_allocation = self.room_inst.members(rand_room, "O")
		self.room_inst.addMember(rand_room, "O", unallocated["office"][0])
		after_allocation = self.room_inst.members(rand_room, "O")
		self.assertGreater(after_allocation, before_allocation)
		self.assertEqual(len(after_allocation), len(before_allocation) + 1)

	def test_save_user(self):
		'''
		 Tests the function saving users adds one user to the data file
	 	'''
		count_before = len(self.test_users.users("F")) + len(self.test_users.users("S"))
		self.test_users.user_type = "F"
		self.test_users.user_name = "User Testing"
		self.test_users.accomodation = "Y"
		self.test_users.user_id = "use12"
		self.test_users.saveUser()
		count_after = len(self.test_users.users("F")) + len(self.test_users.users("S"))
		self.assertGreater(count_after, count_before)

	def test_user_list(self):
		'''
		 Tests the user list function returns the same data type for 
		 both types of users
	 	'''
		fellow_list = self.test_users.users("F")
		staff_list = self.test_users.users("S")
		self.assertEqual(type(fellow_list), type(staff_list))

	def test_get_user(self):
		'''
		Tests the user ID from getUser() function is in the list of 
		users in the system
		'''
		fellow_list = self.test_users.users("F")
		get_user = self.test_users.getUser(fellow_list[0])
		self.assertIn(get_user["userID"], fellow_list)


if __name__ == '__main__':
	unittest.main()

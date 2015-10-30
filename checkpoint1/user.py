import json
import random
import os


class User(object):
    '''
    The User class defines the data and methods used in the system 
    that are related to users
    '''

    def __init__(self, d_path=os.path.dirname(os.path.abspath(__file__))):
        self.user_type = ""
        self.user_name = ""
        self.accomodation = ""
        self.user_id = ""
        self.d_path = d_path
        self.user_data = os.path.join(self.d_path, "data/users.json")
        self.room_data = os.path.join(self.d_path, "data/rooms.json")

    def saveUser(self):
        '''
        Save user to data file
        '''
        tosave = {"username": self.user_name, "accomodation": self.accomodation}
        with open(self.user_data, "r+") as data_file:
            data = json.load(data_file)
            user_names = []
            if self.user_type == "F":
                fellow_list = self.users("F")
                for each_user in fellow_list:
                    user_details = self.getUser(each_user)
                    user_names.append(user_details["username"])
                if self.user_name not in user_names:
                    data["users"]["fellows"][self.user_id] = tosave
                    print "Member " + self.user_name + " added to the system"
                else:
                    print "The member " + self.user_name + " is currently in the system"
            elif self.user_type == "S":
                staff_list = self.users("S")
                for each_user in staff_list:
                    user_details = self.getUser(each_user)
                    user_names.append(user_details["username"])
                if self.user_name not in user_names:
                    data["users"]["staff"][self.user_id] = tosave
                    print "Member " + self.user_name + " added to the system"
                else:
                    print "The member " + self.user_name + " is currently in the system"
            data_file.seek(0)
            data_file.write(json.dumps(data, indent=4, sort_keys=True))


    def addUser(self):
        '''
        Add user data manually
        '''
        user_type = raw_input(
            "User Type? Enter S for staff and F for fellow: \n").upper()

        while user_type != "F" and user_type != "S":
            user_type = raw_input(
                "Try again. Enter S for staff and F for fellow: \n").upper()

        name = raw_input("Enter name: \n").upper()

        if user_type == "F":
            accomodation = raw_input(
                "Does the fellow need living space? (Y or N): \n").upper()
            while accomodation != "Y" and accomodation != "N":
                accomodation = raw_input(
                    "Try again. Allocate living space? (Y or N): \n").upper()

        elif user_type == "S":
            accomodation = "N/A"

        self.user_type = user_type
        self.user_name = name
        self.accomodation = accomodation
        self.user_id = self.user_name[
            0:3].lower() + str((random.randint(10, 100)))

        self.saveUser()

    def unallocated(self, user_type):
        '''
        Returns a list of unallocated users
        '''
        office = []
        living = []
        with open(self.user_data, 'r') as f:
            data = json.load(f)
            if user_type == "F":
                users = data["users"]["fellows"]
                for key in users:
                    if "office" not in users[key] or users[key]["office"] == "":
                        office.append(key)

                    if "living" not in users[key] or users[key]["living"] == "":
                        living.append(key)
                userlist = {"office": office, "living": living}

            elif user_type == "S":
                users = data["users"]["staff"]
                for key in users:
                    if "office" not in users[key] or users[key]["office"] == "":
                        office.append(key)

                userlist = {"office": office}
        return userlist

    def view_unallocated(self, user_type):
        '''
        View users yet to be allocated either a living space or an office space
        '''
        os.system('clear')
        to_print = self.unallocated(user_type)
        if user_type == "F":
            print "FELLOWS"
            print "********************************************************************"
            print "To Allocate Living Space"
            living = to_print["living"]
            for item in living:
                user_details = self.getUser(item)
                if user_details["accomodation"] == "Y":
                    print user_details["username"]
            print "\n"
        if user_type == "S":
            print "STAFF"
            print "********************************************************************"
        print "To Allocate Office Space"
        office = to_print["office"]
        for member in office:
            user_details = self.getUser(member)
            print user_details["username"]

    def listUsers(self, user_type):
        '''
        Display all users
        '''
        userlist = "Name\t User Type \t\t Living Space\n"
        with open(self.user_data, 'r') as f:
            data = json.load(f)
            if user_type == "F":
                users = data["users"]["fellows"]
                utype = "Fellow"
            elif user_type == "S":
                users = data["users"]["staff"]
                utype = "Staff"

        for key in users:
            userlist = userlist + \
                users[key]["username"] + "\t\t" + user_type + \
                "\t" + users[key]["accomodation"] + "\t"

            userlist = userlist + "\n"
        return userlist

    def users(self, user_type):
        '''
        Return a list of all users of a given type (Either fellow or staff)
        '''
        user_ids = []
        with open(self.user_data, 'r') as f:
            data = json.load(f)
            if user_type == "F":
                users = data["users"]["fellows"]
            elif user_type == "S":
                users = data["users"]["staff"]

        for key in users:
            user_ids.append(key)

        return user_ids

    def getUser(self, user_id):
        '''
        Get details of a given user
        '''
        userlist = {}
        with open(self.user_data, 'r') as f:
            data = json.load(f)
            users1 = data["users"]["fellows"]
            users2 = data["users"]["staff"]
        userlist["userID"] = user_id
        if user_id in users1:
            for each, value in users1[user_id].iteritems():
                userlist[each] = value
        if user_id in users2:
            for each, value in users2[user_id].iteritems():
                userlist[each] = value
        return userlist

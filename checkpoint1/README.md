# Checkpoint 1
A room allocation system for (Amity)

## Usage Instructions:
* Install Python
* Download or clone the source files
* run `python main.py` from the terminal inside `checkpoint1`

### Adding users
Users can be added either by entering data manually or using a text file.
The text file should be in the format:

`full names \t user_type \t accomodation`

The user type should be either `F` for Fellow or `S` for staff

Accomodation should be either `Y` or `N` for fellows and blank or `N/A` for staff

### Adding rooms
Rooms can be added either by entering data manually or using a text file.

The text file should be in the format:

`room name \t room_type`

The room type should be either `L` for living space or `O` for office space

*Both the user and room details files should be placed inside the `data` directory.*
*Sample files are included*

###Room Allocation
To allocate living and office space to users their details must first be added to the system

Allocation is done randomly, and at once for all unallocated users

### Viewing stored data
One can view:
 - All allocations
 - Allocations per room
 - All users in the system
 - Users pending space allocation
 - Available rooms (spaces)

### Tests
Run `pip install nose`

Run `nosetests` while in the `checkpoints1` directory

## Known Issues
 - The Exit functionality doesn't run after any other option is selected

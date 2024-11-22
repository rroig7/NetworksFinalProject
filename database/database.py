import json

databaseFile = "server/users.json"

def saveUser(user):

    users = loadUsers()

    users.append(user)

    with open(databaseFile, "w") as file:
        json.dump(users, file, indent=4)

def loadUsers():
    with open(databaseFile, "r") as file:
        users = json.load(file)
        return users


def checkForExistingUser(username):
    # Iterate through the list of users to find a match
    for user in loadUsers():
        if user['username'] == username:
            return user  # Return the matching user dictionary
    return None  # Return None if no matching user is found

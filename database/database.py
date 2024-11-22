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
    return any(user['username'] == username for user in loadUsers())

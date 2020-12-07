from socket import socket, AF_INET, SOCK_DGRAM

s = socket(AF_INET, SOCK_DGRAM)
source_ip = '127.0.0.1'
source_port = 12345
s.bind((source_ip, source_port))
usersAddress = {}
usersMessages = {"": []}
while True:
    # server recieves message and server info
    data, sender_info = s.recvfrom(2048)
    dataD = data.decode()
    # if user wants to sign in
    if dataD[0] == '1':
        userAlreadyExists = '0'
        # check if user already exists
        for key in usersAddress:
            if usersAddress.get(key) == sender_info:
                userAlreadyExists = '1'
                s.sendto("User already exists .".encode(), sender_info)
        # if user doesn't exist , add him
        if userAlreadyExists == '0':
            message = ""
            print("Message:", dataD[2:], "from:", sender_info)
            if len(dataD) == 1:
                s.sendto("Invalid input".encode(), sender_info)
            currentUsersInChat = ""
            name = dataD[2:]
            usersAddress[name] = sender_info
            if name not in usersMessages:
                usersMessages[name] = []
            for key in usersAddress:
                if key != name:
                    currentUsersInChat += key + ", "
            # print users in chat
            if currentUsersInChat != "":
                s.sendto(("Current users in chat: " + (currentUsersInChat[:(len(currentUsersInChat) - 2)])).encode(),
                         sender_info)
            # inform everyone that new user joined
            for key in usersAddress:
                if key != name:
                    message = name + " has joined."
                    usersMessages.get(key).append(message)
        s.sendto("halt".encode(), sender_info)
    # if user wants to send message
    if dataD[0] == '2':
        userName = ""
        message = ""
        content = dataD[2:]
        print("Message: ", dataD, "from:", sender_info)
        # check if user exists
        for key in usersAddress:
            if usersAddress.get(key) == sender_info:
                userName = key
        # user doesn't exist
        if userName == "":
            s.sendto("User does not exists .".encode(), sender_info)
        else:
            for key in usersAddress:
                if usersAddress.get(key) != sender_info:
                    message = userName + " sent: " + content
                    usersMessages[key] += [message]
    # if user wants to change name
    if dataD[0] == '3':
        userName = ""
        message = ""
        newName = dataD[2:]
        tempName = ""
        print("Message: ", dataD, "from:", sender_info)
        # check if user exists
        for key in usersAddress:
            if usersAddress.get(key) == sender_info:
                userName = key
        # user doesnt exist
        if userName == "":
            s.sendto("User does not exists .".encode(), sender_info)
        elif len(dataD) == 1:
            s.sendto("Invalid Input".encode(), sender_info)
        else:
            for key in usersAddress:
                if usersAddress.get(key) == sender_info:
                    tempName = key
                    usersAddress[newName] = usersAddress[key]
                    usersMessages[newName] = usersMessages[key]
                    break
            if tempName is not "":
                del usersAddress[tempName]
                del usersMessages[tempName]
            message = tempName + " changed his name to: " + newName
            for key in usersAddress:
                if usersAddress.get(key) != sender_info:
                    usersMessages.get(key).append(message)
    # if user wants to delete himself
    if dataD[0] == '4':
        tempName = ""
        message = ""
        userName = ""
        print("Message: ", dataD, "from:", sender_info)
        # check if user exists
        for key in usersAddress:
            if usersAddress.get(key) == sender_info:
                userName = key
        # user doesnt exist
        if userName == "":
            s.sendto("User does not exists .".encode(), sender_info)
        else:
            for key in usersAddress:
                if usersAddress.get(key) == sender_info:
                    tempName = key
            del usersAddress[tempName]
            del usersMessages[tempName]
            message = tempName + " has left the chat"
            for key in usersMessages:
                usersMessages.get(key).append(message)
            s.sendto("halt".encode(), sender_info)
    # user wants to get updates
    if dataD[0] == '5' or dataD[0] == '2' or dataD[0] == '3':
        name = ""
        userName = ""
        for key in usersAddress:
            if usersAddress.get(key) == sender_info:
                userName = key
        if userName == "":
            s.sendto("User does not exists .".encode(), sender_info)
        else:
            for key in usersAddress:
                if usersAddress.get(key) == sender_info:
                    inbox = usersMessages.get(key)
                    name = key
                    for msg in inbox:
                        s.sendto(msg.encode(), sender_info)
                    break
            usersMessages[name] = []
        s.sendto("halt".encode(), sender_info)
    if dataD[0] != '1' and dataD[0] != '2' and dataD[0] != '3' and dataD[0] != '4' and dataD[0] != '5':
        s.sendto("Bad input, please try again".encode(), sender_info)
        s.sendto("halt".encode(), sender_info)


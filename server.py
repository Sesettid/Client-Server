import socket
import sys

newDict = {}


def start_server(customers_dict):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)
    sock.listen(1)

    while True:
        print(sys.stderr, 'waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print(sys.stderr, 'connection from', client_address)

            while True:
                value = ""
                data = connection.recv(40)
                print(sys.stderr, 'received "%s"' % data.decode())
                rec_message = data.decode()
                choice = rec_message.split(',')

                if choice[0] == "1":
                    if choice[1] in newDict.keys():
                        value = newDict[choice[1]]
                    else:
                        value = "Customer not found"
                elif choice[0] == "2":
                    if choice[1] in newDict.keys():
                        value = "Customer already exists"
                    else:
                        newDict[choice[1]] = choice[2]
                        value = "Customer added successfully"
                elif choice[0] == "3":
                    if choice[1] in newDict.keys():
                        del newDict[choice[1]]
                        value = "Customer deleted"
                    else:
                        value = "Customer does not exist"
                elif choice[0] == "4":
                    if choice[1] in newDict.keys():
                        value = newDict[choice[1]]
                        index = value.index("|")
                        new_value = str(choice[2]) + value[index:]
                        newDict[choice[1]] = new_value
                        value = new_value
                    else:
                        value = "Customer does not exist"
                elif choice[0] == "5":
                    if choice[1] in newDict.keys():
                        value = newDict[choice[1]]
                        index = value.rindex("|")
                        new_value = value[:value.index('|') + 1] + str(choice[2]) + value[index:]
                        newDict[choice[1]] = new_value
                        value = new_value
                elif choice[0] == "6":
                    if choice[1] in newDict.keys():
                        value = newDict[choice[1]]
                        index = value.rindex("|")
                        new_value = value[:index + 1] + str(choice[2])
                        newDict[choice[1]] = new_value
                        value = new_value
                elif choice[0] == "7":
                    value = ""
                    s = [(key, newDict[key]) for key in sorted(newDict)]
                    for list in s:
                        value = value + ':' + str(list)

                if value:
                    print(sys.stderr, 'sending data back to the client')
                    connection.sendall(value.encode())
                else:
                    print(sys.stderr, 'no more data from', client_address)
                    break

        finally:
            connection.close()


def create_dict_from_file():
    with open("data.txt", "r+") as infile:
        for line in infile:
            line = line.strip()
            val = line.split("|", 1)[0]
            newDict[val] = line.split("|", 1)[1]

    return newDict


if __name__ == '__main__':
    customers_dict = create_dict_from_file()
    start_server(customers_dict)

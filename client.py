import socket
import sys


def print_menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. Find customer")
    print("2. Add customer")
    print("3. Delete customer")
    print("4. Update customer age")
    print("5. Update customer address")
    print("6. Update customer phone")
    print("7. Print report")
    print("8. Exit")
    print(67 * "-")

    choice = input("Enter your choice [1-8]: ")
    choice = int(choice)
    return choice


def perform_actions(choice):
    if choice == 1:
        print("Choice 1 has been selected")
        name = input("Enter the name to find:")
        return "1," + name

    elif choice == 2:
        print("Choice 2 has been selected")
        name = input("Enter the customer to be added")
        age = int(input("Enter the age of the customer"))
        address = input("Enter the address of the customer")
        phone = int(input("Enter the number"))

        return "2," + name + "," + str(age) + "|" + address + "|" + str(phone)

    elif choice == 3:
        print("Choice 3 has been selected")
        name = input("Enter the customer name to be deleted")
        return "3," + name

    elif choice == 4:
        print("Choice 4 has been selected")
        name = input("Enter the customer name to be updated")
        age = int(input("Enter the new age to be updated"))
        return "4," + name + "," + str(age)

    elif choice == 5:
        print("Choice 5 has been selected")
        name = input("Enter the customer name to be updated")
        address = input("Enter the new address to be updated")
        return "5," + name + "," + address

    elif choice == 6:
        print("Choice 6 has been selected")
        name = input("Enter the customer name to be updated")
        phone = input("Enter the new phone number to be updated")
        return "6," + name + "," + str(phone)

    elif choice == 7:
        print("Choice 7 has been selected")
        return "7,"

    else:
        print("Wrong choice selection. Enter any key to try again..")


def create_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    print(sys.stderr, 'connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:
        loop = True
        while loop:
            choice = print_menu()
            if choice == 8:
                print("Good Bye")
                loop = False

            elif choice == 7:
                message = perform_actions(choice)
                sock.sendall(message.encode())

                amount_received = 0
                amount_expected = len(message)

                while amount_received < amount_expected:
                    data = sock.recv(3000)
                    response_message = data.decode()
                    amount_received += len(response_message)
                    rows = response_message.split(':')
                    for records in rows:
                        if records:
                            print(records)
                    break
            elif 0 < choice < 7:
                message = perform_actions(choice)
                sock.sendall(message.encode())

                amount_received = 0
                amount_expected = len(message)

                while amount_received < amount_expected:
                    data = sock.recv(3000)
                    response_message = data.decode()
                    amount_received += len(response_message)
                    print('Received data is "%s"' % response_message)
                    break
            else:
                print("Invalid choice")

    finally:
        print(sys.stderr, 'closing socket')
        sock.close()


if __name__ == '__main__':
    create_client()

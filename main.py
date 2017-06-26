from steganography.steganography import Steganography  # to read secret messeges

from spy_details1 import spy, Spy, ChatMessage, friends

from termcolor import colored

from colorama import init

from datetime import datetime

init()

print colored("hello","red")


STATUS_MESSAGES = ['My name is Bond, James Bond', 'Shaken, not stirred.', 'Keeping the British end up, Sir']

question= "Do you want to continue as " + spy.salutation + " " + spy.name + " (Y/N)? "     # String Concatenation using + symbol
ans = raw_input(question.upper())  #raw_input always gives us a string

def add_status():     #defining add_status() function to update a new status

    updated_status_message = None

    if spy.current_status_message != None:

        print 'Your current status message is %s \n' % (spy.current_status_message)
    else:
        print 'You don\'t have any status message currently \n'

    default = raw_input("Do you want to select from the older status (y/n)? ")    #asking to whether to continue with the older one

    if default.upper() == "N":
        new_status_message = raw_input("What status message do you want to set? ")


        if len(new_status_message) > 0:
            STATUS_MESSAGES.append(new_status_message)     #new status message has been added succesfully
            updated_status_message = new_status_message    # new_status_message updated

    elif default.upper() == 'Y':

        item_position = 1

        for message in STATUS_MESSAGES:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1

        message_selection = int(raw_input("\nChoose from the above messages "))    #to choose messages fro above defined messages


        if len(STATUS_MESSAGES) >= message_selection:
            updated_status_message = STATUS_MESSAGES[message_selection - 1]

    else:
        print 'The option you chose is not valid! Press either y or n.'

    if updated_status_message:
        print 'Your updated status message is: %s' % (updated_status_message)
    else:
        print 'You current don\'t have a status update'

    return updated_status_message


def add_friend():     # this function is defined to a add a new friend to the list

    new_friend = Spy('','',0,0.0)

    new_friend.name = raw_input("Please add your friend's name: ")
    new_friend.salutation = raw_input("Are they Mr. or Ms.?: ")

    new_friend.name = new_friend.salutation + " " + new_friend.name

    new_friend.age = raw_input("Age?")
    new_friend.age = int(new_friend.age)

    new_friend.rating = raw_input("Spy rating?")
    new_friend.rating = float(new_friend.rating)

    if len(new_friend.name) > 0 and new_friend.age > 12 and new_friend.rating >= spy.rating:   # specific conditions are provided which are checked first
        friends.append(new_friend)
        print 'New Friend Added!'
    else:
        print 'Sorry! Invalid entry. We can\'t add spy with the details you provided'

    return len(friends)


def select_a_friend():     # to select a friend whom we want to send a message or from whom we want to recieve a message
    item_number = 0

    for friend in friends:
        print '%d. %s %s aged %d with rating %.2f is online' % (item_number +1, friend.salutation, friend.name,
                                                   friend.age,
                                                   friend.rating)
        item_number = item_number + 1

    friend_choice = raw_input("Choose from your friends")

    friend_choice_position = int(friend_choice) - 1

    return friend_choice_position


def send_message():   # this function is defined to send a message to a friend

    friend_choice = select_a_friend()

    original_image = raw_input("What is the name of the image?")
    output_path = "output.jpg"
    text = raw_input("What do you want to say? ")
    Steganography.encode(original_image, output_path, text)

    new_chat = ChatMessage(text,True)

    friends[friend_choice].chats.append(new_chat)

    print "Your secret message image is ready!"


def read_message():                                    # this function is defined to read a message sent by a friend


    dict_special_words={'asap':'as soon as possible','lol':'laugh out loud','gtg':'got to go'}

    sender = select_a_friend()

    output_path = raw_input("What is the name of the file?")

    secret_text = Steganography.decode(output_path)

    new_chat = ChatMessage(secret_text,False)

    if len(secret_text.split())>50:                    # Checking if the friend spoke more than 50 word
        friends.remove(friends[sender])                # Deleting the friend if he spoke more than 50 words
    elif len(secret_text)==0 :                         # Checking if the image contains any text or not
        print ('there is no secret text in your image')
    else:
        for word in dict_special_words.keys():         # Checking special words
            found=secret_text.find(word)               # Checking if the the Secret_text contains special words or not
            if found!=-1:
                print(word + '=' + dict_special_words[word])


        friends[sender].chats.append(new_chat)
        print secret_text
        print "Your secret message has been saved!"



def read_chat_history(): # this function is defined to read the chat history of a particular friend

    read_for = select_a_friend()

    print '\n6'

    for chat in friends[read_for].chats:
        if chat.sent_by_me:
            print '[%s] %s: %s' % (chat.time.strftime("%d %B %Y"), 'You said:', chat.message)
        else:
            # Adding colors to time, friend and secret_text
            print '[%s] %s said: %s' % (colored(chat.time.strftime("%d %B %Y"),"red","on_blue"), colored(friends[read_for].name, "green","on_red"), colored(chat.message, "blue","on_green"))


def start_chat(spy):

    spy.name = spy.salutation + " " + spy.name


    if spy.age > 12 and spy.age < 50:


        print "Authentication complete. Welcome " + spy.name + " age: " \
              + str(spy.age) + " and rating of: " + str(spy.rating) + " Proud to have you onboard"

        show_menu = True

        while show_menu:
            # a menu is made from which user selects an option
            menu_choices = "What do you want to do? \n 1. Add a status update \n 2. Add a friend \n 3. Send a secret message \n 4. Read a secret message \n 5. Read Chats from a user \n 6. Close Application \n"
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)

                if menu_choice == 1:
                    spy.current_status_message = add_status()
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'You have %d friends' % (number_of_friends)
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                elif menu_choice == 5:
                    read_chat_history()
                else:
                    show_menu = False
    else:
        print 'Sorry you are not of the correct age to be a spy'

if ans.upper()== "Y":
    start_chat(spy)
else:

    spy = Spy('','',0,0.0)


    spy.name = raw_input("Welcome to spy chat, you must tell me your spy name first: ")

    if len(spy.name) > 0:            #spy name's length is checked
        spy.salutation = raw_input("Should I call you Mr. or Ms.?: ")

        spy.age = raw_input("What is your age?")
        spy.age = int(spy.age)

        spy.rating = raw_input("What is your spy rating?")
        spy.rating = float(spy.rating)
        if spy.rating>=5:
            print "AWESOME!!"
        elif spy.rating>=4:
            print "good"
        else:
            print "AVERAGE"

        start_chat(spy)
    else:
        print 'Please add a valid spy name'
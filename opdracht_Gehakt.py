import os

#User input requested
user_input = input("Voer de master directory in: ")

def file_list(input):
    #Dictionary om alle files met hashes erbij op te slaan
    file_dict = {}
    hashie = 0
    # Loop die een variabele met het path naar een file update zodat iedere file in de directory wordt afgelopen.
    # Vervolgens worden de subdir en de file gejoind in de variabele current_dir
    # Hierna wordt een betreffende directory meegegeven aan een splitext commando die de extensie van de file afhaald
    for subdir, dirs, files in os.walk(user_input):
        for file in files:
            current_dir = (os.path.join(subdir, file))
            filename, file_extension = os.path.splitext(current_dir)
            file_dict[filename] = {"Extension":file_extension, "Hash value":hashie}
            print(file_dict)

file_list(user_input)
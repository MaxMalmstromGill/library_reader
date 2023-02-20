def string_to_secounds(s):
    result = 0
    if ":" not in s:
        # If there is no colon in the string, it raises a ValueError indicating that the string is not in the correct format.
        raise ValueError("Input string must be in minute-second format.")
    else:
        seperated = s.split(":")
        if int(seperated[0]) >= 0:
            # If the first element of the split string is a positive integer, it is multiplied by 60 to convert to seconds and added to the result.
            result += int(seperated[0]) * 60
        if 0 <= int(seperated[1]) < 60:
            # If the second element of the split string is a positive integer between 0 and 59, it is added to the result.
            result += int(seperated[1])   

    return result


def read_library(filename):
    try:
        with open(filename, 'r') as file:
            library = {}
            for line in file:
                try:
                    # Each line is split by the comma and assigned to the variables 'artist', 'song', and 'time'.
                    artist, song, time = line.strip().split(',')
                    # The 'time' string is split by colon and converted to integers for minutes and seconds.
                    minutes, seconds = map(int, time.split(':'))
                    duration = minutes * 60 + seconds
                    if artist in library:
                        # If the artist already exists in the library dictionary, the song is added as a key to the artist's dictionary.
                        library[artist][song] = duration
                    else:
                        # If the artist does not exist in the library dictionary, a new dictionary for the artist is created with the song as a key.
                        library[artist] = {song: duration}
                except ValueError:
                    # If there is a ValueError in splitting the line, it raises a ValueError indicating that the line is malformed.
                    raise ValueError(f"Line '{line.strip()}' in file '{filename}' is malformed.")
            return library
    except FileNotFoundError:
        # If the file cannot be found, it raises a FileNotFoundError indicating the file does not exist.
        raise FileNotFoundError(f"File '{filename}' does not exist.")


def print_library(library):
    result = ""
    total_time = 0
    total_songs = 0
    # Loop through the library to get information about each artist and their songs
    for artist in library:
        artist_time = 0
        for song, time in library[artist].items():
            artist_time += time
            total_time += time
            total_songs += 1
        # Format the artist information to add to the result string
        result += artist + " (" + str(len(library[artist])) + " songs, " + str(artist_time // 60) + ":" + str(artist_time % 60) + ")\n"
        # Loop through the artist's songs to add them to the result string
        for song, time in library[artist].items():
            result += "- " + song + "(" + str(time) + ")\n"
    # Add the total number of songs and total time to the result string
    result += "Total: " +  str(total_songs) + " songs, " + str(total_time // 60) + ":" + str(total_time % 60)
    return result


# Function to create a playlist based on a given theme
def make_playlist(library, theme):
    result = []
    match_found = False
    theme = theme.lower()
    # Loop through the library to find songs with the specified theme
    for artist in library:
        for song, time in library[artist].items():
            if theme in song.lower():
                match_found = True
                result.append("(" + artist + ", " + song + ", " + str(time) + ")" )
    
    # Raise an error if no song matches the specified theme
    if not match_found:
        raise ValueError("No song matched the theme")
    return result


# Function to write the playlist to a file
def write_playlist(playlist, filename):
    with open(filename, 'w') as file:
        # Loop through the playlist to write each song to the file
        for song in playlist:
            file.write(song + '\n')


def main():
    #Variable filename is initialized to empty string
    filename = ""
    
    #loop to repeatedly ask the user to enter a filename until a valid file name is entered
    while not filename:
        filename = input("Which music library do you want to load? ")
        try:
            library = read_library(filename)
            break
        except FileNotFoundError:
            print("That file does not exist.")
            filename = ""
    print(print_library(library))
    
    theme = ""
    
    #loop to repeatedly ask the user to enter a theme until a valid theme is entered
    while not theme:
        theme = input("Enter a playlist theme: ")
        try:
            playlist = make_playlist(library, theme)
            break
        except ValueError:
            print("No song matched the theme. Please try again.")
            theme = ""

    print(playlist)
    
    save = ""
    #loop to repeatedly ask the user to enter a save location until a valid location is entered
    while not save:
        save = input("Where do you want to save the playlist? ")
        try:
            write_playlist(playlist, save)
            break
        except:
            print("Error saving the file. Please try again.")
            save = ""
    print("Saved, Goodbye!")

main()

import json
import os

FILE = "music-playlist/playlist.json"

def load_playlist():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save_playlist(playlist):
    with open(FILE, "w") as f:
        json.dump(playlist, f, indent=2)

def add_song(title, artist, genre):
    playlist = load_playlist()
    playlist.append({"title": title, "artist": artist, "genre": genre})
    save_playlist(playlist)

def search_by_artist(artist):
    playlist = load_playlist()
    return [song for song in playlist if song["artist"].lower() == artist.lower()]

def delete_song(title):
    playlist = load_playlist()
    playlist = [song for song in playlist if song["title"].lower() != title.lower()]
    save_playlist(playlist)

def update_song(title, new_title=None, new_artist=None, new_genre=None):
    playlist = load_playlist()
    for song in playlist:
        if song["title"].lower() == title.lower():
            if new_title:
                song["title"] = new_title
            if new_artist:
                song["artist"] = new_artist
            if new_genre:
                song["genre"] = new_genre
            break
    save_playlist(playlist)

def show_playlist():
    playlist = load_playlist()
    if not playlist:
        print("No songs in the playlist.")
    else:
        for song in playlist:
            print(f"Title: {song['title']}, Artist: {song['artist']}, Genre: {song['genre']}")

def main():
    print("Music Playlist Manager ")
    print("Commands: add, search, delete, update, show, quit")
    while True:
        cmd = input("Command: ").lower()
        if cmd == "quit":
            break
        elif cmd == "add":
            title = input("Title: ")
            artist = input("Artist: ")
            genre = input("Genre: ")
            add_song(title, artist, genre)
        elif cmd == "search":
            artist = input("Artist: ")
            results = search_by_artist(artist)
            if results:
                for song in results:
                    print(f"Found: {song['title']} by {song['artist']}")
            else:
                print("No songs found.")
        elif cmd == "delete":
            title = input("Title to delete: ")
            delete_song(title)
        elif cmd == "update":
            title = input("Title to update: ")
            new_title = input("New Title (leave blank to keep current): ") or None
            new_artist = input("New Artist (leave blank to keep current): ") or None
            new_genre = input("New Genre (leave blank to keep current): ") or None
            update_song(title, new_title, new_artist, new_genre)
        elif cmd == "show":
            show_playlist()
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()

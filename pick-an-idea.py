import os
import random
import subprocess
import sqlite3

def scan_videos(directory, extensions):
    """Recursively scan a directory for video files with specific extensions."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                yield os.path.join(root, file)

def pick_random_video(videos):
    """Pick a random video file from a list."""
    return random.choice(videos)

def save_to_db(db_conn, video_file):
    """Save the picked video filename to the SQLite database."""
    with db_conn:
        db_conn.execute("INSERT INTO picked_videos (filename) VALUES (?)", (video_file,))

def load_picked_videos(db_conn):
    """Load the list of already picked video filenames from the SQLite database."""
    with db_conn:
        return {row[0] for row in db_conn.execute("SELECT filename FROM picked_videos")}

def clear_db(db_conn):
    """Clear the table of picked videos in the SQLite database."""
    with db_conn:
        db_conn.execute("DELETE FROM picked_videos")

def main():
    # Directory to search for video files
    directory = r'C:\Users\LENOVO\Desktop\pick-an-idea\videos-ideas'
    
    # Video file extensions to look for
    extensions = ('.mp4', '.avi', '.mkv')

    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect("picked_videos.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS picked_videos (
            id INTEGER PRIMARY KEY,
            filename TEXT UNIQUE
        )
    """)

    # Scan the directory for video files
    all_videos = list(scan_videos(directory, extensions))

    # Load already picked video filenames from the database
    picked_videos = load_picked_videos(conn)

    # Filter out the videos that have already been picked
    remaining_videos = [video for video in all_videos if video not in picked_videos]

    if remaining_videos:
        # Pick a random video from the remaining options
        picked_video = pick_random_video(remaining_videos)
        
        # Save the picked video filename to the database
        save_to_db(conn, picked_video)
        
        # Print the picked video filename
        print("Picked video:", picked_video)
        subprocess.Popen(['explorer', picked_video])


        
    else:
        print("All videos have been picked, clearing the memory...")
        # Clear the database since all videos have been picked
        clear_db(conn)

if __name__ == "__main__":
    main()

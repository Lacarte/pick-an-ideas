# pick-an-ideas

Certainly! Below is a nicely formatted Markdown `README.md` file for the given Python script. This README explains the purpose of the script, its features, how to set it up and run it, and details about the functions it uses:

---

# Video Picker

## Description

This Python script is designed to randomly select a video file from a specified directory and its subdirectories. Once a video is selected, the script logs the name of the picked video and opens it using the default program. The script ensures that a video, once picked, is not picked again by saving its name in an SQLite database. After all videos have been picked, the script clears the database.

## Features

- Scans a specified directory and its subdirectories for video files with certain extensions (`.mp4`, `.avi`, `.mkv`, `.flv` in this example).
- Randomly picks one of the found video files that hasn't been picked before.
- Logs the name of the picked video file.
- Opens the picked video file using the default program.
- Saves the name of the picked video file to an SQLite database to avoid picking it again.
- Clears the SQLite database when all videos have been picked.

## Setup and Run

1. **Python Installation:**
   - Ensure that Python is installed on your system. If not, download and install it from https://www.python.org/downloads/.

2. **Running the Script:**
   - Open your command prompt or terminal.
   - Navigate to the directory where you saved the script.
   - Run the script using the command: `python <script_name>.py`.

3. **Logs:**
   - The script generates logs which are saved in a `logs` directory. The logs contain information about which video was picked, or if all videos have been picked.

## Functions Overview

- `scan_videos(directory, extensions)`: 
  - Scans a given directory recursively for video files with specific extensions.
  - `directory` (str): The directory to search in.
  - `extensions` (tuple): The file extensions to look for.

- `pick_random_video(videos)`: 
  - Randomly selects a video file from a list.
  - `videos` (list): The list of video files to pick from.

- `save_to_db(db_conn, video_file)`:
  - Saves the picked video filename to the SQLite database to avoid picking it again.
  - `db_conn` (sqlite3.Connection): The SQLite database connection.
  - `video_file` (str): The name of the video file to save.

- `load_picked_videos(db_conn)`:
  - Loads the list of already picked video filenames from the SQLite database.
  - `db_conn` (sqlite3.Connection): The SQLite database connection.

- `clear_db(db_conn)`:
  - Clears the table of picked videos in the SQLite database. This function is called when all videos have been picked.
  - `db_conn` (sqlite3.Connection): The SQLite database connection.

## Author

[Lacarte]

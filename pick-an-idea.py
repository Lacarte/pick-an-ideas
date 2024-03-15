import os
import random
import subprocess
import sqlite3
import json
from dotenv import load_dotenv
from utils import setup_loguru_logging, resource_path
import time

# Setup logger
load_dotenv()  # Load environment variables
logger = setup_loguru_logging()

def load_json_config():
    """Load the JSON configuration from the path specified in the .env file."""
    config_path = os.getenv("CONFIG_PATH")
    if not config_path:
        logger.error("CONFIG_PATH not found in .env file.")
        return None

    logger.info(f"Loading JSON config from: {config_path}")
    try:
        path = resource_path(config_path)
        with open(path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            return config
    except Exception as e:
        logger.error(f"Failed to load or parse the JSON config: {e}")
        return None

def list_videos_from_config_all_path(config, extensions=(".mp4", ".avi", ".mkv", ".flv")):
    if not config or "app" not in config or "scan-paths" not in config["app"]:
        logger.error("Invalid or missing JSON configuration for scan paths.")
        return []
    file_list = []
    for item in config["app"]["scan-paths"]:
        path = item.get("path")
        if not path or not os.path.isdir(path):
            logger.info(f"Directory does not exist or is empty: {path}")
            continue
        for ext in extensions:
            file_list.extend([os.path.join(path, f) for f in os.listdir(path) if f.endswith(ext)])
    if not file_list:
        logger.info("No files found with specified extensions in any of the directories.")
    
    logger.info(f"Total files found: {len(file_list)}")
    return file_list

def pick_random_video(videos):
    """Pick a random video file from a list."""
    return random.choice(videos)


def save_to_db(db_conn, video_file):
    """Save the picked video filename to the SQLite database."""
    with db_conn:
        db_conn.execute(
            "INSERT INTO picked_videos (filename) VALUES (?)", (video_file,)
        )

def load_picked_videos(db_conn):
    """Load the list of already picked video filenames from the SQLite database."""
    with db_conn:
        return {row[0] for row in db_conn.execute("SELECT filename FROM picked_videos")}

def clear_db(db_conn):
    """Clear the table of picked videos in the SQLite database."""
    with db_conn:
        db_conn.execute("DELETE FROM picked_videos")


def main():
    extensions = (".mp4", ".avi", ".mkv", ".flv")
    try:
        with sqlite3.connect(resource_path("picked_videos.sqlite")) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS picked_videos (
                    id INTEGER PRIMARY KEY,
                    filename TEXT UNIQUE
                )
            """)

            config = load_json_config()
            if config:
                all_videos = list_videos_from_config_all_path(config, extensions)
                if not all_videos:
                    logger.error("No video files found in the scan paths.")
                    return

                if not all_videos:
                    logger.error("No video files found in the scan paths.")
                    clear_db(conn)  # Clear the database after opening the video
                    return

                picked_videos = {row[0] for row in conn.execute("SELECT filename FROM picked_videos")}
                remaining_videos = [video for video in all_videos if video not in picked_videos]

                # If there's exactly one video, open it, then clear the database
                if len(remaining_videos) == 1:
                    last_video_path = remaining_videos[0]  # This is the only video
                    logger.info(f"one last video remain, opening: {last_video_path}")
                    subprocess.Popen(["explorer", last_video_path])
                    clear_db(conn)  # Clear the database after opening the video
                    return  # Exit the function after handling this case


                if remaining_videos:
                    picked_video = random.choice(remaining_videos)
                    conn.execute("INSERT INTO picked_videos (filename) VALUES (?)", (picked_video,))
                    logger.info(f"Picked video: {picked_video}")
                    subprocess.Popen(["explorer", picked_video])
                else:
                    logger.info("All videos have been picked. Consider clearing the database.")
                    clear_db(conn)  # Clear the database after opening the video
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    time_in_seconds = 17
    while time_in_seconds:
        mins, secs = divmod(time_in_seconds, 60)
        timer = '{:02d}'.format(secs)
        timer = f"\033[92m{timer} seconds\033[0m"  # \033[92m is the escape sequence for light green
        print(timer, end="\r")
        time.sleep(1)
        time_in_seconds -= 1

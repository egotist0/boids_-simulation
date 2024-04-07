import taichi as ti
from BoidSimulation import init, update, render, screen

import cv2
import os
import time
import shutil



def clean_output_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Remove the folder and all its contents
        shutil.rmtree(folder_path)
    # Create the folder again, fresh and empty
    os.makedirs(folder_path, exist_ok=True)
def make_video_from_frames(frame_folder, output_video_file, frame_rate):
    # Get the list of image files
    images = [img for img in os.listdir(frame_folder) if img.endswith(".png")]
    print(len(images))
    images.sort()  # Ensure the images are sorted by name

    # Determine the width and height from the first image
    frame = cv2.imread(os.path.join(frame_folder, images[0]))
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # You can also use 'XVID'. If you want to save in .mp4 format, use 'mp4v'
    out = cv2.VideoWriter(output_video_file, fourcc, frame_rate, (width, height))

    for image in images:
        frame = cv2.imread(os.path.join(frame_folder, image))
        out.write(frame)  # Write out frame to video

    out.release()  # Release everything if job is finished
    cv2.destroyAllWindows()

def create_video():
    video_manager = ti.tools.VideoManager(output_dir="./output", framerate=30, automatic_build=False)

    init()
    for i in range(1000):
        update()
        render()
        img = screen.to_numpy()
        video_manager.write_frame(img)


    # video_manager.make_video(gif=True, mp4=True)
if __name__ == "__main__":
    frame_folder = './output/frames'
    # Ensure the folder is clean before starting the simulation
    clean_output_folder(frame_folder)

    # Proceed with creating your video frames
    create_video()

    # Specify your output video file and frame rate
    output_video_file = 'output_video.mp4'
    frame_rate = 30  # Adjust to your desired frame rate

    # Finally, compile the video from frames
    make_video_from_frames(frame_folder, output_video_file, frame_rate)

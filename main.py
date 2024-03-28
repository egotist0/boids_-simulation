import taichi as ti
from BoidSimulation import init, update, render, screen


def create_video():
    video_manager = ti.tools.VideoManager(output_dir="./output", framerate=20, automatic_build=False)

    init()
    for i in range(500):
        update()
        render()
        img = screen.to_numpy()
        video_manager.write_frame(img)

    # video_manager.make_video(gif=True, mp4=True)
if __name__ == "__main__":
    create_video()


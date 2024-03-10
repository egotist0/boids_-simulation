import taichi as ti

ti.init(arch=ti.gpu)

# Constants
boids_num = 1000
width = 800
height = 450
boids_size = 1
max_speed = 100
neighbor_radius = 8.0
separation_radius = 8.0
alignment_weight = 1.0
cohesion_weight = 1.0
separation_weight = 1.15
dt = 0.05

# Parameters
speeds = ti.Vector.field(2, dtype=ti.f32, shape=boids_num)
positions = ti.Vector.field(2, dtype=ti.f32, shape=boids_num)
screen = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))


@ti.func
def random_range(min, max):
    return ti.random() * (max - min) + min


@ti.kernel
def init():
    for i in range(boids_num):
        speeds[i] = ti.Vector(
            [random_range(-1, 1) * max_speed,
             random_range(-1, 1) * max_speed])
        positions[i] = ti.Vector([ti.random() * width, ti.random() * height])


@ti.kernel
def render():
    # clear screen
    for i, j in screen:
        screen[i, j] = [0.0, 0.0, 0.0]
    # draw boids
    for i in positions:
        s = speeds[i].norm()
        color = ti.Vector([
            abs(speeds[i][0]) / s,
            abs(speeds[i][1]) / s,
            abs(speeds[i][0]) / s
        ])
        for x in range(-boids_size + ti.cast(positions[i][0], ti.i32),
                       boids_size + 1 + ti.cast(positions[i][0], ti.i32)):
            for y in range(-boids_size + ti.cast(positions[i][1], ti.i32),
                           boids_size + 1 + ti.cast(positions[i][1], ti.i32)):
                if 0 <= x < width and 0 <= y < height:
                    screen[x, y] = color


@ti.func
def wrap():
    for i in range(boids_num):
        if positions[i][0] < 0:
            positions[i][0] += width
        elif positions[i][0] > width:
            positions[i][0] -= width
        if positions[i][1] < 0:
            positions[i][1] += height
        elif positions[i][1] > height:
            positions[i][1] -= height


@ti.func
def bounceoff():
    for i in range(boids_num):
        if positions[i][0] < 50:
            speeds[i][0] += 1
        elif positions[i][0] > width - 50:
            speeds[i][0] -= 1
        if positions[i][1] < 50:
            speeds[i][1] += 1
        elif positions[i][1] > height - 50:
            speeds[i][1] -= 1


@ti.kernel
def update():
    for i in range(boids_num):
        # compute neighbors
        neighbors = 0
        cohesion = ti.Vector([0.0, 0.0])
        alignment = ti.Vector([0.0, 0.0])
        separation = ti.Vector([0.0, 0.0])
        for j in range(boids_num):
            if i != j:
                distance = (positions[i] - positions[j]).norm()
                if distance < neighbor_radius:
                    neighbors += 1
                    cohesion += positions[j]
                    alignment += speeds[j]
                    if distance < separation_radius:
                        separation += (positions[i] - positions[j]) / distance
        if neighbors > 0:
            # compute forces
            alignment = alignment.normalized() * max_speed - speeds[i]
            cohesion = (cohesion / neighbors -
                        positions[i]).normalized() * max_speed - speeds[i]
            separation = separation.normalized() * max_speed - speeds[i]
            speeds[i] += (cohesion * cohesion_weight +
                          alignment * alignment_weight +
                          separation * separation_weight) * dt

        positions[i] += speeds[i] * dt
    # wrap around
    # wrap()
    # bounce off
    bounceoff()


init()

video_manager = ti.tools.VideoManager(output_dir="./output",
                                      framerate=60,
                                      automatic_build=False)
for i in range(1000):
    update()
    render()
    img = screen.to_numpy()
    video_manager.write_frame(img)

video_manager.make_video(gif=True, mp4=True)

# gui = ti.GUI("Boids", (width, height))

# while True:
#     for e in gui.get_events(ti.GUI.PRESS):
#         if e.key == ti.GUI.ESCAPE:
#             exit()
#     update()
#     render()
#     gui.set_image(screen)
#     gui.show()
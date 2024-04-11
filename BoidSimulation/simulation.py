import taichi as ti
from .config import boids_num, width, height, boids_size, max_speed, min_speed, neighbor_radius, separation_radius, alignment_weight, cohesion_weight, separation_weight, dt, obstacle_num, obstacle_size
from .models import speeds, positions, screen, obstacles,energy,energy_consumption_rate,initial_energy


@ti.func
def random_range(min, max):
    return ti.random() * (max - min) + min


@ti.kernel
def init():
    center_point = ti.Vector([width / 2, height / 2])
    init_radius = min(width, height) / 4

    for i in range(boids_num):
        direction = ti.Vector([ti.random() - 0.5, ti.random() - 0.5]).normalized()
        magnitude = ti.random() * init_radius
        speeds[i] = ti.Vector([random_range(0, 1) * max_speed, random_range(0, 1) * max_speed])
        positions[i] = center_point + direction * magnitude
        initial_energy[i] = 10000.0  # Set the initial energy for each boid
        energy[i] = initial_energy[i]  # Initialize the current energy

    # Initialize obstacles
    for i in range(obstacle_num):
        obstacles[i] = ti.Vector([ti.random() * width, ti.random() * height])

    # Initialize the energy consumption rate
    # Adjust this value to change the energy consumption rate
    energy_consumption_rate[None] = 0.0025


@ti.kernel
def render():
    # clear screen
    for i, j in screen:
        screen[i, j] = [0.0, 0.0, 0.0]
    # draw boids
    for i in positions:
        s = speeds[i].norm()
        color = ti.Vector([0.0, 0.0, 0.0])
        if s == 0:
            color = ti.Vector([1.0, 0.0, 0.0])
        else:
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

    # Draw obstacles as circles
    for i in range(obstacle_num):
        obstacle_center = obstacles[i]
        obstacle_radius = obstacle_size / 2
        obstacle_color = [1.0, 1.0, 1.0]  # You can customize the color of obstacles

        for x in range(ti.cast(obstacle_center[0] - obstacle_radius, ti.i32),
                        ti.cast(obstacle_center[0] + obstacle_radius, ti.i32) + 1):
            for y in range(ti.cast(obstacle_center[1] - obstacle_radius, ti.i32),
                            ti.cast(obstacle_center[1] + obstacle_radius, ti.i32) + 1):
                if 0 <= x < width and 0 <= y < height:
                    if (x - obstacle_center[0]) ** 2 + (y - obstacle_center[1]) ** 2 <= obstacle_radius ** 2:
                        screen[x, y] = obstacle_color




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
@ti.func
def closest_point_on_obstacle(boid_pos, obstacle_center, obstacle_half_size):
    closest_x = max(obstacle_center.x - obstacle_half_size, min(boid_pos.x, obstacle_center.x + obstacle_half_size))
    closest_y = max(obstacle_center.y - obstacle_half_size, min(boid_pos.y, obstacle_center.y + obstacle_half_size))
    return ti.Vector([closest_x, closest_y])


@ti.func
def obstacles_force(i: int) -> ti.Vector:
    force = ti.Vector([0.0, 0.0])
    for j in range(obstacle_num):
        obstacle_center = obstacles[j]
        closest_point = closest_point_on_obstacle(positions[i], obstacle_center, obstacle_size / 2)

        dir_to_obstacle = positions[i] - closest_point
        distance = dir_to_obstacle.norm()

        # Immediate reaction when too close to an obstacle
        if distance < 80:  # Immediate avoidance distance
            repulsion_force = dir_to_obstacle.normalized() * (1 / max(distance, 1)) * max_speed
            force += repulsion_force
        # Proactive avoidance based on distance to the closest point on the obstacle
        elif distance < separation_radius:
            repulsion_force = dir_to_obstacle.normalized() * (separation_radius - distance) / separation_radius * max_speed
            force += repulsion_force / 1.0

    return force


@ti.func
def cohesion(i: int) -> ti.Vector:
    perceived_center = ti.Vector([0.0, 0.0])
    count = 0
    for j in range(boids_num):
        if i != j and (positions[i] - positions[j]).norm() < neighbor_radius:
            perceived_center += positions[j]
            count += 1
    cohesion_force = ti.Vector([0.0, 0.0])
    # Move the conditional logic outside the loop and ensure a single return path
    if count > 0:
        perceived_center /= count
        cohesion_force = (perceived_center - positions[i]) / cohesion_weight  # Adjust the divisor for strength of force
    else:
        cohesion_force = ti.Vector([0.0, 0.0])
    return cohesion_force



@ti.func
def separation(i: int) -> ti.Vector:
    move = ti.Vector([0.0, 0.0])
    for j in range(boids_num):
        if i != j:
            distance = (positions[i] - positions[j]).norm()
            if distance < separation_radius:
                move += (positions[i] - positions[j]) / distance  # Normalized direction
    return move


@ti.func
def alignment(i: int) -> ti.Vector:
    average_velocity = ti.Vector([0.0, 0.0])
    count = 0
    for j in range(boids_num):
        if i != j and (positions[i] - positions[j]).norm() < neighbor_radius:
            average_velocity += speeds[j]
            count += 1
    alignment_force = ti.Vector([0.0, 0.0])
    if count > 0:
        average_velocity /= count
        alignment_force = (average_velocity - speeds[i]) / alignment_weight  # Adjust the divisor for the strength of force
    else:
        alignment_force = ti.Vector([0.0, 0.0])
    return alignment_force




@ti.kernel
def update():
    for i in range(boids_num):
        # Compute forces from behaviors
        cohesion_force = cohesion(i)
        separation_force = separation(i)
        alignment_force = alignment(i)
        obstacle_force = obstacles_force(i)



        # Sum forces to determine acceleration
        acceleration = cohesion_force + separation_force + alignment_force + obstacle_force

        # Update velocity and position
        speeds[i] += acceleration
        # Apply velocity limits (if necessary)
        if speeds[i].norm() > max_speed:
            speeds[i] = speeds[i].normalized() * max_speed
        if speeds[i].norm() < min_speed:
            speeds[i] = speeds[i].normalized() * min_speed

        # Update energy level
        # Energy consumption proportional to velocity squared
        energy[i] -= energy_consumption_rate[None] * speeds[i].norm() ** 2
        if energy[i] <= 0:
            # Turn off all forces when the energy is depleted
            speeds[i] = ti.Vector([0.0, 0.0])

        positions[i] += speeds[i] * dt  # Assuming `dt` is your timestep variable


    # wrap around
    wrap()
    # bounce off
    # bounceoff()

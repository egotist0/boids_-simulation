import taichi as ti
import BoidSimulation.config as config

# Initialize Taichi
ti.init(arch=ti.gpu)

# Parameters
speeds = ti.Vector.field(2, dtype=ti.f32, shape=config.boids_num)
positions = ti.Vector.field(2, dtype=ti.f32, shape=config.boids_num)
screen = ti.Vector.field(3, dtype=ti.f32, shape=(config.width, config.height))
obstacles = ti.Vector.field(2, dtype=ti.f32, shape=config.obstacle_num)
initial_energy = ti.field(dtype=ti.f32, shape=config.boids_num)
energy = ti.field(dtype=ti.f32, shape=config.boids_num)
energy_consumption_rate = ti.field(dtype=ti.f32, shape=())

predators_pos = ti.Vector.field(2, dtype=ti.f32, shape=config.predator_num)
predators_spd = ti.Vector.field(2, dtype=ti.f32, shape=config.predator_num)

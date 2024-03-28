import taichi as ti
import BoidSimulation.config as config

# Initialize Taichi
ti.init(arch=ti.gpu)

# Parameters
speeds = ti.Vector.field(2, dtype=ti.f32, shape=config.boids_num)
positions = ti.Vector.field(2, dtype=ti.f32, shape=config.boids_num)
screen = ti.Vector.field(3, dtype=ti.f32, shape=(config.width, config.height))
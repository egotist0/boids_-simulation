# Boids Flocking Simulation

> Authors: Authors: Ge Jiang [(email)](mailto:gejiang@@gatech.edu), Zhining Zhang [(email)](mailto:zzhang3180@gatech.edu), Xing Tong [(email)](mailto:txing31@gatech.edu), Yizhe Hong [(email)](mailto:yhong312@gatech.edu)


### Abstract

In this project, we pursued an unconventional path in enhancing the traditional Boid Flocking simulation. Two novel features were introduced to delve into the nuanced aspects of collective behavior. Firstly, the incorporation of an energy model imposes a constraint on each boid. Secondly, the introduction of predators adds a compelling dimension, compelling the flock to engage their survival instincts more frequently. These modifications are aimed at scrutinizing and dissecting their impact on group dynamics and stability, all while evading predation. Through these endeavors, our objective is to gain deeper insights into the dynamics of animal life and interactions within natural systems.
Presentation slides can be found [here](https://docs.google.com/presentation/d/1i1aomyqqpqrqwGwjjzXCHQ3CZLED7QYFCX82MFbC5U4/edit#slide=id.g2c9f19130db_0_136)


## System Description

Our system consisted of three distinct models:

1. The traditional boid model was constructed based on classic alignment, cohesion, and separation rules.

2. The energy model takes into account the limitations of the boid's body energy. Birds may need to rest during extended periods of flight.

3. The predator model simulates the scenario of a flock of boids evading capture by predators.

By integrating all three models, our system can be utilized to simulate, observe, and analyze flocks of boids navigating situations involving predators.



## Model

### Theoretical Behavior Model

#### Recognizing the problem

We want to determine the velocities of boids, which are represented in a fixed Cartesian coordinate system with coordinates $(x, y, \theta)$. The velocities in different directions can be described by a time-dependent equation system:
$$
\begin{cases}
\dot{x} = v · {\cos(\theta)}, \\
\dot{y} = v · {\sin(\theta)}, \\
\dot{\theta} = \omega
\end{cases}
$$
In this context, $v$ represents the magnitude of translational velocity, and $\omega$ represents angular velocity. Since a point does not inherently possess direction, $\theta$ cannot be determined based on the information presented above. However, when using the unicycle model, it becomes possible to establish $\theta$ by selecting an arbitrary reference point and determining orientation with respect to that point.



#### Saturation function

As we are dealing with velocity limits, we need a method to restrict them. The saturation function for the translational velocity is defined as follows:
$$
s(v)= \begin{cases}
v_{\text{max}} & \text{if } v > v_{\text{max}}, \\
v & \text{if } 0 \leq v \leq v_{\text{max}}, \\
0 & \text{if } v < 0
\end{cases}
$$
where $v_{\text{max}}$ denotes the maximum magnitude of angular velocity.

Similarly, the saturation function for angular velocity can be expressed as:
$$
s(\omega)= \begin{cases}
\omega_{\text{max}} & \text{if } \omega > \omega_{\text{max}}, \\
\omega & \text{if } -\omega_{\text{max}} \leq \omega \leq \omega_{\text{max}}, \\
-\omega_{\text{max}} & \text{if } \omega < -\omega_{\text{max}}
\end{cases}
$$
where $\omega_{\text{max}}$ is the magnitude of the maximum angular velocity.



#### The unicycle model

The unicycle model is a common framework in control theory. It is implemented by establishing a reference point $(x, y)$ and an arbitrary point $(x_{\text{h}}, y_{\text{h}})$ relative to the object to define its orientation using an angle, denoted as $\theta$ in this context. The simplest and most intuitive choice for this reference point is the head of the boids. As a result, the distance between these two points remains constant and can be characterized as the boids' length. The coordinates of the boid's head can be determined using the following system of equations:
$$
\begin{cases}
x_{\text{h}} = x + L \cdot \cos(\theta), \\
y_{\text{h}} = y + L \cdot \sin(\theta),
\end{cases}
$$
where $L$ represents the length of the animal, and $\theta$ indicates the angle of the head concerning the body. With the head's coordinates now defined, it becomes possible to determine its velocities, represented as $v$ and $\omega$.
$$
\begin{cases}
\dot{x}_{\text{h}} = \dot{x} + L \cdot (-\sin(\theta)) \cdot \dot{\theta} = v \cdot \cos(\theta) - \omega \cdot L \cdot \sin(\theta), \\
\dot{y}_{\text{h}} = \dot{y} + L \cdot \cos(\theta) \cdot \dot{\theta} = v \cdot \sin(\theta) + \omega \cdot L \cdot \cos(\theta).
\end{cases}
$$


### Behaviour model

The control function, denoted as $u$, is responsible for managing the velocities and can be represented as a vector:
$$
u = \begin{bmatrix}
\dot{x}_{\text{h}} \\
\dot{y}_{\text{h}}
\end{bmatrix}
$$
In order to calculate the control function $u$, several forces are applied to govern the speed. The function that controls the movement of boid $i$ is expressed as follows:
$$
u = f_{i,g} + f_{i,ca} + f_{i,fl} + f_{i,pa}
$$
where the grouping force is denoted as $f_{i,g}$, the collision avoidance force is labeled as $f_{i,ca}$, $f_{i,fl}$ represents the flocking force, and $f_{i,pa}$ is associated with the predator avoidance force.

The forces described in the upcoming section share a common characteristic: they depend on the position of the boid they are acting upon, denoted as $z_i$. In cases where the force also involves interactions with other boids surrounding boid $i$, these boids are referred to as $z_j$.



#### Grouping Force

The influence of the force is limited to boids within a defined local area, which is determined by a distance denoted as $R_{\text{n}}$. Within this distance, they regard the nearby flock members as their neighbors.
$$
f_{i,g} = \sum_{j: |z_j - z_i| \leq R_{\text{n}} \, j \neq i} c_{g} \cdot (z_j - z_i)
$$
where $c_{g}$ represents a constant that determines the magnitude of the force.

#### Collision avoidance force
In order to model a boid's protection of its personal space, a function that rapidly decreases with distance is needed. Therefore, collision avoidance is a crucial aspect when dealing with a group of agents, as it helps prevent accidents and maintain a harmonious group dynamic. The exponential function was used as shown below:
$$
f_{i,ca} = \sum_{j: |z_j - z_i| \leq R_{\text{n}}} c_{ca} \cdot \frac{1}{1 + \exp(\omega_{ca} (\lvert z_j - z_i \rvert - R_{ca}))} \cdot \frac{(z_j - z_i)}{\lvert z_j - z_i \rvert}
$$
where $c_{ca}$ is a constant that determines the magnitude of the force, while $\omega_{ca}$​ is a constant responsible for controlling the rate of decay.



#### Flocking force

To keep the flock together, a force is required to bring the boids closer. This is achieved by consideri  ng the position of the boids' center of mass, denoted as $z_{\text{mc}}$, and applying an attractive force directed toward it, which promotes flock cohesion.
$$
\begin{cases}
z_{\text{mc}} = \frac{1}{n} \sum_{i=1}^{n} z_i, \\
f_{i,fl} = c_{fl} \cdot (z_{\text{mc}} - z_i)
\end{cases}
$$
The strength of the force is controlled by the constant $c_{fl}$​, which governs its overall magnitude.





==The above is the basic algorithm (constructed based on classic alignment, cohesion, and separation rules.)==

Further **Energy Constraint** and **Predator Behaviors** will be added later.





## Platforms of development

+ Python
+ [Taichi Lang](https://www.taichi-lang.org/)



## Current implementation

### Generates visualization

The following part generates a visualization of the Julia Set using the Taichi library. The Julia Set is a complex fractal form commonly used for artistic and mathematical visualization. 

1. Import necessary libraries: `taichi` is a programming language for high-performance computing, and `taichi.math` provides additional functions and data structures for mathematical computations.

```python
import taichi as ti
import taichi.math as tm
```

2. Initialize the Taichi runtime environment, specifying GPU for computation.

```python
ti.init(arch=ti.gpu)
```

3. Define variables and data structures needed.

```python
n = 320
pixels = ti.field(dtype=float, shape=(n * 2, n))
```

4. Define the complex square function `complex_sqr`, used for calculating the square of a complex number. Here, the vector data structure provided by Taichi, `tm.vec2`, is utilized, where `z[0]` represents the real part, and `z[1]` represents the imaginary part.

```python
@ti.func
def complex_sqr(z):
    return tm.vec2(z[0] * z[0] - z[1] * z[1], 2 * z[0] * z[1])
```

5. Define the painting function `paint`, marked as a Taichi kernel function using the `@ti.kernel` decorator. This function calculates the value of each pixel based on the generation rules of the Julia Set.

```python
@ti.kernel
def paint(t: float):
    for i, j in pixels:
        c = tm.vec2(-0.8, tm.cos(t) * 0.2)
        z = tm.vec2(i / n - 1, j / n - 0.5) * 2
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_sqr(z) + c
            iterations += 1
        pixels[i, j] = 1 - iterations * 0.02
```

6. Create a GUI window for displaying the Julia Set image.

```python
gui = ti.GUI("Julia Set", res=(n * 2, n))
```

7. Continuously update the Julia Set image in a loop and display it in the GUI window.

```python
i = 0
while gui.running:
    paint(i * 0.03)
    gui.set_image(pixels)
    gui.show()
    i += 1
```

In each iteration of the loop, the `paint` function is updated, and the generated image of the Julia Set is displayed in the GUI window, while `i` is incremented to change the shape of the Julia Set.



### Bodis implementation

The implementation can be found on: https://github.com/egotist0/boids_simulation/blob/master/boids.py

1. **Initialization**: It initializes the parameters such as the number of boids, screen size, boid size, maximum speed, etc., and initializes the positions and speeds of boids randomly.
2. **Update Loop**: It runs a loop to update the positions and speeds of the boids based on the Boids algorithm. This loop consists of the following steps:
   - **Compute Neighbors**: For each boid, it calculates its neighbors based on a certain radius.
   - **Compute Forces**: It calculates cohesion, alignment, and separation forces for each boid based on its neighbors.
   - **Update Positions and Speeds**: It updates the positions and speeds of the boids based on the computed forces and time step (dt).
3. **Render**: It renders the current state of the simulation by drawing the boids on a screen. It assigns colors to the boids based on their speed vectors and draws them as pixels on the screen.
4. **Wrap and Bounce Off Functions**: These functions are optional and can be used to handle boundary conditions. They are currently commented out in the code.
5. **Video Output**: It records the simulation as a video (both GIF and MP4 formats) using `ti.tools.VideoManager`.





## Literature review

**1. Existing models, simulators, or simulation techniques for boids simulation**

In 1986, Craig Reynolds [1] developed a computer model called Boids simulation, which mimics the behavior of flocks of birds or other swarming organisms like fish or insects. It has made a substantial contribution to the field of artificial life and is used in many different contexts. Basic flocking models include three basic steering behaviors that describe how an individual boid maneuvers based on the positions and velocities its nearby flockmates, which are:

- **Separation**: steer to avoid crowding local flockmates
- **Alignment**: steer towards the average heading of local flockmates
- **Cohesion**: steer to move toward the average position of local flockmates

Delgado-Mata et al [2] extended the basic model to include the influence of fear. Since animals communicate emotions through smell, they used particles in a freely expanding gas to simulate pheromones. Hartman et al [3] introduced a complementary force to this alliance, called leadership alternation. This force determines the probability of a bird becoming a leader or attempting to escape the group. This model has also been applied to other areas. Min et al [4] proposed a distributed algorithm to perform Group Escape Behavior without inter-robot communication by mimicking behaviors of boids. Saska et al [5] extended the idea of the simple BOID model, with three simple rules: Separation, Alignment and Cohesion for swarms of quadrotors. 

Here is a summary of a few noteworthy developments and accomplishments in the simulation of boids:

- **Emergent Behavior**: The capacity of the boids simulation to illustrate emergent behavior is one of its major accomplishments. The individual boids (simulated agents) collectively display intricate flocking patterns that mimic the behavior of actual flocks or swarms by adhering to basic criteria like separation, alignment, and cohesiveness.
- **Animation and Computer Graphics**: The simulation of boids has been widely used in computer animation and visual effects. Two notable instances are the bat swarms in the motion picture "Batman Begins" and the flocks of birds in the animated feature "Finding Nemo."
- **Traffic Simulation**: Modeling and simulating traffic flow, pedestrian movement, and crowd dynamics, Boids simulation techniques have been modified. Transportation systems and crowd management techniques can be studied and optimized by researchers by considering vehicles or people as distinct agents with particular rules.
- **Optimization Algorithms**: The creation of optimization algorithms, including particle swarm optimization (PSO), which are used to solve complicated optimization problems in a variety of domains, including engineering, machine learning, and finance, was influenced by the concepts of boids simulation.

**2. What will us do that will be different from what we’ve found**

We will use Taichi (https://docs.taichi-lang.org/) to implement our simulation. Taichi is an open source high-performance programming language and computational framework focused on high-performance numerical computation and physics simulation. It combines advanced techniques such as compile-time automatic parallelization, on-the-fly compilation, and automatic differentiation to simplify complex parallel computation tasks. Taichi uses a simple syntax similar to Python, but is designed to focus more on GPU acceleration and parallel computation.

If we try to utilize Taichi for simulation of Boids or even introduction of predator scenarios, Taichi can provide the following benefits.

- **Physical Simulation**: Taichi provides a powerful physical simulation of bird flight, pursuit and predation behaviors, as well as the evasion and defense strategies of the prey.Taichi clearly helps us to implement Boids simulation and to set up specific behavioral strategies. Moreover, Taichi is also capable of visualization, which will make our simulation more intuitive.
- **Modeling capabilities**: Taichi uses a simple Python-like syntax and provides extensive documentation and examples. Since Taichi enables custom modeling and simulation, we can flexibly adjust the model parameters and environmental conditions to our specific needs in subsequent projects. This enables us to explore different assumptions and scenarios, thus helping us to better simulate the Boids model.

**References**

[1] Reynolds, Craig W. "Flocks, herds and schools: A distributed behavioral model." Proceedings of the 14th annual conference on Computer graphics and interactive techniques. 1987.

[2] Delgado-Mata, Carlos, et al. "On the use of virtual animals with artificial fear in virtual environments." New Generation Computing 25 (2007): 145-169.

[3] Hartman, Christopher, and Bedrich Benes. "Autonomous boids." Computer Animation and Virtual Worlds 17.3‐4 (2006): 199-206.

[4] Min, Hongkyu, and Zhidong Wang. "Design and analysis of group escape behavior for distributed autonomous mobile robots." 2011 IEEE international conference on robotics and automation. IEEE, 2011.

[5] Saska, Martin, Jan Vakula, and Libor Přeućil. "Swarms of micro aerial vehicles stabilized under a visual relative localization." 2014 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2014.

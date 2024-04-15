# Boids Flocking Simulation

> Authors: Authors: Ge Jiang [(email)](mailto:gejiang@@gatech.edu), Zhining Zhang [(email)](mailto:zzhang3180@gatech.edu), Xing Tong [(email)](mailto:txing31@gatech.edu), Yizhe Hong [(email)](mailto:yhong312@gatech.edu)

### Setup and Run
pip install - r requirement.txt \
python main.py



### Abstract

In this project, we pursued an unconventional path in enhancing the traditional Boid Flocking simulation. Two novel features were introduced to delve into the nuanced aspects of collective behavior. Firstly, the incorporation of an energy model imposes a constraint on each boid. Secondly, the introduction of predators adds a compelling dimension, compelling the flock to engage their survival instincts more frequently. These modifications are aimed at scrutinizing and dissecting their impact on group dynamics and stability, all while evading predation. Through these endeavors, our objective is to gain deeper insights into the dynamics of animal life and interactions within natural systems.
Presentation slides can be found [here](https://docs.google.com/presentation/d/1i1aomyqqpqrqwGwjjzXCHQ3CZLED7QYFCX82MFbC5U4/edit#slide=id.g2c9f19130db_0_136)


## System Description

Our system consisted of three distinct models:

1. The traditional boid model was constructed based on classic alignment, cohesion, and separation rules.

2. The energy model takes into account the limitations of the boid's body energy. Birds may need to rest during extended periods of flight.

3. The predator model simulates the scenario of a flock of boids evading capture by predators.

By integrating all three models, our system can be utilized to simulate, observe, and analyze flocks of boids navigating situations involving predators.



## Usage

First install the dependence

```bash
pip install -r requirement
```

Then run the main.py

```bash
python run main.py
```

Then you can see the result video in your dir

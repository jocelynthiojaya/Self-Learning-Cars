# Self Learning Cars

#### Help visualize neural networks and evolutionary algorithms in interactive forms!

In this simulation, cars with their neural network starts out very stupid, they run everywhere and hit every walls and cars even though they are equipped with sensors to detect them. Even though that's the case, Some of them will be able to traverse *slightly farther* without hitting the walls. From then, new cars are made with neural network based on the genetics of the previous best car plus some mutations and then simulated again. Then, the cycle repeats with the hopes of finding better and better cars each time that can traverse the obstacle nicely. This is possible with the means of AI and genetic algorithms!

This project is developed in Python using the Arcade framework.

```
Group effort by
* Christy Natalia
* Jason Christian
* Jocelyn Thiojaya
```


## Instructions

1.  Clone project and change directory
```bash
git clone https://github.com/jocelynthiojaya/Self-Learning-Cars.git
cd Self-Learning-Cars
```
2.  Create a virtual environment for Python 3 (Google if don't know :<zero-width space>( )
```bash
python -m venv venv
```

3. Activate the virtual environment, and install libraries for this project.
```bash
venv/Scripts/activate
pip install -r requirements.txt
```

4. Run the simulation!
```bash
python main.py
```

If a conf.json file is not available, the program will try to make a filled conf.json in the same directory as the main file.
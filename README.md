# Stochastic Service Composition

Implementation of Industrial APIs Composition in Smart Manufacturing via Markov Decision Processes.

The following sections are:
- Preliminaries
- Structure of the code
- Instructions on how to run the code


## Preliminaries

We assume the review uses a UNIX-like machine and that has Python 3.8 installed.

- Set up the virtual environment. 
First, install [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/).
Then:
```
pipenv install --dev
```
                    
- this command is to start a shell within the Python virtual environment (to be done whenever a new terminal is opened):
```
pipenv shell
```

- Install the Python package in development mode:
```
pip install -e .
# alternatively:
# python setup.py develop 
```

- To use rendering functionalities, you will also need to install Graphviz. 
  At [this page](https://www.graphviz.org/download/) you will
  find the releases for all the supported platform.

## Structure of the code 
`stochastic_service_composition`: the library; reusable software components of the code.

`docs/notebooks/chip_production_supply_chain.ipynb`: link to the notebook showing the Chip Production case study based on stochastic policy described in the paper.

`docs/notebooks/chip_production_LTLf_goals.ipynb`: link to the notebook showing the Chip Production case study based on stochastic constraint-based policy described in the paper.

## Instruction on how to run the code

Each of the following commands must be run on a terminal with the virtual environment activated.
- Go to the notebook's folder:
```
cd docs/notebook
```
- Then, launch jupyter notebook:
```
jupyter-notebook
 ```  

## Discussion of the output:
We base the manufacturing process of chip in the USA.
The Chip Production case study is formed by two phases:
- raw materials and design assortment phase consists of the
collection of the chip design and the essential raw materials. 
In this phase we have that materials and design can be picked from different states.
Every service has its cost to perform the action. Basically the services located in the USA have a unitary cost 
(1.0), while the other costs are computed by measuring the distance between the US and the
identified states. The planner will choose always the convenient service (service located in the USA), 
otherwise will choose the service that has a shorter distance from the USA. In the following
we show the optimal policy that the planner computes:
```
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's0', 'pick_buy_design')
Chosen service:  0 {'ready': {'pick_buy_design': ({'ready': 1.0}, -2.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's1', 'pick_silicon')
Chosen service:  7 {'ready': {'pick_silicon': ({'ready': 1.0}, -2.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's2', 'pick_wafer')
Chosen service:  11 {'ready': {'pick_wafer': ({'ready': 1.0}, -10.1)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's3', 'pick_boron')
Chosen service:  14 {'ready': {'pick_boron': ({'ready': 1.0}, -2.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's4', 'pick_phosphor')
Chosen service:  23 {'ready': {'pick_phosphor': ({'ready': 1.0}, -2.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's5', 'pick_aluminum')
Chosen service:  24 {'ready': {'pick_aluminum': ({'ready': 1.0}, -6.7)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's6', 'pick_resist')
Chosen service:  31 {'ready': {'pick_resist': ({'ready': 1.0}, -1.8)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's7', 'pick_plastic')
Chosen service:  34 {'ready': {'pick_plastic': ({'ready': 1.0}, -11.7)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's8', 'pick_chemicals')
Chosen service:  36 {'ready': {'pick_chemicals': ({'ready': 1.0}, -1.8)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's9', 'pick_copper_frame')
Chosen service:  37 {'ready': {'pick_copper_frame': ({'ready': 1.0}, -2.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's0', 'pick_buy_design')
Chosen service:  0 {'ready': {'pick_buy_design': ({'ready': 1.0}, -2.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's1', 'pick_silicon')
Chosen service:  7 {'ready': {'pick_silicon': ({'ready': 1.0}, -2.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's2', 'pick_wafer')
Chosen service:  11 {'ready': {'pick_wafer': ({'ready': 1.0}, -10.1)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's3', 'pick_boron')
Chosen service:  14 {'ready': {'pick_boron': ({'ready': 1.0}, -2.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's4', 'pick_phosphor')
Chosen service:  23 {'ready': {'pick_phosphor': ({'ready': 1.0}, -2.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's5', 'pick_aluminum')
Chosen service:  24 {'ready': {'pick_aluminum': ({'ready': 1.0}, -6.7)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's6', 'pick_resist')
Chosen service:  31 {'ready': {'pick_resist': ({'ready': 1.0}, -1.8)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's7', 'pick_plastic')
Chosen service:  34 {'ready': {'pick_plastic': ({'ready': 1.0}, -11.7)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's8', 'pick_chemicals')
Chosen service:  36 {'ready': {'pick_chemicals': ({'ready': 1.0}, -1.8)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's9', 'pick_copper_frame')
Chosen service:  37 {'ready': {'pick_copper_frame': ({'ready': 1.0}, -2.0)}}
```










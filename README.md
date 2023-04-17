# Stochastic Service Composition - Chip Chain Case Study

Implementation of Industrial APIs Composition in Smart Manufacturing via Markov Decision Processes.

The following sections are:
- Preliminaries
- Structure of the code
- Instructions on how to run the code
- Discussion of the output

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

`docs/notebooks/chip_production_supply_chain.ipynb`: link to the notebook showing the Chip Chain case study based on stochastic policy described in the paper.

`docs/notebooks/chip_production_LTLf_goals.ipynb`: link to the notebook showing the Chip Chain case study based on stochastic constraint-based policy described in the paper.

## Instructions on how to run the code

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
The Chip Chain case study is formed by two phases:
- raw materials and design assortment phase that consists of the
collection of the chip design and the essential raw materials.
- manufacturing processes phase that  represents the effective operations for the manufacturing of chips
  (cleaning, film deposition, resist coating, exposure, development, etching, impurities implantation, activation, resist stripping, assembly, testing, packaging)

In the first phase we have that materials and design can be picked from different states.
Every service has its cost to perform the action. Basically, the services located in the USA have a unitary cost 
(1.0), while the other costs are computed by measuring the distance between the USA and the
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
Chosen service:  28 {'ready': {'pick_resist': ({'ready': 1.0}, -1.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's7', 'pick_plastic')
Chosen service:  34 {'ready': {'pick_plastic': ({'ready': 1.0}, -11.7)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's8', 'pick_chemicals')
Chosen service:  35 {'ready': {'pick_chemicals': ({'ready': 1.0}, -1.0)}}
**************************************************
Current state:  (('ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready', 'ready'), 's9', 'pick_copper_frame')
Chosen service:  37 {'ready': {'pick_copper_frame': ({'ready': 1.0}, -1.0)}}
```
From this output we observe that:
- the planner preferred using service `service_design_usa` (service `0`) because it was more convenient choose the service located in the USA than the services of other costly countries;
- the planner preferred using service `service_silicon_usa` (service `7`) because it was more convenient pick the silicon from the warehouse located in the USA instead of picking it from other costly countries;
- the planner preferred using service `service_wafer_japan` (service `11`) because it was more convenient pick the wafer from the Japan instead of picking it from South Korea;
- the planner preferred using service `service_boron_usa` (service `14`) because it was more convenient pick the boron from the warehouse located in the USA instead of picking it from other costly countries;
- the planner preferred using service `service_phosphor_usa` (service `23`) because it was more convenient pick the phosphor from the warehouse located in the USA instead of picking it from other costly countries;
- the planner preferred using service `service_aluminum_brazil` (service `24`) because it was more convenient pick the aluminum from the warehouse located in Brazil instead of picking it from other costly countries;
- the planner preferred using service `service_resist_usa` (service `28`) because it was more convenient pick the resist from the warehouse located in the USA instead of picking it from other costly countries;
- the planner preferred using service `service_plastic_china` (service `34`) because it was more convenient pick the plastic from the warehouse located in China instead of picking it from India;
- the planner preferred using service `service_chemicals_usa` (service `35`) because it was more convenient pick the chemicals from the warehouse located in the USA instead of picking it from Canada;
- the planner preferred using service `service_copper_frame_usa` (service `37`) because it was more convenient pick the copper frame from the warehouse located in the USA instead of picking it from other costly countries.

In the second phase the manufacturing services are located in a unique factory in the USA and
generally the cost of the operations is set to 1. However, we have multiple copies of the same service
performing the same operation but more costly and wear out. The planner will choose the best service 
i.e., with a low probability to break and a low cost. In the following we show the optimal policy that the planner computes:

```
**************************************************
Current state:  ['ready', 'ready', 'ready', 'ready', 'ready', 'available']
Chosen service:  0 Chosen action:  cleaning {'ready': {'cleaning': ({'ready': 1.0}, -1.0)}}
**************************************************
Current state:  ['ready', 'ready', 'ready', 'ready', 'ready', 'available']
Chosen service:  1 Chosen action:  config_film_deposition {'ready': {'config_film_deposition': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_film_deposition': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'film_deposition': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_film_deposition': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_film_deposition': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['ready', 'configured', 'ready', 'ready', 'ready', 'available']
Chosen service:  2 Chosen action:  config_film_deposition {'ready': {'config_film_deposition': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_film_deposition': ({'executing': 0.5, 'broken': 0.5}, 0.0)}, 'executing': {'film_deposition': ({'ready': 0.95, 'broken': 0.05}, -5.0)}, 'broken': {'restore_film_deposition': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_film_deposition': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['ready', 'configured', 'configured', 'ready', 'ready', 'available']
Chosen service:  1 Chosen action:  checked_film_deposition {'ready': {'config_film_deposition': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_film_deposition': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'film_deposition': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_film_deposition': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_film_deposition': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['ready', 'executing', 'configured', 'ready', 'ready', 'available']
Chosen service:  2 Chosen action:  checked_film_deposition {'ready': {'config_film_deposition': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_film_deposition': ({'executing': 0.5, 'broken': 0.5}, 0.0)}, 'executing': {'film_deposition': ({'ready': 0.95, 'broken': 0.05}, -5.0)}, 'broken': {'restore_film_deposition': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_film_deposition': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['ready', 'executing', 'executing', 'ready', 'ready', 'available']
Chosen service:  1 Chosen action:  film_deposition {'ready': {'config_film_deposition': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_film_deposition': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'film_deposition': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_film_deposition': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_film_deposition': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['ready', 'ready', 'executing', 'ready', 'ready', 'available']
Chosen service:  3 Chosen action:  config_resist_coating {'ready': {'config_resist_coating': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_resist_coating': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'resist_coating': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_resist_coating': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_resist_coating': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['ready', 'ready', 'executing', 'configured', 'ready', 'available']
Chosen service:  3 Chosen action:  checked_resist_coating {'ready': {'config_resist_coating': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_resist_coating': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'resist_coating': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_resist_coating': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_resist_coating': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['ready', 'ready', 'executing', 'executing', 'ready', 'available']
Chosen service:  4 Chosen action:  config_resist_coating {'ready': {'config_resist_coating': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_resist_coating': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'resist_coating': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_resist_coating': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_resist_coating': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['ready', 'ready', 'executing', 'executing', 'configured', 'available']
Chosen service:  4 Chosen action:  checked_resist_coating {'ready': {'config_resist_coating': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_resist_coating': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'resist_coating': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_resist_coating': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_resist_coating': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['ready', 'ready', 'executing', 'executing', 'executing', 'available']
Chosen service:  3 Chosen action:  resist_coating {'ready': {'config_resist_coating': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_resist_coating': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'resist_coating': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_resist_coating': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_resist_coating': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['ready', 'ready', 'executing', 'ready', 'executing', 'available']
Chosen service:  5 Chosen action:  exposure {'available': {'exposure': ({'done': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'check_exposure': ({'available': 1.0}, -10.0)}, 'done': {'check_exposure': ({'available': 1.0}, 0.0)}}
**************************************************
Current state:  ['done', 'available', 'ready', 'ready', 'available', 'available']
Chosen service:  7 Chosen action:  config_development {'ready': {'config_development': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_development': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'development': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_development': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_development': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['done', 'available', 'configured', 'ready', 'available', 'available']
Chosen service:  7 Chosen action:  checked_development {'ready': {'config_development': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_development': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'development': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_development': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_development': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['done', 'available', 'executing', 'ready', 'available', 'available']
Chosen service:  8 Chosen action:  config_development {'ready': {'config_development': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_development': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'development': ({'ready': 0.95, 'broken': 0.05}, -5.0)}, 'broken': {'restore_development': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_development': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['done', 'available', 'executing', 'configured', 'available', 'available']
Chosen service:  8 Chosen action:  checked_development {'ready': {'config_development': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_development': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'development': ({'ready': 0.95, 'broken': 0.05}, -5.0)}, 'broken': {'restore_development': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_development': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['done', 'available', 'executing', 'executing', 'available', 'available']
Chosen service:  7 Chosen action:  development {'ready': {'config_development': ({'configured': 1.0}, 0.0)}, 'configured': {'checked_development': ({'executing': 0.95, 'broken': 0.05}, 0.0)}, 'executing': {'development': ({'ready': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'restore_development': ({'repairing': 1.0}, -10.0)}, 'repairing': {'repaired_development': ({'ready': 1.0}, 0.0)}}
**************************************************
Current state:  ['done', 'available', 'ready', 'executing', 'available', 'available']
Chosen service:  9 Chosen action:  etching {'available': {'etching': ({'done': 0.95, 'broken': 0.05}, -1.0)}, 'broken': {'check_etching': ({'available': 1.0}, -10.0)}, 'done': {'check_etching': ({'available': 1.0}, 0.0)}}
**************************************************
```

In fact,  from the calculation of the optimal policy we observe that:
- the planner when performs the action `film_deposition` preferred using service `service_film_deposition1` (service `1`) because this service had a more convenient cost respect to `service_film_deposition2`;
- the planner when performs the action `resist_coating` preferred using service `service_resist_coating1` (service `3`) because this service had a more convenient cost respect to `service_resist_coating2`;
- the planner when performs the action `exposure` preferred using service `service_exposure1` (service `5`) because this service had a more convenient cost and less probability to break respect to `service_exposure2`;
- the planner when performs the action `development` preferred using service `service_development1` (service `7`) because this service had a more convenient cost respect to `service_development2`;
- the planner when performs the action `etching` preferred using service `service_etching1` (service `9`) because this service had a more convenient cost and less probability to break respect to `service_etching2`.









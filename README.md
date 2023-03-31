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












#!/usr/bin/env python
# coding: utf-8
import time, json
from memory_profiler import profile
from stochastic_service_composition.declare_utils import *
from stochastic_service_composition.composition_mdp import composition_mdp
from stochastic_service_composition.composition_mdp import comp_mdp
from mdp_dp_rl.algorithms.dp.dp_analytic import DPAnalytic
from docs.notebooks.setup_v1 import *
import os

# create folder if not exists
if not os.path.exists('experimental_results'):
    os.makedirs('experimental_results')

config_json = json.load(open('config.json', 'r'))
mode = config_json['mode']
phase = config_json['phase']
size = config_json['size']

if phase == 1:
    file_name = f"experimental_results/time_profiler_{mode}_phase{phase}.txt"
    fp_compMDP = f"experimental_results/memory_profiler_composition_{mode}_phase{phase}.log"
    fp_DPAnalytic = f"experimental_results/memory_profiler_policy_{mode}_phase{phase}.log"
else:
    file_name = f"experimental_results/time_profiler_{mode}_phase{phase}_{size}.txt"
    fp_compMDP = f"experimental_results/memory_profiler_composition_{mode}_phase{phase}_{size}.log"
    fp_DPAnalytic = f"experimental_results/memory_profiler_policy_{mode}_phase{phase}_{size}.log"

# AUTOMATA
@profile(stream=open(fp_compMDP, "w+"))
def execute_composition_automata(target, services):
    mdp = composition_mdp(target, *services, gamma=0.9)
    return mdp

# LTLf
@profile(stream=open(fp_compMDP, "w+"))
def execute_composition_ltlf(declare_automaton, services):
    print("Composition MDP computing...")
    mdp = comp_mdp(declare_automaton, services, gamma=0.1)
    return mdp

# POLICY
@profile(stream=open(fp_DPAnalytic, "w+"))
def execute_policy(mdp):
    opn = DPAnalytic(mdp, 1e-4)
    opt_policy = opn.get_optimal_policy_vi()
    return opt_policy
    
def main():
    to_write = f"Mode: {mode}\nPhase: {phase}\n" if phase == 1 else f"Mode: {mode}\nPhase: {phase}\nSize: {size}"
    with open(file_name, "w+") as f:
        f.write(f"{to_write}\n")
    print(to_write)

    
    if phase == 1:
        all_services = all_services_phase1
        target = target_service_phase1_automata() if mode == "automata" else target_service_phase1_ltlf()

    elif phase == 2:
        all_services = services_phase2(size)
        target = target_service_phase2_automata() if mode == "automata" else target_service_phase2_ltlf()

    to_write = f"Tot_services: {len(all_services)}"
    with open(file_name, "a") as f:
        f.write(f"{to_write}\n")
    print(to_write)
    
    print("Services created.\nStarting composition...")

    # AUTOMATA
    if mode == "automata":
        now = time.time_ns()
        mdp = execute_composition_automata(target, all_services)
        elapsed1 = (time.time_ns() - now) / 10 ** 9
        states = len(mdp.all_states)
        with open(file_name, "a") as f:
            to_write = f"MDP states: {states}\nComposition elapsed time: {elapsed1} s\n"
            f.write(to_write)
        print("Number of states: ", states)
        print("Composition MDP computed.\nStarting computing policy...")
        now = time.time_ns()
        execute_policy(mdp)
        elapsed2 = (time.time_ns() - now) / 10 ** 9
        with open(file_name, "a") as f:
            to_write = f"Policy elapsed time: {elapsed2} s\n"
            f.write(to_write)
    # LTLf
    elif mode == "ltlf":
        now = time.time_ns()
        mdp = execute_composition_ltlf(target, all_services)
        elapsed1 = (time.time_ns() - now) / 10 ** 9
        states = len(mdp.all_states)
        with open(file_name, "a") as f:
            to_write = f"MDP states: {states}\nComposition elapsed time: {elapsed1} s\n"
            f.write(to_write)
        print("Number of states: ", states)
        print("Composition MDP computed.\nStarting computing policy...")
        now = time.time_ns()
        execute_policy(mdp)
        elapsed2 = (time.time_ns() - now) / 10 ** 9
        with open(file_name, "a") as f:
            to_write = f"Policy elapsed time: {elapsed2} s\n"
            f.write(to_write)
    
    print("Policy computed.")
    print("Done.")
            
if __name__ == '__main__':
    main()
    '''try:
        main()
    except Exception as e:
        with open(file_name, "w+") as f:
            to_write = f"Execution failed: {e}"
            f.write(to_write)'''

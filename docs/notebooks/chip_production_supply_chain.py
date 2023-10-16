#!/usr/bin/env python
# coding: utf-8
import time, json
from memory_profiler import profile
from stochastic_service_composition.declare_utils import *
from stochastic_service_composition.composition_mdp import composition_mdp
from stochastic_service_composition.composition_mdp import comp_mdp
from mdp_dp_rl.algorithms.dp.dp_analytic import DPAnalytic
from docs.notebooks.setup import *
#from tqdm import tqdm


config_json = json.load(open('config.json', 'r'))
mode = config_json['mode']
phase = config_json['phase']
size = config_json['size']

if phase == 1:
    file_name = f"experimental_results/time_profiler_{mode}_phase{phase}.txt"
    fp_compMDP = open(f"experimental_results/memory_profiler_composition_{mode}_phase{phase}.log","w+")
    fp_DPAnalytic = open(f"experimental_results/memory_profiler_policy_{mode}_phase{phase}.log","w+")
else:
    file_name = f"experimental_results/time_profiler_{mode}_phase{phase}_{size}.txt"
    fp_compMDP = open(f"experimental_results/memory_profiler_composition_{mode}_phase{phase}_{size}.log","w+")
    fp_DPAnalytic = open(f"experimental_results/memory_profiler_policy_{mode}_phase{phase}_{size}.log","w+")

@profile(stream=fp_compMDP)
def execute_composition_automata(target, services):
    mdp = composition_mdp(target, *services, gamma=0.9)
    return mdp

@profile(stream=fp_compMDP)
def execute_composition_ltlf(declare_automaton, services):
    mdp = comp_mdp(declare_automaton, services, gamma=0.9)
    return mdp

@profile(stream=fp_DPAnalytic)
def execute_policy(mdp):
    opn = DPAnalytic(mdp, 1e-4)
    opt_policy = opn.get_optimal_policy_vi()
    return opt_policy
    
def main():
    to_print = f"mode {mode}, phase {phase}" if phase == 1 else f"mode {mode}, phase {phase}, size {size}"
    print(to_print)
    
    if phase == 1:
        all_services = all_services_phase1
        
        if mode == "automata":
            target = target_phase1_automata
        elif mode == "ltlf":
            target = target_phase1_ltlf
    elif phase == 2:
        if size == "small":
            all_services = all_services_phase2_small
        elif size == "manageable1":
            all_services = all_services_phase2_manageable1
        elif size == "manageable2":
            all_services = all_services_phase2_manageable2
        elif size == "complex":
            all_services = all_services_phase2_complex
            
        if mode == "automata":
            target = target_phase2_automata
        elif mode == "ltlf":
            target = target_phase2_ltlf
    
    print("Services created.\nStarting composition...")
    #total_iterations = 1000
    #for i in tqdm(range(total_iterations), desc="Processing", ncols=100):
    
    if mode == "automata":
        now = time.time_ns()
        mdp = execute_composition_automata(target, all_services)
        elapsed1 = time.time_ns() - now
        print("Composition MDP computed.\nStarting computing policy...")
        now = time.time_ns()
        execute_policy(mdp)
        elapsed2 = time.time_ns() - now
    elif mode == "ltlf":
        now = time.time_ns()
        mdp = execute_composition_ltlf(target, all_services)
        elapsed1 = time.time_ns() - now
        print("Composition MDP computed.\nStarting computing policy...")
        now = time.time_ns()
        execute_policy(mdp)
        elapsed2 = time.time_ns() - now
    
    print("Policy computed.")
    
    elapsed1 = elapsed1 / 10 ** 9
    elapsed2 = elapsed2 / 10 ** 9
    with open(file_name, "w+") as f:
        to_write = f"tot_services: {len(all_services)}\ncomposition elapsed time: {elapsed1} s\npolicy elapsed time: {elapsed2} s"
        f.write(to_write)
            
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        with open(file_name, "w+") as f:
            to_write = f"Esecuzione fallita: {e}"
            f.write(to_write)

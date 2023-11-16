#!/usr/bin/env python
# coding: utf-8
import time, json
from memory_profiler import profile
from stochastic_service_composition.declare_utils import *
from stochastic_service_composition.composition_mdp_redis import composition_mdp
from stochastic_service_composition.composition_mdp import comp_mdp
from mdp_dp_rl.algorithms.dp.dp_analytic import DPAnalytic
from docs.notebooks.setup import *
#from tqdm import tqdm


config_json = json.load(open('config.json', 'r'))
mode = config_json['mode']
phase = config_json['phase']
size = config_json['size']
encode = config_json['encode']
binary = config_json['binary']

if phase == 1:
    file_name = f"experimental_results/time_profiler_{mode}_phase{phase}.txt"
    fp_compMDP = open(f"experimental_results/memory_profiler_composition_{mode}_phase{phase}.log","w+")
    fp_DPAnalytic = open(f"experimental_results/memory_profiler_policy_{mode}_phase{phase}.log","w+")
else:
    file_name = f"experimental_results/time_profiler_{mode}_phase{phase}_{size}.txt"
    fp_compMDP = open(f"experimental_results/memory_profiler_composition_{mode}_phase{phase}_{size}.log","w+")
    fp_DPAnalytic = open(f"experimental_results/memory_profiler_policy_{mode}_phase{phase}_{size}.log","w+")

@profile(stream=fp_compMDP)
def execute_composition_automata(target, services, tf, encode):
    mdp = composition_mdp(target, *services, tf=tf, gamma=0.1, encode=encode, binary=binary)
    return mdp

@profile(stream=fp_compMDP)
def execute_composition_ltlf(declare_automaton, services, automaton, encode):
    mdp = comp_mdp(declare_automaton, services, automaton=automaton, gamma=0.9, encode=encode)
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
            target = target_service_phase1_automata()
            tf = transition_function_phase1_automata
        elif mode == "ltlf":
            target, automaton = target_service_phase1_ltlf()
    elif phase == 2:
        assert size in ["small", "manageable1", "manageable2", "complex"]
        all_services = services_phase2(size)
            
        if mode == "automata":
            target = target_service_phase2_automata()
            tf = transition_function_phase2_automata
        elif mode == "ltlf":
            target, automaton = target_service_phase2_ltlf()
            
    print("N_services: ", len(all_services))
    
    print("Services created.\nStarting composition...")
    
    with open(file_name, "w+") as f:
        to_write = f"{mode} mode\n{phase} phase\n{size} size\ntot_services: {len(all_services)}\n"
        f.write(to_write)
    
    if mode == "automata":
        now = time.time_ns()
        mdp = execute_composition_automata(target, all_services, tf, encode)
        elapsed1 = (time.time_ns() - now) / 10 ** 9
        states = len(mdp.all_states)
        with open(file_name, "a") as f:
            to_write = f"total states: {states}\n\n"
            f.write(to_write)
        print("Number of states: ", states)
        with open(file_name, "a") as f:
            to_write = f"composition elapsed time: {elapsed1} s\n"
            f.write(to_write)
        print("Composition MDP computed.\nStarting computing policy...")
        now = time.time_ns()
        execute_policy(mdp)
        elapsed2 = (time.time_ns() - now) / 10 ** 9
        with open(file_name, "a") as f:
            to_write = f"policy elapsed time: {elapsed2} s\n"
            f.write(to_write)
    elif mode == "ltlf":
        now = time.time_ns()
        mdp = execute_composition_ltlf(target, all_services, automaton, encode)
        elapsed1 = (time.time_ns() - now) / 10 ** 9
        states = len(mdp.all_states)
        with open(file_name, "a") as f:
            to_write = f"total states: {states}\n\n"
            f.write(to_write)
        print("Number of states: ", states)
        with open(file_name, "a") as f:
            to_write = f"composition elapsed time: {elapsed1} s\n"
            f.write(to_write)
        print("Composition MDP computed.\nStarting computing policy...")
        now = time.time_ns()
        execute_policy(mdp)
        elapsed2 = (time.time_ns() - now) / 10 ** 9
        with open(file_name, "a") as f:
            to_write = f"policy elapsed time: {elapsed2} s\n"
            f.write(to_write)
    print("Policy computed.")
    
            
if __name__ == '__main__':
    '''try:
        main()
    except Exception as e:
        print(e)
        with open(file_name, "a+") as f:
            to_write = f"Esecuzione fallita: {e}"
            f.write(to_write)'''
    main()

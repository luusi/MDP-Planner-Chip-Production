"""This module implements the algorithm to compute the system-target MDP."""
import time
from collections import deque
from typing import Deque, Dict, List, Set, Tuple

from mdp_dp_rl.processes.mdp import MDP
from pythomata import SimpleDFA
from pythomata.impl.symbolic import SymbolicDFA

from stochastic_service_composition.services import Service, build_system_service, build_service_from_transitions
from stochastic_service_composition.target import Target, build_target_from_transitions
from stochastic_service_composition.types import Action, State, MDPDynamics, TargetDynamics

import redis

r_states = redis.Redis(host='localhost', port=6379, db=1)
r_action = redis.Redis(host='localhost', port=6379, db=2)
r_states_tg = redis.Redis(host='localhost', port=6379, db=3)
r_states_ss = redis.Redis(host='localhost', port=6379, db=4)
r_actions_ss = redis.Redis(host='localhost', port=6379, db=5)

COMPOSITION_MDP_INITIAL_STATE = 0
COMPOSITION_MDP_INITIAL_ACTION = "initial"
COMPOSITION_MDP_UNDEFINED_ACTION = "undefined"
DEFAULT_GAMMA = 0.9

COMPOSITION_MDP_SINK_STATE = -1

def encode_automata_binary(target, *services, tf):
    n_elem = 0
    
    # encode services
    print("\tStarting encoding services...")
    new_services : List[Service] = []    
    
    for service in services:
        states = service.states
        for state in states:
            r_states.set(state, str(n_elem).encode())
            n_elem += 1
    
    for service in services:
        actions = service.actions
        for action in actions:
            r_action.set(action, str(n_elem).encode())
            n_elem += 1
        in_action = str(n_elem).encode()
        n_elem += 1
        in_und_action = str(n_elem).encode()
        n_elem += 1
        
    for service in services:
        final_states = service.final_states
        initial_state = service.initial_state
        transition_function = service.transition_function 
        
        transition_function_ser : MDPDynamics = {}
        final_states_ser : Set[State] = set()
        initial_state_ser : State = None
        
        # encode final states and initial state
        for state in final_states:
            final_states_ser.add(r_states.get(state))
        initial_state_ser = r_states.get(initial_state)
        
        # encode transition function (from the new created states and actions)
        # Dict[State, Dict[Action, Tuple[Dict[State, Prob], Reward]]]
        for state in transition_function:
            actions_state_ser = {}
            for action in transition_function[state]:
                dict_next_state = {}
                next_states = list(transition_function[state][action][0].keys())
                for next_state in next_states:
                    prob = transition_function[state][action][0][next_state]
                    dict_next_state[r_states.get(next_state)] = prob
                rew = transition_function[state][action][1]
                actions_state_ser[r_action.get(action)] = (dict_next_state, rew)
            transition_function_ser[r_states.get(state)] = actions_state_ser
                
        # create an updated service and add it to the list
        new_service : Service = build_service_from_transitions(transition_function_ser, initial_state_ser, final_states_ser)
        new_services.append(new_service)
    print("\tService encoded.")
    
    # encode target
    print("\tStarting encoding target...")
    
    final_states_tar : Set[State] = set()
    initial_state_targ : State = None
    transition_function_targ : TargetDynamics = {}
    
    # original target
    states = target.states
    final_states = target.final_states
    initial_state = target.initial_state
    
    in_state = str(n_elem).encode()
    n_elem += 1
    
    # encode states and actions
    for state in states:
        r_states_tg.set(state, str(n_elem).encode())
        n_elem += 1
    
    # encode final states and initial state
    for state in final_states:
        final_states_tar.add(r_states_tg.get(state))
    initial_state_targ = r_states_tg.get(initial_state)
    
    # encode transition function (from the new created states and actions)
    # Dict[State, Dict[Action, Tuple[State, Prob, Reward]]]
    for state in tf:
        actions_state_targ = {}
        for action in tf[state]:
            value_action = tf[state][action]
            state_other = value_action[0]
            prob = value_action[1]
            rew = value_action[2]
            actions_state_targ[r_action.get(action)] = (r_states_tg.get(state_other), prob, rew)
        transition_function_targ[r_states_tg.get(state)] = actions_state_targ
    
    # create an updated target
    new_target : Target = build_target_from_transitions(transition_function_targ, initial_state_targ, final_states_tar)
    print("\tTarget encoded.")
    
    return new_target, new_services, (in_state, in_action, in_und_action), n_elem


def encode_transition_function(transition_function: MDPDynamics, n_elems):
    #Dict[State, Dict[Action, Tuple[Dict[State, Prob], Reward]]]

    # encode states and actions
    # STATI
    for state in transition_function.keys():
        r_states_ss.set(state, str(n_elems).encode())
        n_elems += 1

    # AZIONI
    for state in transition_function.keys():
        for action in transition_function[state].keys():
            r_actions_ss.set(action, str(n_elems).encode())
            n_elems += 1

    new_transition_function : MDPDynamics = {}
    for state in transition_function:
        dict_actions = {}
        for action in transition_function[state]:
            dict_next_state = {}
            current_next_states = transition_function[state][action][0]
            for next_state in current_next_states:
                prob = transition_function[state][action][0][next_state]
                dict_next_state[r_states_ss.get(next_state)] = prob
            rew = transition_function[state][action][1]
            dict_actions[r_actions_ss.get(action)] = (dict_next_state, rew)
        new_transition_function[r_states_ss.get(state)] = dict_actions

    return new_transition_function


def composition_mdp(
    target: Target, *services: Service, tf: TargetDynamics, gamma: float = DEFAULT_GAMMA, encode: bool = False, binary: bool = False
) -> MDP:
    """
    Compute the composition MDP.

    :param target: the target service.
    :param services: the community of services.
    :param tf: the transition function of the target.
    :param gamma: the discount factor.
    :param encode: if True, encode the services and the target.
    :return: the composition MDP.
    """
    
    if encode and binary:
        print("binary")
        target, services, enc_elems, n_elem = encode_automata_binary(target, *services, tf=tf)
        in_state, in_action, in_und_action = enc_elems

    t_now = time.time_ns()
    system_service = build_system_service(*services)
    t_after = time.time_ns()
    print(f"System service created in {(t_after - t_now) / 10 ** 9} s.")

    # one action per service (1..n) + the initial action (0)
    actions: Set[Action] = set(range(len(services)))
    if encode:
        initial_state = in_state
        initial_action = in_action
        undefined_action = in_und_action
    else:
        initial_state = COMPOSITION_MDP_INITIAL_STATE
        initial_action = COMPOSITION_MDP_INITIAL_ACTION
        undefined_action = COMPOSITION_MDP_UNDEFINED_ACTION
    
    actions.add(initial_action)
    # add an 'undefined' action for sink states
    actions.add(undefined_action)

    # CREATE THE FINAL COMPOSITION MDP FROM THE SYSTEM SERVICE AND THE TARGET
    t_now = time.time_ns()
    transition_function: MDPDynamics = {}

    visited = set()
    to_be_visited = set()
    queue: Deque = deque()

    # add initial transitions
    transition_function[initial_state] = {}
    initial_transition_dist = {}
    symbols_from_initial_state = target.policy[target.initial_state].keys()
    for symbol in symbols_from_initial_state:
        next_state = (system_service.initial_state, target.initial_state, symbol)
        next_prob = target.policy[target.initial_state][symbol]
        initial_transition_dist[next_state] = next_prob
        queue.append(next_state)
        to_be_visited.add(next_state)
    transition_function[initial_state][initial_action] = (initial_transition_dist, 0.0)  # type: ignore

    while len(queue) > 0:
        current_state = queue.popleft()
        to_be_visited.remove(current_state)
        visited.add(current_state)
        current_system_state, current_target_state, current_symbol = current_state

        transition_function[current_state] = {}
        # index system symbols (action, service_id) by symbol
        system_symbols: List[Tuple[Action, int]] = list(
            system_service.transition_function[current_system_state].keys()
        )
        system_symbols_by_symbols: Dict[Action, Set[int]] = {}
        for action, service_id in system_symbols:
            system_symbols_by_symbols.setdefault(action, set()).add(service_id)

        for i in system_symbols_by_symbols.get(current_symbol, set()):
            next_transitions = {}
            # TODO check if it is needed
            if current_symbol not in target.transition_function[current_target_state]:
                continue
            next_reward = (
                target.reward[current_target_state][current_symbol]
                if (current_symbol, i)
                in system_service.transition_function[current_system_state]
                else 0
            )
            next_target_state = target.transition_function[current_target_state][
                current_symbol
            ]
            next_system_states, next_system_reward = system_service.transition_function[
                current_system_state
            ][(current_symbol, i)]
            for next_symbol, next_prob in target.policy.get(next_target_state, {}).items():
                for next_system_state, next_system_prob in next_system_states.items():
                    next_state = (next_system_state, next_target_state, next_symbol)
                    if next_prob * next_system_prob == 0.0:
                        continue
                    next_transitions[next_state] = next_prob * next_system_prob
                    if next_state not in visited and next_state not in to_be_visited:
                        to_be_visited.add(next_state)
                        queue.append(next_state)
            transition_function[current_state][i] = (  # type: ignore
                next_transitions,  # type: ignore
                next_reward + next_system_reward,
            )

        # states without outgoing transitions are sink states.
        # add loop transitions with
        # - 'undefined' action
        # - probability 1
        # - reward 0
        if len(transition_function[current_state]) == 0:
            transition_function.setdefault(current_state, {})
            transition_function[current_state][COMPOSITION_MDP_UNDEFINED_ACTION] = (
                {current_state: 1.0},
                0.0,
            )  # type: ignore
        # TODO check correctness
        # if next state distribution is empty, add loops

    if encode:
        t_now_encoding = time.time_ns()
        transition_function = encode_transition_function(transition_function, n_elem)
        t_after_encoding = time.time_ns()
        print(f"\tEncoding of transition function done in {(t_after_encoding - t_now_encoding) / 10 ** 9} s.")
    
    t_after = time.time_ns()
    print(f"Transition function created in {(t_after - t_now) / 10 ** 9} s.")
    
    return MDP(transition_function, gamma)


def encode_ltlf(*services, automaton: SymbolicDFA):
    n_elem = 0
    
    # encode services
    print("\tStarting encoding services...")
    new_services : List[Service] = []    
    dict_act = {}
    dict_states_ser = {}
    
    for service in services:
        states = service.states
        for state in states:
            if state not in dict_states_ser.keys():
                dict_states_ser[state] = n_elem
                n_elem += 1
    
    for service in services:
        actions = service.actions
        for action in actions:
            if action not in dict_act.keys():
                dict_act[action] = n_elem
                n_elem += 1
        in_action = n_elem
        n_elem += 1
        in_und_action = n_elem
        n_elem += 1
        
    for service in services:
        final_states = service.final_states
        initial_state = service.initial_state
        transition_function = service.transition_function 
        
        transition_function_ser : MDPDynamics = {}
        final_states_ser : Set[State] = set()
        initial_state_ser : State = None        
        
        # encode final states and initial state
        for state in final_states:
            final_states_ser.add(dict_states_ser[state])
        initial_state_ser = dict_states_ser[initial_state]
        
        # encode transition function (from the new created states and actions)
        # Dict[State, Dict[Action, Tuple[Dict[State, Prob], Reward]]]
        for state in transition_function:
            actions_state_ser = {}
            for action in transition_function[state]:
                dict_next_state = {}
                next_states = list(transition_function[state][action][0].keys())
                for next_state in next_states:
                    prob = transition_function[state][action][0][next_state]
                    dict_next_state[dict_states_ser[next_state]] = prob
                rew = transition_function[state][action][1]
                actions_state_ser[dict_act[action]] = (dict_next_state, rew)
            transition_function_ser[dict_states_ser[state]] = actions_state_ser
                
        # create an updated service and add it to the list
        new_service : Service = build_service_from_transitions(transition_function_ser, initial_state_ser, final_states_ser)
        new_services.append(new_service)
    print("\tService encoded.")
    
    # encode target
    print("\tStarting encoding target...")
    
    dict_states_targ = {}
    transition_function_targ : TargetDynamics = {}
    
    # original target
    states = automaton.states
    initial_state = automaton.initial_state
    accepting_states = automaton.accepting_states
    
    in_state = n_elem
    n_elem += 1
    
    # encode states and actions
    for state in states:
        if state not in dict_states_targ:
            dict_states_targ[state] = n_elem
            n_elem += 1
    print(states)
    # encode transition function (from the new created states and actions)
    for state in accepting_states:
        print(state)
        print(automaton.accepting_states)
        input()
        '''actions_state_targ = {}
        for action in tf[state]:
            value_action = tf[state][action]
            state_other = value_action[0]
            prob = value_action[1]
            rew = value_action[2]
            actions_state_targ[dict_act[action]] = (dict_states_targ[state_other], prob, rew)
        transition_function_targ[dict_states_targ[state]] = actions_state_targ'''
    
    # create an updated target
    #new_target : Target = build_target_from_transitions(transition_function_targ, initial_state_targ, final_states_tar)
    print("\tTarget encoded.")
    
    return None, new_services, (in_state, in_action, in_und_action)

def comp_mdp(
    dfa: SimpleDFA, services: Service, automaton: SymbolicDFA, gamma: float = DEFAULT_GAMMA, encode: bool = False
) -> MDP:
    """
    Compute the composition MDP.

    :param target: the target service.
    :param services: the community of services.
    :param automaton: the automaton of the target.
    :param gamma: the discount factor.
    :param encode: if True, encode the services and the target.
    :return: the composition MDP.
    """
    #AlphabetLike = Union[Alphabet[SymbolType], Collection[SymbolType], Set[SymbolType]]
    #print the alphabet of the automaton
    print(dfa.alphabet)
    
    if encode:
        target, services, enc_elems = encode_ltlf(*services, automaton=automaton)
        in_state, in_action, in_und_action = enc_elems
    
    dfa = dfa.trim()
    system_service = build_system_service(*services)

    transition_function: MDPDynamics = {}

    visited = set()
    to_be_visited = set()
    queue: Deque = deque()

    # add initial transitions
    initial_state = (system_service.initial_state, dfa.initial_state)
    queue.append(initial_state)
    to_be_visited.add(initial_state)
    for system_service_state in system_service.states:
        if system_service_state == system_service.initial_state:
            continue
        new_initial_state = (system_service_state, dfa.initial_state)
        queue.append(new_initial_state)
        to_be_visited.add(new_initial_state)

    service_id_to_target_action = {
        service_id: set(dfa.alphabet).intersection(service.actions)
        for service_id, service in enumerate(services)
    }
    target_action_to_service_id = {}
    for service_id, supported_actions in service_id_to_target_action.items():
        assert len(supported_actions) == 1
        supported_action = list(supported_actions)[0]
        target_action_to_service_id.setdefault(supported_action, set()).add(service_id)

    mdp_sink_state_used = False
    while len(queue) > 0:
        cur_state = queue.popleft()
        to_be_visited.remove(cur_state)
        visited.add(cur_state)
        cur_system_state, cur_dfa_state = cur_state
        trans_dist = {}

        next_system_state_trans = system_service.transition_function[
            cur_system_state
        ].items()

        # optimization: filter services, consider only the ones that can do the next DFA action
        next_dfa_actions = set(dfa.transition_function.get(cur_dfa_state, {}).keys())
        allowed_services = set()
        for next_dfa_action in next_dfa_actions:
            allowed_services.update(target_action_to_service_id[next_dfa_action])

        if len(allowed_services) == 0:
            mdp_sink_state_used = True
            trans_dist[COMPOSITION_MDP_UNDEFINED_ACTION] = ({COMPOSITION_MDP_SINK_STATE: 1}, 0.0)
        else:
            # iterate over all available actions of system service
            # in case symbol is in DFA available actions, progress DFA state component
            for (symbol, service_id), next_state_info in next_system_state_trans:

                if service_id not in allowed_services:
                    # this service id cannot do any of the next dfa actions
                    continue

                next_system_state_distr, reward_vector = next_state_info
                system_reward = reward_vector

                # if symbol is a tau action, next dfa state remains the same
                if symbol not in dfa.alphabet:
                    next_dfa_state = cur_dfa_state
                    goal_reward = 0.0
                # if there are no outgoing transitions from DFA state:
                elif cur_dfa_state not in dfa.transition_function:
                    mdp_sink_state_used = True
                    trans_dist[COMPOSITION_MDP_UNDEFINED_ACTION] = ({COMPOSITION_MDP_SINK_STATE: 1}, 0.0)
                    continue
                # symbols not in the transition function of the target
                # are considered as "other"; however, when we add the
                # MDP transition, we will label it with the original
                # symbol.
                elif symbol in dfa.transition_function[cur_dfa_state]:
                    symbol_to_next_dfa_states = dfa.transition_function[cur_dfa_state]
                    next_dfa_state = symbol_to_next_dfa_states[symbol]
                    goal_reward = 1.0 if dfa.is_accepting(next_dfa_state) else 0.0
                else:
                    # if invalid target action, skip
                    continue
                final_rewards = (goal_reward + system_reward)

                for next_system_state, prob in next_system_state_distr.items():
                    assert prob > 0.0
                    next_state = (next_system_state, next_dfa_state)
                    trans_dist.setdefault((symbol, service_id), ({}, final_rewards))[0][
                        next_state
                    ] = prob
                    if next_state not in visited and next_state not in to_be_visited:
                        queue.append(next_state)
                        to_be_visited.add(next_state)

        transition_function[cur_state] = trans_dist

    if mdp_sink_state_used:
        transition_function[COMPOSITION_MDP_SINK_STATE] = {COMPOSITION_MDP_UNDEFINED_ACTION: ({COMPOSITION_MDP_SINK_STATE: 1.0}, 0.0)}

    result = MDP(transition_function, gamma)
    result.initial_state = initial_state
    return result


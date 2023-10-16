from stochastic_service_composition.services import build_service_from_transitions, Service
from stochastic_service_composition.target import build_target_from_transitions
from stochastic_service_composition.declare_utils import *
import logaut
import pylogics.parsers.ldl
from stochastic_service_composition.dfa_target import from_symbolic_automaton_to_declare_automaton

LOW_PROB = 0.05

# probabilities of being broken after an action
DEFAULT_BROKEN_PROB = LOW_PROB
BROKEN_PROB = 0.5
HIGH_BROKEN_PROB = 0.7

# default probability of being unemployable after the configuration
DEFAULT_UNEMPLOYABLE_PROB = LOW_PROB
HIGH_UNEMPLOYABLE_PROB = 0.5

# costs of the machines that perform their job in different countries
DEFAULT_USA_REWARD = -1.0
WAR_REWARD = -3.0
USA_REWARD = -2.0
HIGH_USA_REWARD = -5.0
UK_REWARD = -6.8
CHINA_REWARD = -11.7
TAIWAN_REWARD = -12.2
RUSSIA_REWARD = -9.12 # we have to take into the account political problems
NORWAY_REWARD = -7.16
BRAZIL_REWARD = -6.7
FRANCE_REWARD = -7.6
AUSTRALIA_REWARD = -14.0
INDIA_REWARD = -13.1
BELGIUM_REWARD = -7.6
SWITZERLAND_REWARD = -8.0
CANADA_REWARD = -1.8
PERU_REWARD = -6.0
AUSTRIA_REWARD = -8.38
MALAYSIA_REWARD = -14.73
TURKEY_REWARD = -10.16
KAZAKHSTAN_REWARD = -10.4
CHILE_REWARD = -7.8
BOLIVIA_REWARD = -6.8
ARGENTINA_REWARD = -8.55
MOROCCO_REWARD = -7.9
JAPAN_REWARD = -10.1
SOUTH_KOREA = -10.7
NETHERLANDS_REWARD = -7.5

# default reward when the service becomes broken
DEFAULT_BROKEN_REWARD = -10.0

# all the atomic actions for PHASE 1
PICK_BUY_DESIGN = "pick_buy_design"
PICK_SILICON = "pick_silicon"
PICK_WAFER = "pick_wafer"
PICK_BORON = "pick_boron"
PICK_PHOSPHOR = "pick_phosphor"
PICK_ALUMINUM = "pick_aluminum"
PICK_RESIST = "pick_resist"
PICK_PLASTIC = "pick_plastic"
PICK_CHEMICALS = "pick_chemicals"
PICK_COPPER_FRAME = "pick_copper_frame"

# all the atomic actions for PHASE 2
CLEANING = "cleaning"
CONFIG_FILM_DEPOSITION = "config_film_deposition"
CHECKED_FILM_DEPOSITION = "checked_film_deposition"
FILM_DEPOSITION = "film_deposition"
CONFIG_RESIST_COATING = "config_resist_coating"
CHECKED_RESIST_COATING = "checked_resist_coating"
RESIST_COATING = "resist_coating"
EXPOSURE = "exposure"
CHECK_EXPOSURE = "check_exposure"
CONFIG_DEVELOPMENT = "config_development"
CHECKED_DEVELOPMENT = "checked_development"
DEVELOPMENT = "development"
ETCHING = "etching"
CHECK_ETCHING = "check_etching"
CONFIG_IMPURITIES_IMPLANTATION = "config_impurities_implantation"
CHECKED_IMPURITIES_IMPLANTATION = "checked_impurities_implantation"
IMPURITIES_IMPLANTATION = "impurities_implantation"
ACTIVATION = "activation"
RESIST_STRIPPING = "resist_stripping"
CHECK_RESIST_STRIPPING = "check_resist_stripping"
ASSEMBLY = "assembly"
TESTING = "testing"
PACKAGING = "packaging"

SYMBOLS_PHASE_1 = [
    PICK_BUY_DESIGN,
    PICK_SILICON,
    PICK_WAFER,
    PICK_BORON,
    PICK_PHOSPHOR,
    PICK_ALUMINUM,
    PICK_RESIST,
    PICK_PLASTIC,
    PICK_CHEMICALS,
    PICK_COPPER_FRAME
]

SYMBOLS_PHASE_2 = [
    CLEANING,
    CONFIG_FILM_DEPOSITION,
    CHECKED_FILM_DEPOSITION,
    FILM_DEPOSITION,
    CONFIG_RESIST_COATING,
    CHECKED_RESIST_COATING,
    RESIST_COATING,
    EXPOSURE,
    CHECK_EXPOSURE,
    CONFIG_DEVELOPMENT,
    CHECKED_DEVELOPMENT,
    DEVELOPMENT,
    ETCHING,
    CHECK_ETCHING,
    CONFIG_IMPURITIES_IMPLANTATION,
    CHECKED_IMPURITIES_IMPLANTATION,
    IMPURITIES_IMPLANTATION,
    ACTIVATION,
    RESIST_STRIPPING,
    CHECK_RESIST_STRIPPING,
    ASSEMBLY,
    TESTING,
    PACKAGING
]

# phase1
DESIGN_SERVICE_NAME_USA = "design_usa"                                      # human
DESIGN_SERVICE_NAME_UK = "design_uk"                                        # human
DESIGN_SERVICE_NAME_CHINA = "design_china"                                  # human
DESIGN_SERVICE_NAME_TAIWAN = "design_taiwan"                                # human
SILICON_SERVICE_NAME_CHINA = "silicon_china"                                # warehouse
SILICON_SERVICE_NAME_RUSSIA = "silicon_russia"                              # warehouse
SILICON_SERVICE_NAME_NORWAY = "silicon_norway"                              # warehouse
SILICON_SERVICE_NAME_USA = "silicon_usa"                                    # warehouse
SILICON_SERVICE_NAME_FRANCE = "silicon_france"                              # warehouse
SILICON_SERVICE_NAME_BRAZIL = "silicon_brazil"                              # warehouse
SILICON_SERVICE_NAME_MALAYSIA = "silicon_malaysia"                          # warehouse
WAFER_SERVICE_NAME_JAPAN = "wafer_japan"                                    # warehouse
WAFER_SERVICE_NAME_SOUTH_KOREA = "wafer_south_korea"                        # warehouse
BORON_SERVICE_NAME_TURKEY = "boron_turkey"                                  # warehouse
BORON_SERVICE_NAME_USA = "boron_usa"                                        # warehouse
BORON_SERVICE_NAME_KAZAKHSTAN = "boron_kazakhstan"                          # warehouse
BORON_SERVICE_NAME_CHILE = "boron_chile"                                    # warehouse
BORON_SERVICE_NAME_CHINA = "boron_china"                                    # warehouse
BORON_SERVICE_NAME_ARGENTINA = "boron_argentina"                            # warehouse
BORON_SERVICE_NAME_RUSSIA = "boron_russia"                                  # warehouse
BORON_SERVICE_NAME_BOLIVIA = "boron_bolivia"                                # warehouse
PHOSPHOR_SERVICE_NAME_MOROCCO = "phosphor_morocco"                          # warehouse
PHOSPHOR_SERVICE_NAME_CHINA = "phosphor_china"                              # warehouse
PHOSPHOR_SERVICE_NAME_USA = "phosphor_usa"                                  # warehouse
ALUMINUM_SERVICE_NAME_AUSTRALIA = "aluminum_australia"                      # warehouse
ALUMINUM_SERVICE_NAME_INDIA = "aluminum_india"                              # warehouse
ALUMINUM_SERVICE_NAME_BRAZIL = "aluminum_brazil"                            # warehouse
RESIST_SERVICE_NAME_USA = "resist_usa"                                      # warehouse
RESIST_SERVICE_NAME_BELGIUM = "resist_belgium"                              # warehouse
RESIST_SERVICE_NAME_AUSTRIA = "resist_austria"                              # warehouse
RESIST_SERVICE_NAME_INDIA = "resist_india"                                  # warehouse
RESIST_SERVICE_NAME_SWITZERLAND = "resist_switzerland"                      # warehouse
RESIST_SERVICE_NAME_CANADA = "resist_canada"                                # warehouse
PLASTIC_SERVICE_NAME_CHINA = "plastic_china"                                # warehouse
PLASTIC_SERVICE_NAME_INDIA = "plastic_india"                                # warehouse
CHEMICALS_SERVICE_NAME_USA = "chemicals_usa"                                # warehouse
CHEMICALS_SERVICE_NAME_CANADA = "chemicals_canada"                          # warehouse
COPPER_FRAME_SERVICE_NAME_USA = "copper_frame_usa"                          # warehouse
COPPER_FRAME_SERVICE_NAME_CHINA = "copper_frame_china"                      # warehouse
COPPER_FRAME_SERVICE_NAME_PERU = "copper_frame_peru"                        # warehouse
COPPER_FRAME_SERVICE_NAME_CHILE = "copper_frame_chile"                      # warehouse

# phase2
CLEANING_SERVICE_NAME = "cleaning_human"                                    # human
FILM_DEPOSITION1_SERVICE_NAME = "film_deposition_machine1"                  # machine
FILM_DEPOSITION2_SERVICE_NAME = "film_deposition_machine2"                  # machine
RESIST_COATING1_SERVICE_NAME = "resist_coating_machine1"                    # machine
RESIST_COATING2_SERVICE_NAME = "resist_coating_machine2"                    # machine
EXPOSURE1_SERVICE_NAME = "exposure_machine1"                                # machine
EXPOSURE2_SERVICE_NAME = "exposure_machine2"                                # machine
DEVELOPMENT1_SERVICE_NAME = "development_machine1"                          # machine
DEVELOPMENT2_SERVICE_NAME = "development_machine2"                          # machine
ETCHING1_SERVICE_NAME = "etching_machine1"                                  # machine
ETCHING2_SERVICE_NAME = "etching_machine2"                                  # machine
IMPURITIES_IMPLANTATION1_SERVICE_NAME = "impurities_implantation_machine1"    # machine
IMPURITIES_IMPLANTATION2_SERVICE_NAME = "impurities_implantation_machine2"    # machine
ACTIVATION_SERVICE_NAME = "activation_human"                                # human
RESIST_STRIPPING1_SERVICE_NAME = "resist_stripping_machine1"                # machine
RESIST_STRIPPING2_SERVICE_NAME = "resist_stripping_machine2"                # machine
ASSEMBLY1_SERVICE_NAME = "assembly_human1"                                  # human
ASSEMBLY2_SERVICE_NAME = "assembly_human2"                                  # human
TESTING1_SERVICE_NAME = "testing_human1"                                      # human
TESTING2_SERVICE_NAME = "testing_human2"                                      # human
PACKAGING1_SERVICE_NAME = "packaging_human1"                                  # human
PACKAGING2_SERVICE_NAME = "packaging_human2"                                  # human


def build_generic_breakable_service(service_name: str, action_name: str, broken_prob: float, broken_reward: float, action_reward: float):
    assert 0.0 <= broken_prob <= 1.0
    deterministic_prob = 1.0
    success_prob = deterministic_prob - broken_prob
    transitions = {
        "available": {
            action_name: ({"done": success_prob, "broken": broken_prob}, action_reward),
        },
        "broken": {
            f"check_{action_name}": ({"available": 1.0}, broken_reward),
        },
        "done": {
            f"check_{action_name}": ({"available": 1.0}, 0.0),
        }
    }
    final_states = {"available"}
    initial_state = "available"
    return build_service_from_transitions(transitions, initial_state, final_states)  # type: ignore

def build_complex_breakable_service(service_name: str, action_name: str, broken_prob: float, unemployable_prob: float, broken_reward: float, action_reward: float) -> Service:
    assert 0.0 <= broken_prob <= 1.0
    deterministic_prob = 1.0
    configure_success_prob = deterministic_prob - unemployable_prob
    op_success_prob = deterministic_prob - broken_prob
    transitions = {
        "ready": { # current state
            f"config_{action_name}": # action
                (
                    {
                        "configured": deterministic_prob # next state : prob
                    },
                    0.0
                ),
        },
        "configured": {
            f"checked_{action_name}":
                (
                    {
                    "executing": configure_success_prob,
                    "broken": unemployable_prob
                    } if unemployable_prob > 0.0 else {"executing": configure_success_prob},
                    0.0
                ),
        },
        "executing": {
            action_name: # operation
                (
                    {
                        "ready": op_success_prob,
                        "broken": broken_prob
                    } if broken_prob > 0.0 else {"ready": op_success_prob},
                    action_reward
                ),
        },
        "broken": {
            f"restore_{action_name}":
            (
                {
                        "repairing": deterministic_prob
                },
                broken_reward
            ),
        },
        "repairing": {
            f"repaired_{action_name}":
                (
                    {
                        "ready": deterministic_prob
                    },
                    0.0
                ),
        },

    }
    final_states = {"ready"}
    initial_state = "ready"
    return build_service_from_transitions(transitions, initial_state, final_states)  # type: ignore

def build_generic_service_one_state(
    service_name: str,
    operation_names: Set[str],
    action_reward: float,
) -> Service:
    """Build the one state device."""
    transitions = {
        "ready": {
            operation_name: ({"ready": 1.0}, action_reward) for operation_name in operation_names
        },
    }
    final_states = {"ready"}
    initial_state = "ready"
    return build_service_from_transitions(transitions, initial_state, final_states)  # type: ignore


# PHASE 1
def design_service(name: str, action_reward: float) -> Service:
    """Build the design device."""
    return build_generic_service_one_state(
        name,
        {PICK_BUY_DESIGN},
        action_reward=action_reward
    )

def silicon_warehouse_service(name: str, action_reward) -> Service:
    """Build the silicon warehouse device."""
    return build_generic_service_one_state(
        name,
        {PICK_SILICON},
        action_reward=action_reward
    )

def wafer_warehouse_service(name: str, action_reward: float) -> Service:
    """Build the wafer warehouse device."""
    return build_generic_service_one_state(
        name,
        {PICK_WAFER},
        action_reward=action_reward
    )

def boron_warehouse_service(name: str, action_reward: float) -> Service:
    """Build the boron warehouse device."""
    return build_generic_service_one_state(
        name,
        {PICK_BORON},
        action_reward=action_reward
    )

def phosphor_warehouse_service(name: str, action_reward: float) -> Service:
    """Build the phosphor warehouse device."""
    return build_generic_service_one_state(
        name,
        {PICK_PHOSPHOR},
        action_reward=action_reward
    )

def aluminum_warehouse_service(name: str, action_reward: float) -> Service:
    """Build the aluminum warehouse device."""
    return build_generic_service_one_state(
        name,
        {PICK_ALUMINUM},
        action_reward=action_reward
    )

def resist_warehouse_service(name: str, action_reward: float) -> Service:
    """Build the resist warehouse device."""
    return build_generic_service_one_state(
        name,
        {PICK_RESIST},
        action_reward=action_reward
    )

def plastic_warehouse_service(name: str, action_reward: float) -> Service:
    """Build the plastic warehouse device."""
    return build_generic_service_one_state(
        name,
        {PICK_PLASTIC},
        action_reward=action_reward
    )

def chemicals_warehouse_service(name: str, action_reward: float) -> Service:
    """Build the chemicals warehouse device."""
    return build_generic_service_one_state(
        name,
        {PICK_CHEMICALS},
        action_reward=action_reward
    )

def copper_frame_warehouse_service(name: str, action_reward: float) -> Service:
    """Build the copper frame warehouse device."""
    return build_generic_service_one_state(
        name,
        {PICK_COPPER_FRAME},
        action_reward=action_reward
    )


# PHASE 2
def cleaning_service(name: str = CLEANING_SERVICE_NAME, action_reward: float = USA_REWARD) -> Service:
    """Build the human cleaning device."""
    return build_generic_service_one_state(
        name,
        {CLEANING},
        action_reward=action_reward
    )

def film_deposition_service(name: str, broken_prob: float, unemployable_prob: float, broken_reward: float,
                        action_reward: float) -> Service:
    """Build the film deposition device."""
    return build_complex_breakable_service(name, FILM_DEPOSITION, broken_prob=broken_prob,
                                        unemployable_prob=unemployable_prob, broken_reward=broken_reward,
                                        action_reward=action_reward)

def resist_coating_service(name: str, broken_prob: float, unemployable_prob: float, broken_reward: float,
                            action_reward: float) -> Service:
    """Build the resist coating device."""
    return build_complex_breakable_service(name, RESIST_COATING, broken_prob=broken_prob,
                                        unemployable_prob=unemployable_prob, broken_reward=broken_reward,
                                        action_reward=action_reward)

def exposure_service(name: str, broken_prob: float, broken_reward: float, action_reward: float) -> Service:
    """Build the exposure device."""
    return build_generic_breakable_service(name, EXPOSURE, broken_prob=broken_prob, broken_reward=broken_reward,
                                        action_reward=action_reward)

def development_service(name: str, broken_prob: float, unemployable_prob: float, broken_reward: float,
                        action_reward: float) -> Service:
    """Build the development device."""
    return build_complex_breakable_service(name, DEVELOPMENT, broken_prob=broken_prob,
                                        unemployable_prob=unemployable_prob, broken_reward=broken_reward,
                                        action_reward=action_reward)

def etching_service(name: str, broken_prob: float, broken_reward: float, action_reward: float) -> Service:
    """Build the etching device."""
    return build_generic_breakable_service(name, ETCHING, broken_prob=broken_prob, broken_reward=broken_reward,
                                        action_reward=action_reward)

def impurities_implantation_service(name: str, broken_prob: float, unemployable_prob: float, broken_reward: float,
                                action_reward: float) -> Service:
    """Build the impurities implantation device."""
    return build_complex_breakable_service(name, IMPURITIES_IMPLANTATION, broken_prob=broken_prob,
                                        unemployable_prob=unemployable_prob, broken_reward=broken_reward,
                                        action_reward=action_reward)

def activation_service(name: str = ACTIVATION_SERVICE_NAME, action_reward: float = USA_REWARD) -> Service:
    """Build the human activation device."""
    return build_generic_service_one_state(
        name,
        {ACTIVATION},
        action_reward=action_reward
    )

def resist_stripping_service(name: str, broken_prob: float, broken_reward: float, action_reward: float) -> Service:
    """Build the resist stripping device."""
    return build_generic_breakable_service(name, RESIST_STRIPPING, broken_prob=broken_prob, broken_reward=broken_reward,
                                        action_reward=action_reward)

def assembly_service(name: str, action_reward: float = USA_REWARD) -> Service:
    """Build the human assembly device."""
    return build_generic_service_one_state(
        name,
        {ASSEMBLY},
        action_reward=action_reward
    )

def testing_service(name: str, action_reward: float = USA_REWARD) -> Service:
    """Build the human testing device."""
    return build_generic_service_one_state(
        name,
        {TESTING},
        action_reward=action_reward
    )
    
def packaging_service(name: str, action_reward: float = USA_REWARD) -> Service:
    """Build the human packaging device."""
    return build_generic_service_one_state(
        name,
        {PACKAGING},
        action_reward=action_reward
    )

# PHASE 1
service_design_usa = design_service(DESIGN_SERVICE_NAME_USA, USA_REWARD)
service_design_uk = design_service(DESIGN_SERVICE_NAME_UK, UK_REWARD)
service_design_china = design_service(DESIGN_SERVICE_NAME_CHINA, CHINA_REWARD)
service_design_taiwan = design_service(DESIGN_SERVICE_NAME_TAIWAN, TAIWAN_REWARD)
service_silicon_china = silicon_warehouse_service(SILICON_SERVICE_NAME_CHINA, CHINA_REWARD)
service_silicon_russia = silicon_warehouse_service(SILICON_SERVICE_NAME_RUSSIA, RUSSIA_REWARD + WAR_REWARD)
service_silicon_norway = silicon_warehouse_service(SILICON_SERVICE_NAME_NORWAY, NORWAY_REWARD)
service_silicon_usa = silicon_warehouse_service(SILICON_SERVICE_NAME_USA, USA_REWARD)
service_silicon_brazil = silicon_warehouse_service(SILICON_SERVICE_NAME_BRAZIL, BRAZIL_REWARD)
service_silicon_france = silicon_warehouse_service(SILICON_SERVICE_NAME_FRANCE, FRANCE_REWARD)
service_silicon_malaysia = silicon_warehouse_service(SILICON_SERVICE_NAME_MALAYSIA, MALAYSIA_REWARD)
service_wafer_japan = wafer_warehouse_service(WAFER_SERVICE_NAME_JAPAN, JAPAN_REWARD)
service_wafer_south_korea = wafer_warehouse_service(WAFER_SERVICE_NAME_SOUTH_KOREA, SOUTH_KOREA)
service_boron_turkey = boron_warehouse_service(BORON_SERVICE_NAME_TURKEY, TURKEY_REWARD)
service_boron_usa = boron_warehouse_service(BORON_SERVICE_NAME_USA, USA_REWARD)
service_boron_kazakhstan = boron_warehouse_service(BORON_SERVICE_NAME_KAZAKHSTAN, KAZAKHSTAN_REWARD)
service_boron_chile = boron_warehouse_service(BORON_SERVICE_NAME_CHILE, CHILE_REWARD)
service_boron_china = boron_warehouse_service(BORON_SERVICE_NAME_CHINA, CHINA_REWARD)
service_boron_bolivia = boron_warehouse_service(BORON_SERVICE_NAME_BOLIVIA, BOLIVIA_REWARD)
service_boron_argentina = boron_warehouse_service(BORON_SERVICE_NAME_ARGENTINA, ARGENTINA_REWARD)
service_boron_russia = boron_warehouse_service(BORON_SERVICE_NAME_RUSSIA, RUSSIA_REWARD + WAR_REWARD)
service_phosphor_morocco = phosphor_warehouse_service(PHOSPHOR_SERVICE_NAME_MOROCCO, MOROCCO_REWARD)
service_phosphor_china = phosphor_warehouse_service(PHOSPHOR_SERVICE_NAME_CHINA, CHINA_REWARD)
service_phosphor_usa = phosphor_warehouse_service(PHOSPHOR_SERVICE_NAME_USA, USA_REWARD)
service_aluminum_australia = aluminum_warehouse_service(ALUMINUM_SERVICE_NAME_AUSTRALIA, AUSTRALIA_REWARD)
service_aluminum_india = aluminum_warehouse_service(ALUMINUM_SERVICE_NAME_INDIA, INDIA_REWARD)
service_aluminum_brazil = aluminum_warehouse_service(ALUMINUM_SERVICE_NAME_BRAZIL, BRAZIL_REWARD)
service_resist_usa = resist_warehouse_service(RESIST_SERVICE_NAME_USA, USA_REWARD)
service_resist_belgium = resist_warehouse_service(RESIST_SERVICE_NAME_BELGIUM, BELGIUM_REWARD)
service_resist_austria = resist_warehouse_service(RESIST_SERVICE_NAME_AUSTRIA, AUSTRIA_REWARD)
service_resist_india = resist_warehouse_service(RESIST_SERVICE_NAME_INDIA, INDIA_REWARD)
service_resist_switzerland = resist_warehouse_service(RESIST_SERVICE_NAME_SWITZERLAND, SWITZERLAND_REWARD)
service_resist_canada = resist_warehouse_service(RESIST_SERVICE_NAME_CANADA, CANADA_REWARD)
service_plastic_china = plastic_warehouse_service(PLASTIC_SERVICE_NAME_CHINA, CHINA_REWARD)
service_plastic_india = plastic_warehouse_service(PLASTIC_SERVICE_NAME_INDIA, INDIA_REWARD)
service_chemicals_usa = chemicals_warehouse_service(CHEMICALS_SERVICE_NAME_USA, USA_REWARD)
service_chemicals_canada = chemicals_warehouse_service(CHEMICALS_SERVICE_NAME_CANADA, CANADA_REWARD)
service_copper_frame_usa = copper_frame_warehouse_service(COPPER_FRAME_SERVICE_NAME_USA, USA_REWARD)
service_copper_frame_china = copper_frame_warehouse_service(COPPER_FRAME_SERVICE_NAME_CHINA, CHINA_REWARD)
service_copper_frame_peru = copper_frame_warehouse_service(COPPER_FRAME_SERVICE_NAME_PERU, PERU_REWARD)
service_copper_frame_chile = copper_frame_warehouse_service(COPPER_FRAME_SERVICE_NAME_CHILE, CHILE_REWARD)

# PHASE 2
service_cleaning = cleaning_service()
service_film_deposition1 = film_deposition_service(FILM_DEPOSITION1_SERVICE_NAME, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
service_film_deposition2 = film_deposition_service(FILM_DEPOSITION2_SERVICE_NAME, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD)
service_resist_coating1 = resist_coating_service(RESIST_COATING1_SERVICE_NAME, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
service_resist_coating2 = resist_coating_service(RESIST_COATING2_SERVICE_NAME, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD)
service_exposure1 = exposure_service(EXPOSURE1_SERVICE_NAME, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
service_exposure2 = exposure_service(EXPOSURE2_SERVICE_NAME, BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD)
service_development1 = development_service(DEVELOPMENT1_SERVICE_NAME, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
service_development2 = development_service(DEVELOPMENT2_SERVICE_NAME, BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD)
service_etching1 = etching_service(ETCHING1_SERVICE_NAME, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
service_etching2 = etching_service(ETCHING2_SERVICE_NAME, BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD)
service_impurities_implantation1 = impurities_implantation_service(IMPURITIES_IMPLANTATION1_SERVICE_NAME, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
service_impurities_implantation2 = impurities_implantation_service(IMPURITIES_IMPLANTATION2_SERVICE_NAME, BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD)
service_activation = activation_service()
service_resist_stripping1 = resist_stripping_service(RESIST_STRIPPING1_SERVICE_NAME, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
service_resist_stripping2 = resist_stripping_service(RESIST_STRIPPING2_SERVICE_NAME, BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD)
service_assembly1 = assembly_service(ASSEMBLY1_SERVICE_NAME)
service_assembly2 = assembly_service(ASSEMBLY2_SERVICE_NAME, HIGH_USA_REWARD)
service_testing1 = testing_service(TESTING1_SERVICE_NAME)
service_testing2 = testing_service(TESTING2_SERVICE_NAME, HIGH_USA_REWARD)
service_packaging1 = packaging_service(PACKAGING1_SERVICE_NAME)
service_packaging2 = packaging_service(PACKAGING2_SERVICE_NAME, HIGH_USA_REWARD)

# creare 60 servizi per la fase 2 per testare la size COMPLEX

def target_service_phase1_automata():
    """Build the target service."""
    transition_function = {
        "s0": {"pick_buy_design": ("s1", 1.0, 0),},
        "s1": {"pick_silicon": ("s2", 1.0, 0),},
        "s2": {"pick_wafer": ("s3", 1.0, 0),},
        "s3": {"pick_boron": ("s4", 1.0, 0), },
        "s4": {"pick_phosphor": ("s5", 1.0, 0), },
        "s5": {"pick_aluminum": ("s6", 1.0, 0), },
        "s6": {"pick_resist": ("s7", 1.0, 0), },
        "s7": {"pick_plastic": ("s8", 1.0, 0), },
        "s8": {"pick_chemicals": ("s9", 1.0, 0), },
        "s9": {"pick_copper_frame": ("s0", 1.0, 0), },
    }

    initial_state = "s0"
    final_states = {"s0"}

    return build_target_from_transitions(
        transition_function, initial_state, final_states
    )
    
def target_service_phase1_ltlf():
    regex_seq = ""
    for symbol_index, symbol in enumerate(SYMBOLS_PHASE_1):
        all_but_symbol = set(SYMBOLS_PHASE_1).difference({symbol})
        item = symbol + "&" + " & ".join(map(lambda x: "!" + x, all_but_symbol))
        regex_seq = regex_seq + (";" if symbol_index != 0 else "") + item
    formula_str = f"<({regex_seq})*>end"
    formula = pylogics.parsers.ldl.parse_ldl(formula_str)
    automaton = logaut.core.ldl2dfa(formula, backend="lydia")
    #print("Specification: ", formula_str)
    #print("Compute declare automaton")
    declare_automaton = from_symbolic_automaton_to_declare_automaton(automaton, set(SYMBOLS_PHASE_1))
    return declare_automaton
    
def target_service_phase2_automata():
    """Build the target service."""
    transition_function = {
        "s0": {"cleaning": ("s1", 1.0, 0), },
        "s1": {"config_film_deposition": ("s2", 1.0, 0), },
        "s2": {"checked_film_deposition": ("s3", 1.0, 0), },
        "s3": {"film_deposition": ("s4", 1.0, 0), },
        "s4": {"config_resist_coating": ("s5", 1.0, 0), },
        "s5": {"checked_resist_coating": ("s6", 1.0, 0), },
        "s6": {"resist_coating": ("s7", 1.0, 0), },
        "s7": {"exposure": ("s8", 1.0, 0), },
        "s8": {"check_exposure": ("s9", 1.0, 0), },
        "s9": {"config_development": ("s10", 1.0, 0), },
        "s10": {"checked_development": ("s11", 1.0, 0), },
        "s11": {"development": ("s12", 1.0, 0), },
        "s12": {"etching": ("s13", 1.0, 0), },
        "s13": {"check_etching": ("s14", 1.0, 0), },
        "s14": {"config_impurities_implantation": ("s15", 1.0, 0), },
        "s15": {"checked_impurities_implantation": ("s16", 1.0, 0), },
        "s16": {"impurities_implantation": ("s17", 1.0, 0), },
        "s17": {"activation": ("s18", 1.0, 0), },
        "s18": {"resist_stripping": ("s19", 1.0, 0), },
        "s19": {"check_resist_stripping": ("s20", 1.0, 0), },
        "s20": {"assembly": ("s21", 1.0, 0), },
        "s21": {"testing": ("s22", 1.0, 0), },
        "s22": {"packaging": ("s0", 1.0, 0), }
    }

    initial_state = "s0"
    final_states = {"s0"}

    return build_target_from_transitions(
        transition_function, initial_state, final_states
    )
    
def target_service_phase2_ltlf():
    formula_str = "<"
    regex_seq = ""
    for symbol_index, symbol in enumerate(SYMBOLS_PHASE_2):
        all_but_symbol = set(SYMBOLS_PHASE_2).difference({symbol})
        item = symbol + " & " + " & ".join(map(lambda x: "!" + x, all_but_symbol))
        regex_seq = regex_seq + (";" if symbol_index != 0 else "") + item
    formula_str = f"<({regex_seq})*>end"
    formula = pylogics.parsers.ldl.parse_ldl(formula_str)
    automaton = logaut.core.ldl2dfa(formula, backend="lydia")
    #print("Specification: ", formula_str)
    declare_automaton = from_symbolic_automaton_to_declare_automaton(automaton, set(SYMBOLS_PHASE_2))
    return declare_automaton
    
    
def services_phase2 (dimension):
    if dimension == "small":
        all_services = [
            # 0
            service_cleaning,
            # 1
            service_film_deposition1,
            # 2
            service_resist_coating1,
            # 3
            service_exposure1,
            # 4
            service_exposure2,
            # 5
            service_development1,
            # 6
            service_etching1,
            # 7
            service_impurities_implantation1,
            # 8
            service_activation,
            # 9
            service_resist_stripping1,
            # 10
            service_resist_stripping2,
            # 11
            service_assembly1,
            # 12
            service_testing1,
            # 13
            service_packaging1
        ]
    elif dimension == "manageable1":
        all_services = [
            # 0
            service_cleaning,
            # 1
            service_film_deposition1,
            # 2
            service_film_deposition2,
            # 3
            service_resist_coating1,
            # 4
            service_resist_coating2,
            # 5
            service_exposure1,
            # 6
            service_exposure2,
            # 7
            service_development1,
            # 8
            service_development2,
            # 9
            service_etching1,
            # 10
            service_impurities_implantation1,
            # 11
            service_activation,
            # 12
            service_resist_stripping1,
            # 13
            service_resist_stripping2,
            # 14
            service_assembly1,
            # 15
            service_testing1,
            # 16
            service_packaging1
        ]
    elif dimension == "manageable2":
        all_services = [
            # 0
            service_cleaning,
            # 1
            service_film_deposition1,
            # 2
            service_film_deposition2,
            # 3
            service_resist_coating1,
            # 4
            service_resist_coating2,
            # 5
            service_exposure1,
            # 6
            service_exposure2,
            # 7
            service_development1,
            # 8
            service_development2,
            # 9
            service_etching1,
            # 10
            service_etching2,
            # 11
            service_impurities_implantation1,
            # 12
            service_impurities_implantation2,
            # 13
            service_activation,
            # 14
            service_resist_stripping1,
            # 15
            service_resist_stripping2,
            # 16
            service_assembly1,
            # 17
            service_assembly2,
            # 18
            service_testing1,
            # 19
            service_testing2,
            # 20
            service_packaging1,
            # 21
            service_packaging2
        ]
    elif dimension == "complex":
        #TODO create lot of services
        return
    
    return all_services

all_services_phase1 = [
    # 0
    service_design_usa,
    # 1
    service_design_uk,
    # 2
    service_design_china,
    # 3
    service_design_taiwan,
    # 4
    service_silicon_china,
    # 5
    service_silicon_russia,
    # 6
    service_silicon_norway,
    # 7
    service_silicon_usa,
    # 8
    service_silicon_brazil,
    # 9
    service_silicon_france,
    # 10
    service_silicon_malaysia,
    # 11
    service_wafer_japan,
    # 12
    service_wafer_south_korea,
    # 13
    service_boron_turkey,
    # 14
    service_boron_usa,
    # 15
    service_boron_kazakhstan,
    # 16
    service_boron_chile,
    # 17
    service_boron_china,
    # 18
    service_boron_bolivia,
    # 19
    service_boron_argentina,
    # 20
    service_boron_russia,
    # 21
    service_phosphor_morocco,
    # 22
    service_phosphor_china,
    # 23
    service_phosphor_usa,
    # 24
    service_aluminum_brazil,
    # 25
    service_aluminum_india,
    # 26
    service_aluminum_australia,
    # 27
    service_resist_switzerland,
    # 28
    service_resist_usa,
    # 29
    service_resist_austria,
    # 30
    service_resist_belgium,
    # 31
    service_resist_canada,
    # 32
    service_resist_india,
    # 33
    service_plastic_india,
    # 34
    service_plastic_china,
    # 35
    service_chemicals_usa,
    # 36
    service_chemicals_canada,
    # 37
    service_copper_frame_usa,
    # 38
    service_copper_frame_chile,
    # 39
    service_copper_frame_peru,
    # 40
    service_copper_frame_china
]
target_phase1_automata = target_service_phase1_automata()
target_phase1_ltlf = target_service_phase1_ltlf()

all_services_phase2_small = services_phase2("small")
all_services_phase2_manageable1 = services_phase2("manageable1")
all_services_phase2_manageable2 = services_phase2("manageable2")
all_services_phase2_complex = services_phase2("complex")
target_phase2_automata = target_service_phase2_automata()
target_phase2_ltlf = target_service_phase2_ltlf()
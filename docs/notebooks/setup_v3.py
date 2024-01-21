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
USA_REWARD = -2.0
HIGH_USA_REWARD = -5.0
UK_REWARD = -6.8
CHINA_REWARD = -11.7
TAIWAN_REWARD = -12.2
RUSSIA_REWARD = -9.12 
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


# actions terms
PICK_DESIGN = "p_d"
PICK_SILICON = "p_s"
PICK_IMPURITIES = "p_i"
PICK_RESIST = "p_r"
PICK_CHEMICALS = "p_c"

MASK_CREATION = "cr_m"
PHOTOLITOGRAPHY = "ph_l"
ION_IMPLANTATION = "ion_i"

TESTING = "tes"
TESTING_QUALITY = "tes_qua"

QUALITY = "qua"

DICING = "dic"

CLASSIC_PACKAGING = "pac"  
THERMAL_PACKAGING = "pac_t"     #for cooling of GPU


# service names
DESIGN_SERVICE_NAME_USA = "p_d_usa"
DESIGN_SERVICE_NAME_UK = "p_d_uk"
DESIGN_SERVICE_NAME_CHINA = "p_d_ch"
DESIGN_SERVICE_NAME_TAIWAN = "p_d_tw"

SILICON_SERVICE_NAME_CHINA = "p_s_chi"
SILICON_SERVICE_NAME_RUSSIA = "p_s_ru"
SILICON_SERVICE_NAME_NORWAY = "p_s_nw"
SILICON_SERVICE_NAME_USA = "p_s_usa"
SILICON_SERVICE_NAME_FRANCE = "p_s_fr"
SILICON_SERVICE_NAME_BRAZIL = "p_s_br"
SILICON_SERVICE_NAME_MALAYSIA = "p_s_mal"

IMPURITIES_SERVICE_NAME_USA = "p_i_usa"
IMPURITIES_SERVICE_NAME_CHILE = "p_i_chi"
IMPURITIES_SERVICE_NAME_CHINA = "p_i_ch"
IMPURITIES_SERVICE_NAME_BRAZIL = "p_i_br"

RESIST_SERVICE_NAME_USA = "p_r_usa"
RESIST_SERVICE_NAME_BELGIUM = "p_r_be"
RESIST_SERVICE_NAME_AUSTRIA = "p_r_au"
RESIST_SERVICE_NAME_INDIA = "p_r_in"
RESIST_SERVICE_NAME_SWITZERLAND = "p_r_sw"
RESIST_SERVICE_NAME_CANADA = "p_r_ca"

CHEMICALS_SERVICE_NAME_USA = "chemicals_usa"
CHEMICALS_SERVICE_NAME_CANADA = "chemicals_ca"

MASK_CREATION1_SERVICE_NAME = "cr_m_1"
MASK_CREATION2_SERVICE_NAME = "cr_m_2"

PHOTOLITOGRAPHY1_SERVICE_NAME = "ph_l_1"
PHOTOLITOGRAPHY2_SERVICE_NAME = "ph_l_2"

ION_IMPLANTATION1_SERVICE_NAME = "ion_i_m_1"
ION_IMPLANTATION2_SERVICE_NAME = "ion_i_m_2"

TESTING1_SERVICE_NAME = "tes_m_1"
TESTING2_SERVICE_NAME = "tes_m_2"

TESTING_QUALITY1_SERVICE_NAME = "tes_qua_m_1"
TESTING_QUALITY2_SERVICE_NAME = "tes_qua_m_2"

QUALITY1_SERVICE_NAME = "qua_m_1"
QUALITY2_SERVICE_NAME = "qua_m_2"

DICING1_SERVICE_NAME = "dic_m_1"
DICING2_SERVICE_NAME = "dic_m_2"

PACKAGING1_SERVICE_NAME = "pac_m_1"
PACKAGING2_SERVICE_NAME = "pac_m_2"

THERMAL_PACKAGING1_SERVICE_NAME = "pac_t_m_1"
THERMAL_PACKAGING2_SERVICE_NAME = "pac_t_m_2"


def build_generic_service_one_state(
    service_name: str,
    operation_names: Set[str],
    action_reward: float,
) -> Service:
    '''1-state service: ready'''
    transitions = {
        "re": {
            operation_name: ({"re": 1.0}, action_reward) for operation_name in operation_names
        },
    }
    final_states = {"re"}
    initial_state = "re"
    return build_service_from_transitions(transitions, initial_state, final_states, service_name=service_name)  # type: ignore


def build_generic_breakable_service(service_name: str, action_name: str, broken_prob: float, broken_reward: float, action_reward: float):
    '''3-states service: available, broken, done'''
    assert 0.0 <= broken_prob <= 1.0
    deterministic_prob = 1.0
    success_prob = deterministic_prob - broken_prob
    transitions = {
        "av": {
            action_name: ({"do": success_prob, "br": broken_prob}, action_reward),
        },
        "br": {
            f"ch_{action_name}": ({"av": 1.0}, broken_reward),
        },
        "do": {
            f"ch_{action_name}": ({"av": 1.0}, 0.0),
        }
    }
    final_states = {"av"}
    initial_state = "av"
    return build_service_from_transitions(transitions, initial_state, final_states, service_name=service_name)  # type: ignore


def build_complex_breakable_service(service_name: str, action_name: str, broken_prob: float, unemployable_prob: float, broken_reward: float, action_reward: float) -> Service:
    '''5-states service: ready, configured, executing, broken, repaired'''
    assert 0.0 <= broken_prob <= 1.0
    deterministic_prob = 1.0
    configure_success_prob = deterministic_prob - unemployable_prob
    op_success_prob = deterministic_prob - broken_prob
    transitions = {
        "re": { # current state
            f"con_{action_name}": # action
                (
                    {
                        "con": deterministic_prob # next state : prob
                    },
                    0.0
                ),
        },
        "con": {
            f"che_{action_name}":
                (
                    {
                    "ex": configure_success_prob,
                    "br": unemployable_prob
                    } if unemployable_prob > 0.0 else {"ex": configure_success_prob},
                    0.0
                ),
        },
        "ex": {
            action_name: # operation
                (
                    {
                        "re": op_success_prob,
                        "br": broken_prob
                    } if broken_prob > 0.0 else {"re": op_success_prob},
                    action_reward
                ),
        },
        "br": {
            f"res_{action_name}":
            (
                {
                        "rep": deterministic_prob
                },
                broken_reward
            ),
        },
        "rep": {
            f"rep_{action_name}":
                (
                    {
                        "re": deterministic_prob
                    },
                    0.0
                ),
        },

    }
    final_states = {"re"}
    initial_state = "re"
    return build_service_from_transitions(transitions, initial_state, final_states, service_name=service_name)  # type: ignore


def process_services(mode, dimension):
    '''Builds all the services for the given dimension of the problem.'''
    if mode == "automata" and dimension == "small":
        all_services = [
            build_generic_service_one_state(DESIGN_SERVICE_NAME_USA, {PICK_DESIGN}, USA_REWARD),
            # #build_generic_service_one_state(DESIGN_SERVICE_NAME_CHINA, {PICK_DESIGN}, CHINA_REWARD),
            #
            # build_generic_service_one_state(SILICON_SERVICE_NAME_USA, {PICK_SILICON}, USA_REWARD),
            # #build_generic_service_one_state(SILICON_SERVICE_NAME_BRAZIL, {PICK_SILICON}, BRAZIL_REWARD),
            # #build_generic_service_one_state(SILICON_SERVICE_NAME_CHINA, {PICK_SILICON}, CHINA_REWARD),
            #
            # build_generic_service_one_state(IMPURITIES_SERVICE_NAME_USA, {PICK_IMPURITIES}, USA_REWARD),
            # #build_generic_service_one_state(IMPURITIES_SERVICE_NAME_CHILE, {PICK_IMPURITIES}, CHILE_REWARD),
            #
            # build_generic_service_one_state(RESIST_SERVICE_NAME_USA, {PICK_RESIST}, USA_REWARD),
            # #build_generic_service_one_state(RESIST_SERVICE_NAME_CANADA, {PICK_RESIST}, CANADA_REWARD),
            #
            # build_generic_service_one_state(CHEMICALS_SERVICE_NAME_USA, {PICK_CHEMICALS}, USA_REWARD),
            # #build_generic_service_one_state(CHEMICALS_SERVICE_NAME_CANADA, {PICK_CHEMICALS}, CANADA_REWARD),
            #
            build_complex_breakable_service(MASK_CREATION1_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            # #build_complex_breakable_service(MASK_CREATION2_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),
            #
            # build_generic_breakable_service(PHOTOLITOGRAPHY1_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #
            # build_generic_breakable_service(ION_IMPLANTATION1_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #
            # build_generic_breakable_service(TESTING1_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #
            # build_generic_breakable_service(TESTING_QUALITY1_SERVICE_NAME, TESTING_QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #
            # build_complex_breakable_service(QUALITY1_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #
            # build_complex_breakable_service(DICING1_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            # #build_complex_breakable_service(DICING2_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),
            #
            # build_generic_breakable_service(PACKAGING1_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #
            # build_generic_breakable_service(THERMAL_PACKAGING1_SERVICE_NAME, THERMAL_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
        ]
    elif mode == "automata" and dimension == "medium":
        all_services = [
            build_generic_service_one_state(DESIGN_SERVICE_NAME_USA, {PICK_DESIGN}, USA_REWARD),
            build_generic_service_one_state(DESIGN_SERVICE_NAME_CHINA, {PICK_DESIGN}, CHINA_REWARD),
            #build_generic_service_one_state(DESIGN_SERVICE_NAME_UK, {PICK_DESIGN}, UK_REWARD),
        
            build_generic_service_one_state(SILICON_SERVICE_NAME_USA, {PICK_SILICON}, USA_REWARD),
            build_generic_service_one_state(SILICON_SERVICE_NAME_BRAZIL, {PICK_SILICON}, BRAZIL_REWARD),
            build_generic_service_one_state(SILICON_SERVICE_NAME_CHINA, {PICK_SILICON}, CHINA_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_RUSSIA, {PICK_SILICON}, RUSSIA_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_NORWAY, {PICK_SILICON}, NORWAY_REWARD),
        
            build_generic_service_one_state(IMPURITIES_SERVICE_NAME_USA, {PICK_IMPURITIES}, USA_REWARD),
            build_generic_service_one_state(IMPURITIES_SERVICE_NAME_CHILE, {PICK_IMPURITIES}, CHILE_REWARD),
            #build_generic_service_one_state(IMPURITIES_SERVICE_NAME_BRAZIL, {PICK_IMPURITIES}, BRAZIL_REWARD),

            build_generic_service_one_state(RESIST_SERVICE_NAME_USA, {PICK_RESIST}, USA_REWARD),
            build_generic_service_one_state(RESIST_SERVICE_NAME_CANADA, {PICK_RESIST}, CANADA_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_INDIA, {PICK_RESIST}, INDIA_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_SWITZERLAND, {PICK_RESIST}, SWITZERLAND_REWARD),
        
            build_generic_service_one_state(CHEMICALS_SERVICE_NAME_USA, {PICK_CHEMICALS}, USA_REWARD),
            build_generic_service_one_state(CHEMICALS_SERVICE_NAME_CANADA, {PICK_CHEMICALS}, CANADA_REWARD),

            build_complex_breakable_service(MASK_CREATION1_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #build_complex_breakable_service(MASK_CREATION2_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PHOTOLITOGRAPHY1_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(PHOTOLITOGRAPHY2_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(ION_IMPLANTATION1_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(ION_IMPLANTATION2_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(TESTING1_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(TESTING_QUALITY1_SERVICE_NAME, TESTING_QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(QUALITY1_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(DICING1_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(DICING2_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PACKAGING1_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(THERMAL_PACKAGING1_SERVICE_NAME, THERMAL_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
        ]
    elif mode == "automata" and dimension == "large":
        all_services = [
            build_generic_service_one_state(DESIGN_SERVICE_NAME_USA, {PICK_DESIGN}, USA_REWARD),
            build_generic_service_one_state(DESIGN_SERVICE_NAME_UK, {PICK_DESIGN}, UK_REWARD),
            build_generic_service_one_state(DESIGN_SERVICE_NAME_CHINA, {PICK_DESIGN}, CHINA_REWARD),
            #build_generic_service_one_state(DESIGN_SERVICE_NAME_TAIWAN, {PICK_DESIGN}, TAIWAN_REWARD),

            build_generic_service_one_state(SILICON_SERVICE_NAME_BRAZIL, {PICK_SILICON}, BRAZIL_REWARD),
            build_generic_service_one_state(SILICON_SERVICE_NAME_CHINA, {PICK_SILICON}, CHINA_REWARD),
            build_generic_service_one_state(SILICON_SERVICE_NAME_RUSSIA, {PICK_SILICON}, RUSSIA_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_NORWAY, {PICK_SILICON}, NORWAY_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_USA, {PICK_SILICON}, USA_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_FRANCE, {PICK_SILICON}, FRANCE_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_MALAYSIA, {PICK_SILICON}, MALAYSIA_REWARD),

            build_generic_service_one_state(IMPURITIES_SERVICE_NAME_USA, {PICK_IMPURITIES}, USA_REWARD),
            build_generic_service_one_state(IMPURITIES_SERVICE_NAME_CHILE, {PICK_IMPURITIES}, CHILE_REWARD),
            #build_generic_service_one_state(IMPURITIES_SERVICE_NAME_CHINA, {PICK_IMPURITIES}, CHINA_REWARD),
            #build_generic_service_one_state(IMPURITIES_SERVICE_NAME_BRAZIL, {PICK_IMPURITIES}, BRAZIL_REWARD),

            build_generic_service_one_state(RESIST_SERVICE_NAME_USA, {PICK_RESIST}, USA_REWARD),
            build_generic_service_one_state(RESIST_SERVICE_NAME_BELGIUM, {PICK_RESIST}, BELGIUM_REWARD),
            build_generic_service_one_state(RESIST_SERVICE_NAME_AUSTRIA, {PICK_RESIST}, AUSTRIA_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_INDIA, {PICK_RESIST}, INDIA_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_SWITZERLAND, {PICK_RESIST}, SWITZERLAND_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_CANADA, {PICK_RESIST}, CANADA_REWARD),

            build_generic_service_one_state(CHEMICALS_SERVICE_NAME_USA, {PICK_CHEMICALS}, USA_REWARD),
            build_generic_service_one_state(CHEMICALS_SERVICE_NAME_CANADA, {PICK_CHEMICALS}, CANADA_REWARD),

            build_complex_breakable_service(MASK_CREATION1_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #build_complex_breakable_service(MASK_CREATION2_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PHOTOLITOGRAPHY1_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(PHOTOLITOGRAPHY2_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(ION_IMPLANTATION1_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(ION_IMPLANTATION2_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(TESTING1_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(TESTING2_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(TESTING_QUALITY1_SERVICE_NAME, TESTING_QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(QUALITY1_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(QUALITY2_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(DICING1_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(DICING2_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PACKAGING1_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(PACKAGING2_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(THERMAL_PACKAGING1_SERVICE_NAME, THERMAL_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
        ]
    elif mode == "ltlf" and dimension == "small":
        all_services = [
            build_generic_service_one_state(DESIGN_SERVICE_NAME_USA, {PICK_DESIGN}, USA_REWARD),
            #build_generic_service_one_state(DESIGN_SERVICE_NAME_CHINA, {PICK_DESIGN}, CHINA_REWARD),

            build_generic_service_one_state(SILICON_SERVICE_NAME_USA, {PICK_SILICON}, USA_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_BRAZIL, {PICK_SILICON}, BRAZIL_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_CHINA, {PICK_SILICON}, CHINA_REWARD),
        
            build_generic_service_one_state(IMPURITIES_SERVICE_NAME_USA, {PICK_IMPURITIES}, USA_REWARD),
            #build_generic_service_one_state(IMPURITIES_SERVICE_NAME_CHILE, {PICK_IMPURITIES}, CHILE_REWARD),

            build_generic_service_one_state(RESIST_SERVICE_NAME_USA, {PICK_RESIST}, USA_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_CANADA, {PICK_RESIST}, CANADA_REWARD),

            build_generic_service_one_state(CHEMICALS_SERVICE_NAME_USA, {PICK_CHEMICALS}, USA_REWARD),
            #build_generic_service_one_state(CHEMICALS_SERVICE_NAME_CANADA, {PICK_CHEMICALS}, CANADA_REWARD),

            build_complex_breakable_service(MASK_CREATION1_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #build_complex_breakable_service(MASK_CREATION2_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PHOTOLITOGRAPHY1_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(ION_IMPLANTATION1_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(TESTING1_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(TESTING_QUALITY1_SERVICE_NAME, TESTING_QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(QUALITY1_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(DICING1_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #build_complex_breakable_service(DICING2_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PACKAGING1_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(THERMAL_PACKAGING1_SERVICE_NAME, THERMAL_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
        ]
    elif mode == "ltlf" and dimension == "medium":
        all_services = [
            build_generic_service_one_state(DESIGN_SERVICE_NAME_USA, {PICK_DESIGN}, USA_REWARD),
            build_generic_service_one_state(DESIGN_SERVICE_NAME_CHINA, {PICK_DESIGN}, CHINA_REWARD),
            #build_generic_service_one_state(DESIGN_SERVICE_NAME_UK, {PICK_DESIGN}, UK_REWARD),
        
            build_generic_service_one_state(SILICON_SERVICE_NAME_USA, {PICK_SILICON}, USA_REWARD),
            build_generic_service_one_state(SILICON_SERVICE_NAME_BRAZIL, {PICK_SILICON}, BRAZIL_REWARD),
            build_generic_service_one_state(SILICON_SERVICE_NAME_CHINA, {PICK_SILICON}, CHINA_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_RUSSIA, {PICK_SILICON}, RUSSIA_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_NORWAY, {PICK_SILICON}, NORWAY_REWARD),
        
            build_generic_service_one_state(IMPURITIES_SERVICE_NAME_USA, {PICK_IMPURITIES}, USA_REWARD),
            build_generic_service_one_state(IMPURITIES_SERVICE_NAME_CHILE, {PICK_IMPURITIES}, CHILE_REWARD),
            #build_generic_service_one_state(IMPURITIES_SERVICE_NAME_BRAZIL, {PICK_IMPURITIES}, BRAZIL_REWARD),

            build_generic_service_one_state(RESIST_SERVICE_NAME_USA, {PICK_RESIST}, USA_REWARD),
            build_generic_service_one_state(RESIST_SERVICE_NAME_CANADA, {PICK_RESIST}, CANADA_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_INDIA, {PICK_RESIST}, INDIA_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_SWITZERLAND, {PICK_RESIST}, SWITZERLAND_REWARD),
        
            build_generic_service_one_state(CHEMICALS_SERVICE_NAME_USA, {PICK_CHEMICALS}, USA_REWARD),
            build_generic_service_one_state(CHEMICALS_SERVICE_NAME_CANADA, {PICK_CHEMICALS}, CANADA_REWARD),

            build_complex_breakable_service(MASK_CREATION1_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #build_complex_breakable_service(MASK_CREATION2_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PHOTOLITOGRAPHY1_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(PHOTOLITOGRAPHY2_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(ION_IMPLANTATION1_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(ION_IMPLANTATION2_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(TESTING1_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(TESTING_QUALITY1_SERVICE_NAME, TESTING_QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(QUALITY1_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(DICING1_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(DICING2_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PACKAGING1_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(THERMAL_PACKAGING1_SERVICE_NAME, THERMAL_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
        ]
    elif mode == "ltlf" and dimension == "large":
        all_services = [
            build_generic_service_one_state(DESIGN_SERVICE_NAME_USA, {PICK_DESIGN}, USA_REWARD),
            build_generic_service_one_state(DESIGN_SERVICE_NAME_UK, {PICK_DESIGN}, UK_REWARD),
            build_generic_service_one_state(DESIGN_SERVICE_NAME_CHINA, {PICK_DESIGN}, CHINA_REWARD),
            #build_generic_service_one_state(DESIGN_SERVICE_NAME_TAIWAN, {PICK_DESIGN}, TAIWAN_REWARD),

            build_generic_service_one_state(SILICON_SERVICE_NAME_BRAZIL, {PICK_SILICON}, BRAZIL_REWARD),
            build_generic_service_one_state(SILICON_SERVICE_NAME_CHINA, {PICK_SILICON}, CHINA_REWARD),
            build_generic_service_one_state(SILICON_SERVICE_NAME_RUSSIA, {PICK_SILICON}, RUSSIA_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_NORWAY, {PICK_SILICON}, NORWAY_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_USA, {PICK_SILICON}, USA_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_FRANCE, {PICK_SILICON}, FRANCE_REWARD),
            #build_generic_service_one_state(SILICON_SERVICE_NAME_MALAYSIA, {PICK_SILICON}, MALAYSIA_REWARD),

            build_generic_service_one_state(IMPURITIES_SERVICE_NAME_USA, {PICK_IMPURITIES}, USA_REWARD),
            build_generic_service_one_state(IMPURITIES_SERVICE_NAME_CHILE, {PICK_IMPURITIES}, CHILE_REWARD),
            #build_generic_service_one_state(IMPURITIES_SERVICE_NAME_CHINA, {PICK_IMPURITIES}, CHINA_REWARD),
            #build_generic_service_one_state(IMPURITIES_SERVICE_NAME_BRAZIL, {PICK_IMPURITIES}, BRAZIL_REWARD),

            build_generic_service_one_state(RESIST_SERVICE_NAME_USA, {PICK_RESIST}, USA_REWARD),
            build_generic_service_one_state(RESIST_SERVICE_NAME_BELGIUM, {PICK_RESIST}, BELGIUM_REWARD),
            build_generic_service_one_state(RESIST_SERVICE_NAME_AUSTRIA, {PICK_RESIST}, AUSTRIA_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_INDIA, {PICK_RESIST}, INDIA_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_SWITZERLAND, {PICK_RESIST}, SWITZERLAND_REWARD),
            #build_generic_service_one_state(RESIST_SERVICE_NAME_CANADA, {PICK_RESIST}, CANADA_REWARD),

            build_generic_service_one_state(CHEMICALS_SERVICE_NAME_USA, {PICK_CHEMICALS}, USA_REWARD),
            build_generic_service_one_state(CHEMICALS_SERVICE_NAME_CANADA, {PICK_CHEMICALS}, CANADA_REWARD),

            build_complex_breakable_service(MASK_CREATION1_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            #build_complex_breakable_service(MASK_CREATION2_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PHOTOLITOGRAPHY1_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(PHOTOLITOGRAPHY2_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(ION_IMPLANTATION1_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(ION_IMPLANTATION2_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(TESTING1_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(TESTING2_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(TESTING_QUALITY1_SERVICE_NAME, TESTING_QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(QUALITY1_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(QUALITY2_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(DICING1_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(DICING2_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PACKAGING1_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_generic_breakable_service(PACKAGING2_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(THERMAL_PACKAGING1_SERVICE_NAME, THERMAL_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD)
        ]
    return all_services



def target_service_automata():
    '''Builds the target service automaton for the given dimension of the problem.'''
    # we need to distinguished the different dimensions because of the service setup (different services models for different dimensions)
    transition_function = {
        "s0": {PICK_DESIGN: ("s5", 1.0, 0), },
        "s5": {f"con_{MASK_CREATION}": ("s6", 1.0, 0), },
        "s6": {f"che_{MASK_CREATION}": ("s7", 1.0, 0), },
        # "s7": {MASK_CREATION: ("s8", 1.0, 0), },
        "s7": {MASK_CREATION: ("s0", 1.0, 0), },
        #
        # "s8": {PHOTOLITOGRAPHY: ("s9", 1.0, 0), },
        # "s9": {f"ch_{PHOTOLITOGRAPHY}": ("s10", 1.0, 0), },
        #
        # "s10": {ION_IMPLANTATION: ("s11", 1.0, 0), },
        # "s11": {f"ch_{ION_IMPLANTATION}": ("s12", 1.0, 0), },
        #
        # "s12": {TESTING: ("s13", 1.0, 0), },
        # "s13": {f"ch_{TESTING}": ("s14", 1.0, 0), },
        #
        # "s14": {f"con_{DICING}": ("s15", 1.0, 0), },
        # "s15": {f"che_{DICING}": ("s16", 1.0, 0), },
        # "s16": {DICING: ("s17", 1.0, 0), },
        #
        # "s17": {CLASSIC_PACKAGING: ("s18", 1.0, 0), },
        # "s18": {f"ch_{CLASSIC_PACKAGING}": ("s0", 1.0, 0), }
    }

    initial_state = "s0"
    final_states = {"s0"}

    return build_target_from_transitions(
        transition_function, initial_state, final_states
    )


ALL_SYMBOLS = [
    PICK_DESIGN,
    PICK_SILICON,
    PICK_IMPURITIES,
    PICK_RESIST,
    PICK_CHEMICALS,
    MASK_CREATION,
    PHOTOLITOGRAPHY,
    ION_IMPLANTATION,
    TESTING,
    TESTING_QUALITY,
    QUALITY,
    DICING,
    CLASSIC_PACKAGING,
    THERMAL_PACKAGING
]

ALL_SYMBOLS_SET = set(ALL_SYMBOLS)


# declare process specification
declare_constraints = [
    exactly_once(PICK_DESIGN),
    exactly_once(PICK_SILICON),
    exactly_once(PICK_IMPURITIES),
    exactly_once(PICK_RESIST),
    exactly_once(PICK_CHEMICALS),
    exactly_once(MASK_CREATION),
    exactly_once(PHOTOLITOGRAPHY),
    exactly_once(ION_IMPLANTATION),
    exactly_once(DICING),
    
    absence_2(TESTING),
    absence_2(TESTING_QUALITY),
    absence_2(QUALITY),
    absence_2(THERMAL_PACKAGING),
    absence_2(CLASSIC_PACKAGING),
    
    alt_succession(PICK_DESIGN, MASK_CREATION),
    alt_succession(PICK_SILICON, MASK_CREATION),
    alt_succession(PICK_IMPURITIES, MASK_CREATION),
    alt_succession(PICK_RESIST, MASK_CREATION),
    alt_succession(PICK_CHEMICALS, MASK_CREATION),
    
    alt_succession(MASK_CREATION, PHOTOLITOGRAPHY),
    alt_succession(PHOTOLITOGRAPHY, ION_IMPLANTATION),
    
    alt_precedence(ION_IMPLANTATION, TESTING),
    alt_precedence(ION_IMPLANTATION, TESTING_QUALITY),

    alt_succession(TESTING_QUALITY, QUALITY),
    
    alt_response(TESTING, DICING),
    alt_response(QUALITY, DICING),
    precedence_or(TESTING, QUALITY, DICING),
    
    alt_precedence(DICING, CLASSIC_PACKAGING),
    alt_precedence(DICING, THERMAL_PACKAGING),
    
    not_coexistence(TESTING, TESTING_QUALITY),
    not_coexistence(CLASSIC_PACKAGING, THERMAL_PACKAGING),
    
    build_declare_assumption(ALL_SYMBOLS_SET)
]


def target_service_ltlf():
    '''Builds the target service LTLf formula from the DECLARE constraints and symbols.'''
    declare_constraints.append(build_declare_assumption(ALL_SYMBOLS_SET))
    formula_str = " & ".join(map(lambda s: f"({s})", declare_constraints))
    formula = pylogics.parsers.parse_ltl(formula_str)
    automaton = logaut.core.ltl2dfa(formula, backend="lydia")
    declare_automaton = from_symbolic_automaton_to_declare_automaton(automaton, ALL_SYMBOLS_SET)
    return declare_automaton

    

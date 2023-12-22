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
ETCHING = "et"
DEPOSITION = "dep"
ION_IMPLANTATION = "ion_i"
PROCESSING = "proc"

TESTING = "tes"
TESTING_GRAPHICS = "tes_gr"
QUALITY = "qual"
QUALITY_GRAPHICS = "qual_gr"

DICING = "dic"

CLASSIC_PACKAGING = "pac"  
THERMAL_PACKAGING = "pac_t"     #for cooling of GPU

ALL_SYMBOLS = [
    PICK_DESIGN,
    PICK_SILICON,
    PICK_IMPURITIES,
    PICK_RESIST,
    PICK_CHEMICALS,
    MASK_CREATION,
    PHOTOLITOGRAPHY,
    ETCHING,
    DEPOSITION,
    ION_IMPLANTATION,
    PROCESSING,
    TESTING,
    TESTING_GRAPHICS,
    QUALITY,
    QUALITY_GRAPHICS,
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
    exactly_once(ETCHING),
    exactly_once(DEPOSITION),
    exactly_once(ION_IMPLANTATION),
    exactly_once(PROCESSING),
    exactly_once(DICING),
    
    absence_2(TESTING),
    absence_2(TESTING_GRAPHICS),
    absence_2(QUALITY),
    absence_2(QUALITY_GRAPHICS),
    absence_2(THERMAL_PACKAGING),
    absence_2(CLASSIC_PACKAGING),
    
    alt_succession(PICK_DESIGN, MASK_CREATION),
    alt_succession(PICK_SILICON, MASK_CREATION),
    alt_succession(PICK_IMPURITIES, MASK_CREATION),
    alt_succession(PICK_RESIST, MASK_CREATION),
    alt_succession(PICK_CHEMICALS, MASK_CREATION),
    
    alt_succession(MASK_CREATION, PHOTOLITOGRAPHY),
    alt_succession(PHOTOLITOGRAPHY, ETCHING),
    alt_succession(ETCHING, DEPOSITION),
    alt_succession(DEPOSITION, ION_IMPLANTATION),
    alt_succession(ION_IMPLANTATION, PROCESSING),
    
    alt_precedence(PROCESSING, TESTING),
    alt_precedence(PROCESSING, TESTING_GRAPHICS),
    
    alt_succession(TESTING, QUALITY),
    alt_succession(TESTING_GRAPHICS, QUALITY_GRAPHICS),
    
    alt_response(QUALITY, DICING),
    alt_response(QUALITY_GRAPHICS, DICING),
    precedence_or(QUALITY, QUALITY_GRAPHICS, DICING),
    
    alt_precedence(DICING, CLASSIC_PACKAGING),
    alt_precedence(DICING, THERMAL_PACKAGING),
    
    not_coexistence(TESTING, TESTING_GRAPHICS),
    not_coexistence(QUALITY, QUALITY_GRAPHICS),
    not_coexistence(CLASSIC_PACKAGING, THERMAL_PACKAGING),
    
    build_declare_assumption(ALL_SYMBOLS_SET)
]


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
MASK_CREATION2_SERVICE_NAME = "cr_m_2"  # small, medium, large

PHOTOLITOGRAPHY1_SERVICE_NAME = "ph_l_1"
PHOTOLITOGRAPHY2_SERVICE_NAME = "ph_l_2"  # large

ETCHING1_SERVICE_NAME = "et_m_1"
ETCHING2_SERVICE_NAME = "et_m_2"   # large

DEPOSITION1_SERVICE_NAME = "dep_m_1"
DEPOSITION2_SERVICE_NAME = "dep_m_2"   # large

ION_IMPLANTATION1_SERVICE_NAME = "ion_i_m_1"
ION_IMPLANTATION2_SERVICE_NAME = "ion_i_m_2"   # large

PROCESSING1_SERVICE_NAME = "proc_m_1"
PROCESSING2_SERVICE_NAME = "proc_m_2"   # medium, large

TESTING1_SERVICE_NAME = "tes_m_1"
TESTING2_SERVICE_NAME = "tes_m_2"   # medium, large

TESTING_GRAPHICS1_SERVICE_NAME = "tes_gr_m_1"
TESTING_GRAPHICS2_SERVICE_NAME = "tes_gr_m_2"   # large

QUALITY1_SERVICE_NAME = "qual_m_1"
QUALITY2_SERVICE_NAME = "qual_m_2"  # medium, large

QUALITY_GRAPHICS1_SERVICE_NAME = "qual_gr_m_1"
QUALITY_GRAPHICS2_SERVICE_NAME = "qual_gr_m_2"  # large

DICING1_SERVICE_NAME = "dic_m_1"
DICING2_SERVICE_NAME = "dic_m_2"    # small, medium, large

PACKAGING1_SERVICE_NAME = "pac_m_1"
PACKAGING2_SERVICE_NAME = "pac_m_2"  # large

THERMAL_PACKAGING1_SERVICE_NAME = "pac_t_m_1"
THERMAL_PACKAGING2_SERVICE_NAME = "pac_t_m_2"  # large


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
    return build_service_from_transitions(transitions, initial_state, final_states)  # type: ignore


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
    return build_service_from_transitions(transitions, initial_state, final_states)  # type: ignore


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
    return build_service_from_transitions(transitions, initial_state, final_states)  # type: ignore


def process_services(dimension):
    '''Builds all the services for the given dimension of the problem.'''
    all_services = [
        build_generic_service_one_state(DESIGN_SERVICE_NAME_USA, {PICK_DESIGN}, USA_REWARD),
        build_generic_service_one_state(DESIGN_SERVICE_NAME_UK, {PICK_DESIGN}, UK_REWARD),
        build_generic_service_one_state(DESIGN_SERVICE_NAME_CHINA, {PICK_DESIGN}, CHINA_REWARD),
        build_generic_service_one_state(DESIGN_SERVICE_NAME_TAIWAN, {PICK_DESIGN}, TAIWAN_REWARD),

        build_generic_service_one_state(SILICON_SERVICE_NAME_BRAZIL, {PICK_SILICON}, BRAZIL_REWARD),
        build_generic_service_one_state(SILICON_SERVICE_NAME_CHINA, {PICK_SILICON}, CHINA_REWARD),
        build_generic_service_one_state(SILICON_SERVICE_NAME_RUSSIA, {PICK_SILICON}, RUSSIA_REWARD),
        build_generic_service_one_state(SILICON_SERVICE_NAME_NORWAY, {PICK_SILICON}, NORWAY_REWARD),
        build_generic_service_one_state(SILICON_SERVICE_NAME_USA, {PICK_SILICON}, USA_REWARD),
        build_generic_service_one_state(SILICON_SERVICE_NAME_FRANCE, {PICK_SILICON}, FRANCE_REWARD),
        build_generic_service_one_state(SILICON_SERVICE_NAME_MALAYSIA, {PICK_SILICON}, MALAYSIA_REWARD),

        build_generic_service_one_state(IMPURITIES_SERVICE_NAME_USA, {PICK_IMPURITIES}, USA_REWARD),
        build_generic_service_one_state(IMPURITIES_SERVICE_NAME_CHILE, {PICK_IMPURITIES}, CHILE_REWARD),
        build_generic_service_one_state(IMPURITIES_SERVICE_NAME_CHINA, {PICK_IMPURITIES}, CHINA_REWARD),
        build_generic_service_one_state(IMPURITIES_SERVICE_NAME_BRAZIL, {PICK_IMPURITIES}, BRAZIL_REWARD),

        build_generic_service_one_state(RESIST_SERVICE_NAME_USA, {PICK_RESIST}, USA_REWARD),
        build_generic_service_one_state(RESIST_SERVICE_NAME_BELGIUM, {PICK_RESIST}, BELGIUM_REWARD),
        build_generic_service_one_state(RESIST_SERVICE_NAME_AUSTRIA, {PICK_RESIST}, AUSTRIA_REWARD),
        build_generic_service_one_state(RESIST_SERVICE_NAME_INDIA, {PICK_RESIST}, INDIA_REWARD),
        build_generic_service_one_state(RESIST_SERVICE_NAME_SWITZERLAND, {PICK_RESIST}, SWITZERLAND_REWARD),
        build_generic_service_one_state(RESIST_SERVICE_NAME_CANADA, {PICK_RESIST}, CANADA_REWARD),

        build_generic_service_one_state(CHEMICALS_SERVICE_NAME_USA, {PICK_CHEMICALS}, USA_REWARD),
        build_generic_service_one_state(CHEMICALS_SERVICE_NAME_CANADA, {PICK_CHEMICALS}, CANADA_REWARD),
    ]
    if dimension == "small":
        other_services = [
            build_complex_breakable_service(MASK_CREATION1_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(MASK_CREATION2_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PHOTOLITOGRAPHY1_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(ETCHING1_SERVICE_NAME, ETCHING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(DEPOSITION1_SERVICE_NAME, DEPOSITION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(ION_IMPLANTATION1_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(PROCESSING1_SERVICE_NAME, PROCESSING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(TESTING1_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(TESTING_GRAPHICS1_SERVICE_NAME, TESTING_GRAPHICS, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(QUALITY1_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(QUALITY_GRAPHICS1_SERVICE_NAME, QUALITY_GRAPHICS, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(DICING1_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(DICING2_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PACKAGING1_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(THERMAL_PACKAGING1_SERVICE_NAME, THERMAL_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
        ]
    elif dimension == "medium":
        other_services = [
            build_complex_breakable_service(MASK_CREATION1_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(MASK_CREATION2_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PHOTOLITOGRAPHY1_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(ETCHING1_SERVICE_NAME, ETCHING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(DEPOSITION1_SERVICE_NAME, DEPOSITION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(ION_IMPLANTATION1_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(PROCESSING1_SERVICE_NAME, PROCESSING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(PROCESSING2_SERVICE_NAME, PROCESSING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(TESTING1_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(TESTING2_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(TESTING_GRAPHICS1_SERVICE_NAME, TESTING_GRAPHICS, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(QUALITY1_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(QUALITY2_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(QUALITY_GRAPHICS1_SERVICE_NAME, QUALITY_GRAPHICS, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_complex_breakable_service(DICING1_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(DICING2_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_generic_breakable_service(PACKAGING1_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),

            build_generic_breakable_service(THERMAL_PACKAGING1_SERVICE_NAME, THERMAL_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
        ]
    elif dimension == "large":
        other_services = [
            build_complex_breakable_service(MASK_CREATION1_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(MASK_CREATION2_SERVICE_NAME, MASK_CREATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(PHOTOLITOGRAPHY1_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(PHOTOLITOGRAPHY2_SERVICE_NAME, PHOTOLITOGRAPHY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(ETCHING1_SERVICE_NAME, ETCHING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(ETCHING2_SERVICE_NAME, ETCHING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(DEPOSITION1_SERVICE_NAME, DEPOSITION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(DEPOSITION2_SERVICE_NAME, DEPOSITION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(ION_IMPLANTATION1_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(ION_IMPLANTATION2_SERVICE_NAME, ION_IMPLANTATION, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(PROCESSING1_SERVICE_NAME, PROCESSING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(PROCESSING2_SERVICE_NAME, PROCESSING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(TESTING1_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(TESTING2_SERVICE_NAME, TESTING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(TESTING_GRAPHICS1_SERVICE_NAME, TESTING_GRAPHICS, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(TESTING_GRAPHICS2_SERVICE_NAME, TESTING_GRAPHICS, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(QUALITY1_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(QUALITY2_SERVICE_NAME, QUALITY, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(QUALITY_GRAPHICS1_SERVICE_NAME, QUALITY_GRAPHICS, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(QUALITY_GRAPHICS2_SERVICE_NAME, QUALITY_GRAPHICS, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(DICING1_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(DICING2_SERVICE_NAME, DICING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(PACKAGING1_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(PACKAGING2_SERVICE_NAME, CLASSIC_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),

            build_complex_breakable_service(THERMAL_PACKAGING1_SERVICE_NAME, THERMAL_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, DEFAULT_USA_REWARD),
            build_complex_breakable_service(THERMAL_PACKAGING2_SERVICE_NAME, THERMAL_PACKAGING, DEFAULT_BROKEN_PROB, DEFAULT_UNEMPLOYABLE_PROB, DEFAULT_BROKEN_REWARD, HIGH_USA_REWARD),
        ]
    res_services = all_services + other_services
    return res_services


def target_service_automata(dimension):
    '''Builds the target service automaton for the given dimension of the problem.'''
    # we need to distinguished the different dimensions because of the service setup (different services models for different dimensions)
    if dimension == "small":
        transition_function = {
            "s0": {PICK_DESIGN: ("s1", 1.0, 0), },
            "s1": {PICK_SILICON: ("s2", 1.0, 0), },
            "s2": {PICK_IMPURITIES: ("s3", 1.0, 0), },
            "s3": {PICK_RESIST: ("s4", 1.0, 0), },
            "s4": {PICK_CHEMICALS: ("s5", 1.0, 0), },

            "s5": {f"con_{MASK_CREATION}": ("s6", 1.0, 0), },
            "s6": {f"che_{MASK_CREATION}": ("s7", 1.0, 0), },
            "s7": {MASK_CREATION: ("s8", 1.0, 0), },
            
            "s8": {PHOTOLITOGRAPHY: ("s9", 1.0, 0), },
            "s9": {f"ch_{PHOTOLITOGRAPHY}": ("s10", 1.0, 0), },
            
            "s10": {ETCHING: ("s11", 1.0, 0), },
            "s11": {f"ch_{ETCHING}": ("s12", 1.0, 0), },
            
            "s12": {DEPOSITION: ("s13", 1.0, 0), },
            "s13": {f"ch_{DEPOSITION}": ("s14", 1.0, 0), },
            
            "s14": {ION_IMPLANTATION: ("s15", 1.0, 0), },
            "s15": {f"ch_{ION_IMPLANTATION}": ("s16", 1.0, 0), },
            
            "s16": {PROCESSING: ("s17", 1.0, 0), },
            "s17": {f"ch_{PROCESSING}": ("s18", 1.0, 0), },
            
            "s18": {TESTING: ("s19", 1.0, 0), },
            "s19": {f"ch_{TESTING}": ("s20", 1.0, 0), },
            
            "s20": {QUALITY: ("s21", 1.0, 0), },
            "s21": {f"ch_{QUALITY}": ("s22", 1.0, 0), },
            
            "s22": {f"con_{DICING}": ("s23", 1.0, 0), },
            "s23": {f"che_{DICING}": ("s24", 1.0, 0), },
            "s24": {DICING: ("s25", 1.0, 0), },
            
            "s25": {CLASSIC_PACKAGING: ("s26", 1.0, 0), }
        }
    elif dimension == "medium":
        transition_function = {
            "s0": {PICK_DESIGN: ("s1", 1.0, 0), },
            "s1": {PICK_SILICON: ("s2", 1.0, 0), },
            "s2": {PICK_IMPURITIES: ("s3", 1.0, 0), },
            "s3": {PICK_RESIST: ("s4", 1.0, 0), },
            "s4": {PICK_CHEMICALS: ("s5", 1.0, 0), },

            "s5": {f"con_{MASK_CREATION}": ("s6", 1.0, 0), },
            "s6": {f"ch_{MASK_CREATION}": ("s7", 1.0, 0), },
            "s7": {MASK_CREATION: ("s8", 1.0, 0), },
            
            "s8": {PHOTOLITOGRAPHY: ("s9", 1.0, 0), },
            "s9": {f"ch_{PHOTOLITOGRAPHY}": ("s10", 1.0, 0), },
            
            "s10": {ETCHING: ("s11", 1.0, 0), },
            "s11": {f"ch_{ETCHING}": ("s12", 1.0, 0), },
            
            "s12": {DEPOSITION: ("s13", 1.0, 0), },
            "s13": {f"ch_{DEPOSITION}": ("s14", 1.0, 0), },
            
            "s14": {ION_IMPLANTATION: ("s15", 1.0, 0), },
            "s15": {f"ch_{ION_IMPLANTATION}": ("s16", 1.0, 0), },
            
            "s16": {f"con_{PROCESSING}": ("s17", 1.0, 0), },
            "s17": {f"ch_{PROCESSING}": ("s18", 1.0, 0), },
            "s18": {PROCESSING: ("s19", 1.0, 0), },
            
            "s19": {f"con_{TESTING}": ("s20", 1.0, 0), },
            "s20": {f"ch_{TESTING}": ("s21", 1.0, 0), },
            "s21": {TESTING: ("s22", 1.0, 0), },
            
            "s22": {f"con_{QUALITY}": ("s23", 1.0, 0), },
            "s23": {f"ch_{QUALITY}": ("s24", 1.0, 0), },
            "s24": {QUALITY: ("s25", 1.0, 0), },
            
            "s25": {f"con_{DICING}": ("s26", 1.0, 0), },
            "s26": {f"ch_{DICING}": ("s27", 1.0, 0), },
            "s27": {DICING: ("s28", 1.0, 0), },
            
            "s29": {CLASSIC_PACKAGING: ("s30", 1.0, 0), }
        }
    elif dimension == "large":
        transition_function = {
            "s0": {PICK_DESIGN: ("s1", 1.0, 0), },
            "s1": {PICK_SILICON: ("s2", 1.0, 0), },
            "s2": {PICK_IMPURITIES: ("s3", 1.0, 0), },
            "s3": {PICK_RESIST: ("s4", 1.0, 0), },
            "s4": {PICK_CHEMICALS: ("s5", 1.0, 0), },
            
            "s5": {f"con_{MASK_CREATION}": ("s6", 1.0, 0), },
            "s6": {f"ch_{MASK_CREATION}": ("s7", 1.0, 0), },
            "s7": {MASK_CREATION: ("s8", 1.0, 0), },
            
            "s8": {f"con_{PHOTOLITOGRAPHY}": ("s9", 1.0, 0), },
            "s9": {f"ch_{PHOTOLITOGRAPHY}": ("s10", 1.0, 0), },
            "s10": {PHOTOLITOGRAPHY: ("s11", 1.0, 0), },
            
            "s11": {f"con_{ETCHING}": ("s12", 1.0, 0), },
            "s12": {f"ch_{ETCHING}": ("s13", 1.0, 0), },
            "s13": {ETCHING: ("s14", 1.0, 0), },
            
            "s14": {f"con_{DEPOSITION}": ("s15", 1.0, 0), },
            "s15": {f"ch_{DEPOSITION}": ("s16", 1.0, 0), },
            "s16": {DEPOSITION: ("s17", 1.0, 0), },
            
            "s17": {f"con_{ION_IMPLANTATION}": ("s18", 1.0, 0), },
            "s18": {f"ch_{ION_IMPLANTATION}": ("s19", 1.0, 0), },
            "s19": {ION_IMPLANTATION: ("s20", 1.0, 0), },
            
            "s20": {f"con_{PROCESSING}": ("s21", 1.0, 0), },
            "s21": {f"ch_{PROCESSING}": ("s22", 1.0, 0), },
            "s22": {PROCESSING: ("s23", 1.0, 0), },
            
            "s23": {f"con_{TESTING}": ("s24", 1.0, 0), },
            "s24": {f"ch_{TESTING}": ("s25", 1.0, 0), },
            "s25": {TESTING: ("s26", 1.0, 0), },
            
            "s26": {f"con_{QUALITY}": ("s27", 1.0, 0), },
            "s27": {f"ch_{QUALITY}": ("s28", 1.0, 0), },
            "s28": {QUALITY: ("s29", 1.0, 0), },
            
            "s29": {f"con_{DICING}": ("s30", 1.0, 0), },
            "s30": {f"ch_{DICING}": ("s31", 1.0, 0), },
            "s31": {DICING: ("s32", 1.0, 0), },
            
            "s23": {f"con_{CLASSIC_PACKAGING}": ("s24", 1.0, 0), },
            "s24": {f"ch_{CLASSIC_PACKAGING}": ("s25", 1.0, 0), },
            "s25": {CLASSIC_PACKAGING: ("s26", 1.0, 0), }
        }

    initial_state = "s0"
    final_states = {"s0"}

    return build_target_from_transitions(
        transition_function, initial_state, final_states
    )


def target_service_ltlf():
    '''Builds the target service LTLf formula from the DECLARE constraints and symbols.'''
    declare_constraints.append(build_declare_assumption(ALL_SYMBOLS_SET))
    formula_str = " & ".join(map(lambda s: f"({s})", declare_constraints))
    formula = pylogics.parsers.parse_ltl(formula_str)
    automaton = logaut.core.ltl2dfa(formula, backend="lydia")
    declare_automaton = from_symbolic_automaton_to_declare_automaton(automaton, ALL_SYMBOLS_SET)
    return declare_automaton

    

import tensorflow as tf
import math
import itertools
import State
import PolicyState
import Definitions
import Parameters

# Extract parameters
varrho, varsigma = Parameters.varrho, Parameters.varsigma

# --------------------------------------------------------------------------- #
# Deterministic case
# --------------------------------------------------------------------------- #

# Probability of a dummy shock
shock_probs = tf.constant([1.0])  # Dummy probability


def augment_state(state):
    """ Transform the zetax state by taking its exponential """
    _state = state
    _state = State.update(_state, 'zetax', tf.math.exp(State.zetax(state)))
    return _state


def total_step_random(prev_state, policy_state):
    """ State dependant random shock to evaluate the expectation operator """
    _ar = AR_step(prev_state)
    _shock = shock_step_random(prev_state)
    _policy = policy_step(prev_state, policy_state)

    _total_random = _ar + _shock + _policy

    return augment_state(_total_random)


def total_step_spec_shock(prev_state, policy_state, shock_index):
    """ State specific shock to run one episode """
    _ar = AR_step(prev_state)
    _shock = shock_step_spec_shock(prev_state, shock_index)
    _policy = policy_step(prev_state, policy_state)

    _total_spec = _ar + _shock + _policy

    return augment_state(_total_spec)


def AR_step(prev_state):
    """ AR(1) shock on zetax and chix """
    _ar_step = tf.zeros_like(prev_state)  # Initialization
    _ar_step = State.update(
        _ar_step, 'zetax',
        tf.math.log(State.zetax(prev_state)) + State.chix(prev_state))
    _ar_step = State.update(
        _ar_step, 'chix', Parameters.r * State.chix(prev_state))
    return _ar_step


def shock_step_random(prev_state):
    """ TFP shock zeta and chi """
    _shock_step = tf.zeros_like(prev_state)  # Initialization

    return _shock_step


def shock_step_spec_shock(prev_state, shock_index):
    """ TFP shock zeta and chi """
    _shock_step = tf.zeros_like(prev_state)  # Initialization

    return _shock_step


def policy_step(prev_state, policy_state):
    """ State variables are updated by the optimal policy (capital stock) or
    the laws of motion for carbon masses and temperatures """
    _policy_step = tf.zeros_like(prev_state)  # Initialization

    # Update state variables if needed
    _policy_step = State.update(
        _policy_step, 'kx', PolicyState.kplusy(policy_state))
    _policy_step = State.update(
        _policy_step, 'MATx', Definitions.MATplus(prev_state, policy_state))
    _policy_step = State.update(
        _policy_step, 'MUOx', Definitions.MUOplus(prev_state, policy_state))
    _policy_step = State.update(
        _policy_step, 'MLOx', Definitions.MLOplus(prev_state, policy_state))
    _policy_step = State.update(
        _policy_step, 'TATx', Definitions.TATplus(prev_state, policy_state))
    _policy_step = State.update(
        _policy_step, 'TOCx', Definitions.TOCplus(prev_state, policy_state))
    _policy_step = State.update(
        _policy_step, 'taux', Definitions.tau2tauplus(prev_state, policy_state)
    )

    return _policy_step

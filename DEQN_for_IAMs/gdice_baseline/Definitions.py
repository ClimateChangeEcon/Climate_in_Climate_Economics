import tensorflow as tf
import numpy as np
import Parameters
import PolicyState
import State

#--------------------------------------------------------------------------- #
# Extract parameters
# --------------------------------------------------------------------------- #
# Dice specific parameter
Tstep = Parameters.Tstep
Version = Parameters.Version
# Logarithmic time transformation
vartheta = Parameters.vartheta
# Economic parameters
rho = Parameters.rho
alpha, delta, psi = Parameters.alpha, Parameters.delta, Parameters.psi
# Population
L0, Linfty, deltaL = Parameters.L0, Parameters.Linfty, Parameters.deltaL
# TFP
A0hat, gA0hat, deltaA = Parameters.A0hat, Parameters.gA0hat, Parameters.deltaA
# Carbon intensity
sigma0, gSigma0, deltaSigma = Parameters.sigma0, Parameters.gSigma0, \
                                Parameters.deltaSigma
# Mitigation
theta2, pback, gback = Parameters.theta2, Parameters.pback, Parameters.gback
# Land emissions
ELand0, deltaLand = Parameters.ELand0, Parameters.deltaLand
# Exogenous forcings
fex0, fex1, Tyears = Parameters.fex0, Parameters.fex1, Parameters.Tyears
# Climate damage function
pi1, pi2, pow1, pow2 = Parameters.pi1, Parameters.pi2, Parameters.pow1, Parameters.pow2
# Carbon mass transitions
phi12_, phi23_, MATeq, MUOeq, MLOeq = Parameters.phi12_, Parameters.phi23_, \
    Parameters.MATeq, Parameters.MUOeq, Parameters.MLOeq
# Temperature exchange
varphi1_, varphi3_, varphi4_  = Parameters.varphi1_, Parameters.varphi3_, \
    Parameters.varphi4_
f2xco2, t2xco2 =  Parameters.f2xco2, Parameters.t2xco2
# Preindustrial carbon concentration
MATbase = Parameters.MATbase

# --------------------------------------------------------------------------- #
# Real and computational time periods
# --------------------------------------------------------------------------- #
def tau2t(state, policy_state):
    """ Scale back from the computational time tau to the real time t """
    _t = - tf.math.log(1 - State.taux(state)) / vartheta
    return _t


def tau2tauplus(state, policy_state):
    """ Update the computational time tau by tau + 1 based on the current real
    time t """
    _t = tau2t(state, policy_state)  # Current real time
    _tplus = _t + tf.ones_like(_t)  # Real time t + 1
    _tauplus = 1 - tf.math.exp(- vartheta * _tplus)  # Computational time tau+1
    return _tauplus

# --------------------------------------------------------------------------- #
# Exogenous parameters
# --------------------------------------------------------------------------- #
def tfp(state, policy_state):
    """ Deterministic TFP shock on the labor-argumented production function [-]
    """
    _t = tau2t(state, policy_state)
    if (Version == '2016') or (Version == '2007'):
        _adj_coef = Parameters.adj_coef
        _tfp = A0hat * tf.math.exp((Tstep * gA0hat * _adj_coef) * (1 -
                tf.math.exp(-Tstep * deltaA * _t)) / (Tstep * deltaA))
    elif (Version == 'cjl'):
        _tfp = A0hat * tf.math.exp((Tstep * gA0hat) * (1 -
                tf.math.exp(-Tstep*deltaA * _t)) / (Tstep * deltaA))
    return _tfp


def gr_tfp(state, policy_state):
    """ Annual growth rate of the deterministic TFP shock [-/year] """
    _t = tau2t(state, policy_state)
    if (Version == '2016') or (Version == '2007'):
        _adj_coef = Parameters.adj_coef
        _gr_tfp = (Tstep * gA0hat * _adj_coef) * tf.math.exp(-Tstep * deltaA * _t)
    elif (Version == 'cjl'):
        _gr_tfp = (Tstep * gA0hat) * tf.math.exp(-Tstep * deltaA * _t)
    return _gr_tfp


def lab(state, policy_state):
    """ World population [million] """
    _t = tau2t(state, policy_state)
    _lab = L0 + (Linfty - L0) * (1 - tf.math.exp(-Tstep * deltaL * _t))
    return _lab


def gr_lab(state, policy_state):
    """ Annual growth rate of the world population [-/year] """
    _t = tau2t(state, policy_state)
    _gr_lab = (Tstep * deltaL) / ((Linfty / (Linfty-L0)) * tf.math.exp(
                Tstep * deltaL * _t) - 1)
    return _gr_lab


def sigma(state, policy_state):
    """ Carbon intensity """
    _t = tau2t(state, policy_state)
    if (Version == 'cjl') or (Version == '2007'):
        _sigma = sigma0 * tf.math.exp(
            (Tstep * gSigma0) * (1 - tf.math.exp(-Tstep * deltaSigma *_t)) / (
                Tstep * deltaSigma))
    elif (Version == '2016'):
        _sigma = sigma0 * tf.math.exp(Tstep * gSigma0 / np.log(1 + Tstep * deltaSigma)*
                    ((1 + Tstep * deltaSigma)**_t - 1))
    return _sigma


def theta1(state, policy_state):
    """ Cost coefficient of carbon mitigation """
    _t = tau2t(state, policy_state)
    _sigma = sigma(state, policy_state)
    if (Version == 'cjl') or (Version == '2007'):
        _theta1 = pback * (1000 *_sigma) * (1 + tf.math.exp(-Tstep * gback * _t)) \
        / theta2
    elif (Version == '2016'):
        c2co2 = Parameters.c2co2
        _theta1 = pback * (1000 * c2co2 *_sigma) * (tf.math.exp(-Tstep * gback * _t)) \
        / theta2
    return _theta1


def Eland(state, policy_state):
    """ Natural carbon emission """
    _t = tau2t(state, policy_state)
    _Eland = ELand0 * tf.math.exp(-Tstep * deltaLand * _t)
    return _Eland


def Fex(state, policy_state):
    """ External radiative forcing """
    _t = tau2t(state, policy_state)
    Year = np.int(Tyears / Tstep)
    _Fex = fex0 + (1 / Year) * (fex1 - fex0) * tf.math.minimum(_t, Year)
    return _Fex


def beta_hat(state, policy_state):
    """ Effective discout factor """
    _gr_tfp = gr_tfp(state, policy_state)
    _gr_lab = gr_lab(state, policy_state)
    _beta_hat = tf.math.exp(- rho * Tstep + (1-1/psi) * _gr_tfp + _gr_lab)
    return _beta_hat

def phi12(state, policy_state):
    """ Mass of carbon transmission"""
    return Tstep * phi12_

def phi23(state, policy_state):
    """ Mass of carbon transmission"""
    return Tstep * phi23_

def phi21(state, policy_state):
    """ Mass of carbon transmission"""
    if (Version == 'cjl'):
        return np.round(MATeq/MUOeq * Tstep * phi12_, 2)
    elif (Version == '2016') or (Version == '2007'):
        return MATeq/MUOeq * phi12_* Tstep

def phi32(state, policy_state):
    """ Mass of carbon transmission"""
    if (Version == 'cjl'):
        return np.round(MUOeq/MLOeq * Tstep * phi23_, 5)
    elif (Version == '2016') or (Version == '2007'):
        return MUOeq/MLOeq * phi23_* Tstep

def varphi21(state, policy_state):
    if (Version == 'cjl'):
        return np.round(Tstep * varphi1_ * varphi3_, 4)
    elif (Version == '2016') or (Version == '2007'):
        return Tstep * varphi1_ * varphi3_

def varphi4(state, policy_state):
    return Tstep * varphi4_

def varphi1(state, policy_state):
    return Tstep * varphi1_

def xi2(state, policy_state):
    if (Version == 'cjl'):
        return np.round(Tstep*varphi1_ * f2xco2 / t2xco2, 3)
    elif (Version == '2016') or (Version == '2007'):
        return Tstep * varphi1_ * f2xco2 / t2xco2

# --------------------------------------------------------------------------- #
# Economic variables
# --------------------------------------------------------------------------- #
def con(state, policy_state):
    """ Consumption policy """
    _lambd_haty = PolicyState.lambd_haty(policy_state)
    _con = _lambd_haty**(-psi)
    return _con


def Omega(state, policy_state):
    """ Climate damage function """
    _TAT = State.TATx(state)
    if (Version == 'cjl') or (Version == '2007'):
        _Omega = 1 / (1 + pi1 * _TAT**pow1 + pi2 * _TAT**pow2)
    elif (Version == '2016'):
        _Omega = pi1 * _TAT**pow1 + pi2 * _TAT**pow2
    return _Omega

def Omega_prime(state, policy_state):
    """ The first derivative of the climate damage function """
    _TAT = State.TATx(state)
    if (Version == 'cjl') or (Version == '2007'):
        _Omega_prime = - (pow1*pi1*_TAT**(pow1-1) + pow2 * pi2 * _TAT**(pow2-1)) / (
                    1 + pi1 * _TAT**pow1 + pi2 * _TAT**pow2)**2
    elif (Version == '2016'):
        _Omega_prime = pow1 * pi1 * _TAT**(pow1-1) + pow2 * pi2 * _TAT**(pow2-1)
    return _Omega_prime

def ygross(state, policy_state):
    """ Gross production in effective labor units """
    _kx = State.kx(state)  # Capital stock today
    _zetax = State.zetax(state)  # TFP shock
    _ygross = _zetax * _kx**alpha
    return _ygross

def ynet(state, policy_state):
    """ Net production, where the climate damage is deducted, in effective
    labor units """
    if (Version == 'cjl') or (Version == '2007'):
        _ynet = Omega(state, policy_state) * ygross(state, policy_state)
    elif (Version == '2016'):
        _ynet = (1 - Omega(state, policy_state)) * ygross(state, policy_state)
    return _ynet

def Dam(state, policy_state):
    """ Damages """
    if (Version == 'cjl') or (Version == '2007'):
        _dam =  (1 - Omega(state, policy_state)) * ygross(state, policy_state)
    elif (Version == '2016'):
        _dam =  Omega(state, policy_state) * ygross(state, policy_state)
    return _dam

def inv(state, policy_state):
    """ Investment """
    _con = con(state, policy_state)
    _ynet = ynet(state, policy_state)
    _inv = _ynet  - _con
    return _inv


def Eind(state, policy_state):
    """ Industrial CO2 emission [1000 GtC] """
    _sigma = sigma(state, policy_state)
    _tfp = tfp(state, policy_state)
    _lab = lab(state, policy_state)
    _ygross = ygross(state, policy_state)
    _Eind =  _sigma * _ygross
    return _Eind

def Emissions(state, policy_state):
    """ Industrial CO2 emission [1000 GtC] """
    _tfp = tfp(state, policy_state)
    _lab = lab(state, policy_state)
    _Eind = Eind(state, policy_state) * _tfp * _lab
    _Eland = Eland(state, policy_state)
    return _Eind + _Eland


def scc(state, policy_state):
    _lambd_haty = PolicyState.lambd_haty(policy_state)
    _Omega = Omega(state, policy_state)
    _nuAT_haty = PolicyState.nuAT_haty(policy_state)
    _zetax = State.zetax(state)
    _kx = State.kx(state)
    _sigma = sigma(state, policy_state)
    _tfp = tfp(state, policy_state)
    _lab = lab(state, policy_state)
    _phi12 = phi12(state, policy_state)
    _nuUO_haty = PolicyState.nuUO_haty(policy_state)
    _etaAT_haty = PolicyState.etaAT_haty(policy_state)
    _varphi1 = varphi1(state, policy_state)
    _MATx = State.MATx(state)
    if (Version == 'cjl') or (Version == '2007'):
        _dvdk =  (_lambd_haty * (Tstep  * _Omega * alpha * _kx**(alpha-1)
                               + (1 - delta)**Tstep)
                    + (-_nuAT_haty) *  Tstep * _sigma * _zetax * _tfp * _lab * alpha
                    * _kx**(alpha-1))
    elif (Version == '2016'):
        _dvdk =  (_lambd_haty * (Tstep * (1  - _Omega) * alpha * _kx**(alpha-1)
                               + (1 - delta)**Tstep)
                    + (-_nuAT_haty) * Tstep * _sigma * _zetax * _tfp * _lab * alpha
                    * _kx**(alpha-1))

    _dvdMAT =  ((-_nuAT_haty) * (1 - _phi12) + _nuUO_haty * _phi12
                + _etaAT_haty * _varphi1 * f2xco2 / (tf.math.log(2.) * _MATx))
    _scc = - _dvdMAT / _dvdk * _tfp * _lab
    return _scc

# --------------------------------------------------------------------------- #
# State variables in period t+1
# --------------------------------------------------------------------------- #
def MATplus(state, policy_state):
    """ Carbon mass in the atmosphere """
    _tfp = tfp(state, policy_state)
    _lab = lab(state, policy_state)
    _sigma = sigma(state, policy_state)
    _Eland = Eland(state, policy_state)
    _kx = State.kx(state)
    _zetax = State.zetax(state)
    _MATx = State.MATx(state)
    _MUOx = State.MUOx(state)
    _phi21 = phi21(state, policy_state)
    _phi12 = phi12(state, policy_state)
    _MATplus = (1-_phi12) * _MATx + _phi21 * _MUOx \
        + Tstep* _sigma * _tfp * _lab * _zetax * _kx**alpha + Tstep*_Eland
    return _MATplus


def MUOplus(state, policy_state):
    """ Carbon mass in the upper ocean """
    _MATx = State.MATx(state)
    _MUOx = State.MUOx(state)
    _MLOx = State.MLOx(state)
    _phi21 = phi21(state, policy_state)
    _phi32 = phi32(state, policy_state)
    _phi12 = phi12(state, policy_state)
    _phi23 = phi23(state, policy_state)
    _MUOplus = _phi12 * _MATx + (1 - _phi21 - _phi23) * _MUOx + _phi32 * _MLOx
    return _MUOplus


def MLOplus(state, policy_state):
    """ Carbon mass in the lower ocean """
    _MUOx = State.MUOx(state)
    _MLOx = State.MLOx(state)
    _phi32 = phi32(state, policy_state)
    _phi23 = phi23(state, policy_state)
    _MLOplus = _phi23 * _MUOx + (1 - _phi32) * _MLOx
    return _MLOplus


def TATplus(state, policy_state):
    """ Atmosphere temperature change relative to the preindustrial """
    _Fex = Fex(state, policy_state)
    _TATx = State.TATx(state)
    _TOCx = State.TOCx(state)
    _MATx = State.MATx(state)
    _varphi21 = varphi21(state, policy_state)
    _varphi1 = varphi1(state, policy_state)
    _xi2 = xi2(state, policy_state)
    _TATplus = (1 - _varphi21 - _xi2) * _TATx + _varphi21 * _TOCx \
        + _varphi1 * (f2xco2 * (tf.math.log(_MATx / MATbase) / tf.math.log(2.))
                 + _Fex)
    return _TATplus


def TOCplus(state, policy_state):
    """ Ocean temperature change relative to the preindustrial """
    _TATx = State.TATx(state)
    _TOCx = State.TOCx(state)
    _varphi4 = varphi4(state, policy_state)
    _TOCplus = _varphi4 * _TATx + (1 - _varphi4) * _TOCx
    return _TOCplus

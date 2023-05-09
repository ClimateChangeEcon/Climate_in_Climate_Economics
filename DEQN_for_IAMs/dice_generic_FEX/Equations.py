import tensorflow as tf
import Definitions
import PolicyState
import Parameters
import State


def equations(state, policy_state):
    """ The dictionary of loss functions """
    # Expectation operator
    E_t = State.E_t_gen(state, policy_state)

    # ----------------------------------------------------------------------- #
    # Parameters
    # ----------------------------------------------------------------------- #
    Tstep = Parameters.Tstep
    Version = Parameters.Version
    # Economic and climate parameters
    delta, alpha, psi = Parameters.delta, Parameters.alpha, Parameters.psi
    phi12 = Definitions.phi12(state, policy_state)
    phi23 = Definitions.phi23(state, policy_state)
    phi21 = Definitions.phi21(state, policy_state)
    phi32 = Definitions.phi32(state, policy_state)
    varphi21 = Definitions.varphi21(state, policy_state)
    varphi4 = Definitions.varphi4(state, policy_state)
    xi2 = Definitions.xi2(state, policy_state)
    varphi1 = Definitions.varphi1(state, policy_state)
    f2xco2, MATbase = Parameters.f2xco2, Parameters.MATbase
    theta2 = Parameters.theta2

    # Exogenously evolved parameters
    tfp = Definitions.tfp(state, policy_state)
    gr_tfp = Definitions.gr_tfp(state, policy_state)
    lab = Definitions.lab(state, policy_state)
    gr_lab = Definitions.gr_lab(state, policy_state)
    sigma = Definitions.sigma(state, policy_state)
    Eland = Definitions.Eland(state, policy_state)
    # Fex = Definitions.Fex(state, policy_state)
    theta1 = Definitions.theta1(state, policy_state)
    beta_hat = Definitions.beta_hat(state, policy_state)

    # ----------------------------------------------------------------------- #
    # State variables
    # ----------------------------------------------------------------------- #
    # Retlieve the current state
    kx = State.kx(state)
    MATx, MUOx, MLOx = State.MATx(state), State.MUOx(state), State.MLOx(state)
    TATx, TOCx = State.TATx(state), State.TOCx(state)
    zetax, chix = State.zetax(state), State.chix(state)

    # States in period t+1
    MATplus = Definitions.MATplus(state, policy_state)
    MUOplus = Definitions.MUOplus(state, policy_state)
    MLOplus = Definitions.MLOplus(state, policy_state)
    TATplus = Definitions.TATplus(state, policy_state)
    TOCplus = Definitions.TOCplus(state, policy_state)

    # ----------------------------------------------------------------------- #
    # Pptimal policy functions in period t
    # ----------------------------------------------------------------------- #
    kplusy = PolicyState.kplusy(policy_state)
    muy = PolicyState.muy(policy_state)
    lambd_haty = PolicyState.lambd_haty(policy_state)
    nuAT_haty = PolicyState.nuAT_haty(policy_state)
    nuUO_haty = PolicyState.nuUO_haty(policy_state)
    nuLO_haty = PolicyState.nuLO_haty(policy_state)
    etaAT_haty = PolicyState.etaAT_haty(policy_state)
    etaOC_haty = PolicyState.etaOC_haty(policy_state)

    # ----------------------------------------------------------------------- #
    # Defined economic variables in period t
    # ----------------------------------------------------------------------- #
    con = Definitions.con(state, policy_state)
    Omega = Definitions.Omega(state, policy_state)
    Theta = Definitions.Theta(state, policy_state)
    Theta_prime = Definitions.Theta_prime(state, policy_state)

    # ----------------------------------------------------------------------- #
    # Loss functions
    # ----------------------------------------------------------------------- #
    loss_dict = {}

    if (Version == 'cjl') or (Version == '2007'):
        # ----------------------------------------------------------------------- #
        # FOC wrt. kplus for cjl and dice2007
        # ----------------------------------------------------------------------- #
        loss_dict['foc_kplus'] = tf.math.exp(Tstep*(gr_tfp + gr_lab)) * lambd_haty \
            - beta_hat * E_t(
                lambda s, ps:
                PolicyState.lambd_haty(ps) * (
                    Tstep*(1 - Definitions.Theta(s, ps)) * Definitions.Omega(s, ps)
                    * State.zetax(s) * alpha * kplusy**(alpha - 1)
                    + (1 - delta)**Tstep)
                + (-PolicyState.nuAT_haty(ps)) * (1 - PolicyState.muy(ps))
                * Tstep*Definitions.sigma(s, ps) * Definitions.tfp(s, ps)
                * Definitions.lab(s, ps)
                * State.zetax(s) * alpha * kplusy**(alpha - 1)
            )
        # ----------------------------------------------------------------------- #
        # FOC wrt. lambd_haty (budget constraint) for cjl and dice2007
        # ----------------------------------------------------------------------- #
        budget = Tstep*(1 - Theta)* Omega * zetax * kx**alpha - Tstep * con \
            + (1 - delta)**Tstep * kx - tf.math.exp(Tstep*(gr_tfp + gr_lab)) * kplusy
        loss_dict['foc_lambd'] = budget
        # ----------------------------------------------------------------------- #
        # KKT wrt. mu with the Fischer-Burmeister function for cjl and dice2007
        # ----------------------------------------------------------------------- #
        lambdMU_hat = - lambd_haty * Tstep * Theta_prime * Omega  * zetax * kx**alpha \
            - (-nuAT_haty) * Tstep * sigma * tfp * lab * zetax * kx**alpha
        # Fischer-Burmeister function = a + b - sqrt(a**2 + b**2)
        loss_dict['kkt_mu_fb'] = lambdMU_hat + (1 - muy) - tf.math.sqrt(
            lambdMU_hat**2 + (1 - muy)**2)
        # ----------------------------------------------------------------------- #
        # FOC wrt. TATplus for cjl and dice2007
        # ----------------------------------------------------------------------- #
        loss_dict['foc_TATplus'] = etaAT_haty - beta_hat * E_t(
            lambda s, ps:
            PolicyState.lambd_haty(ps)
            * (Tstep * (1 - Theta) * Definitions.Omega_prime(s, ps)) * State.zetax(s)
            * kplusy**alpha + PolicyState.etaAT_haty(ps) * (1 - varphi21 - xi2)
            + PolicyState.etaOC_haty(ps) * varphi4
            )
    else:
        # ----------------------------------------------------------------------- #
        # FOC wrt. kplus for dice 2016
        # ----------------------------------------------------------------------- #
        loss_dict['foc_kplus'] = tf.math.exp(Tstep*(gr_tfp + gr_lab)) * lambd_haty \
            - beta_hat * E_t(
                lambda s, ps:
                PolicyState.lambd_haty(ps) * (
                    Tstep*(1 - Definitions.Theta(s, ps)- Definitions.Omega(s, ps))
                    * State.zetax(s) * alpha * kplusy**(alpha - 1)
                    + (1 - delta)**Tstep)
                + (-PolicyState.nuAT_haty(ps)) * (1 - PolicyState.muy(ps))
                * Tstep*Definitions.sigma(s, ps) * Definitions.tfp(s, ps)
                * Definitions.lab(s, ps)
                * State.zetax(s) * alpha * kplusy**(alpha - 1)
            )
        # ----------------------------------------------------------------------- #
        # FOC wrt. lambd_haty (budget constraint) for dice 2016
        # ----------------------------------------------------------------------- #
        budget = Tstep*(1 - Theta - Omega) * zetax * kx**alpha - Tstep*con \
            + (1 - delta)**Tstep * kx - tf.math.exp(Tstep*(gr_tfp + gr_lab)) * kplusy
        loss_dict['foc_lambd'] = budget
        # ----------------------------------------------------------------------- #
        # KKT wrt. mu with the Fischer-Burmeister function for dice 2016
        # ----------------------------------------------------------------------- #
        lambdMU_hat = - lambd_haty * Tstep*Theta_prime  * zetax * kx**alpha \
            - (-nuAT_haty) * Tstep * sigma * tfp * lab * zetax * kx**alpha
        # Fischer-Burmeister function = a + b - sqrt(a**2 + b**2)
        loss_dict['kkt_mu_fb'] = lambdMU_hat + (1 - muy) - tf.math.sqrt(
            lambdMU_hat**2 + (1 - muy)**2)
        # ----------------------------------------------------------------------- #
        # FOC wrt. TATplus for dice 2016
        # ----------------------------------------------------------------------- #
        loss_dict['foc_TATplus'] = etaAT_haty - beta_hat * E_t(
            lambda s, ps:
            PolicyState.lambd_haty(ps)
            * (-Tstep * Definitions.Omega_prime(s, ps)) * State.zetax(s) * kplusy**alpha
            + PolicyState.etaAT_haty(ps) * (1 - varphi21 - xi2)
            + PolicyState.etaOC_haty(ps) * varphi4
        )

    # ----------------------------------------------------------------------- #
    # FOC wrt. MATplus
    # ----------------------------------------------------------------------- #
    loss_dict['foc_MATplus'] = (-nuAT_haty) - beta_hat * E_t(
        lambda s, ps:
        (-PolicyState.nuAT_haty(ps)) * (1 - phi12)
        + PolicyState.nuUO_haty(ps) * phi12
        + PolicyState.etaAT_haty(ps) * varphi1 * f2xco2 * (1 / (
            tf.math.log(2.) * MATplus))
    )

    # ----------------------------------------------------------------------- #
    # FOC wrt. MUOplus
    # ----------------------------------------------------------------------- #
    loss_dict['foc_MUOplus'] = nuUO_haty - beta_hat * E_t(
        lambda s, ps:
        (-PolicyState.nuAT_haty(ps)) * phi21
        + PolicyState.nuUO_haty(ps) * (1 - phi21 - phi23)
        + PolicyState.nuLO_haty(ps) * phi23
    )

    # ----------------------------------------------------------------------- #
    # FOC wrt. MLOplus
    # ----------------------------------------------------------------------- #
    loss_dict['foc_MLOplus'] = nuLO_haty - beta_hat * E_t(
        lambda s, ps:
        PolicyState.nuUO_haty(ps) * phi32
        + PolicyState.nuLO_haty(ps) * (1 - phi32)
    )


    # ----------------------------------------------------------------------- #
    # FOC wrt. TOCplus
    # ----------------------------------------------------------------------- #
    loss_dict['foc_TOCplus'] = etaOC_haty - beta_hat * E_t(
        lambda s, ps:
        PolicyState.etaAT_haty(ps) * varphi21
        + PolicyState.etaOC_haty(ps) * (1 - varphi4)
    )

    return loss_dict

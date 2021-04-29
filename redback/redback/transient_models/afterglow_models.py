import numpy as np

from .. import model_library
from .. constants import *

from astropy.cosmology import Planck15 as cosmo
from scipy.integrate import simps
from .. utils import logger, calc_ABmag_from_fluxdensity

try:
    import afterglowpy as afterglow

    # keep so you can eventually generalise
    jettype_dict = {'tophat': afterglow.jet.TopHat, 'gaussian': afterglow.jet.Gaussian,
                    'powerlaw_w_core': afterglow.jet.PowerLawCore, 'gaussian_w_core': afterglow.jet.GaussianCore,
                    'cocoon': afterglow.Spherical, 'smooth_power_law': afterglow.jet.PowerLaw,
                    'cone': afterglow.jet.Cone}
    spectype_dict = {'no_inverse_compton': 0, 'inverse_compton': 1}

except ModuleNotFoundError as e:
    logger.warning(e)

def cocoon(time, redshift, umax, umin, logEi, k, mej, logn0, p, logepse, logepsb, ksin, g0, **kwargs):
    dl = cosmo.luminosity_distance(redshift).cgs.value
    spread = kwargs['spread']
    latres = kwargs['latres']
    tres = kwargs['tres']
    jettype = jettype_dict['cocoon']
    spectype = kwargs['spectype']
    frequency = kwargs['frequency']
    e0 = 10**logEi
    n0 = 10**logn0
    epse = 10**logepse
    epsb = 10**logepsb
    Z = {'jetType': jettype, 'specType': spectype, 'uMax': umax, 'Er': e0,
         'uMin': umin, 'k': k, 'MFast_solar': mej, 'n0': n0, 'p': p, 'epsilon_e': epse, 'epsilon_B': epsb,
         'xi_N': ksin, 'd_L': dl, 'z': redshift, 'L0': 0, 'q': 0, 'ts': 0, 'g0': g0,
         'spread': spread, 'latRes': latres, 'tRes': tres}
    fluxdensity = afterglow.fluxDensity(time, frequency, **Z)
    return fluxdensity

def kn_afterglow(time, redshift, umax, umin, logEi, k, mej, logn0, p, logepse, logepsb, ksin, g0, **kwargs):
    dl = cosmo.luminosity_distance(redshift).cgs.value
    spread = kwargs['spread']
    latres = kwargs['latres']
    tres = kwargs['tres']
    jettype = jettype_dict['cocoon']
    spectype =kwargs['spectype']
    frequency = kwargs['frequency']
    e0 = 10**logEi
    n0 = 10**logn0
    epse = 10**logepse
    epsb = 10**logepsb
    Z = {'jetType': jettype, 'specType': spectype, 'uMax': umax, 'Er': e0,
         'uMin': umin, 'k':k, 'MFast_solar':mej,'n0': n0, 'p': p, 'epsilon_e': epse, 'epsilon_B': epsb,
         'xi_N': ksin, 'd_L': dl, 'z': redshift, 'L0': 0, 'q': 0, 'ts': 0, 'g0': g0,
         'spread': spread, 'latRes': latres, 'tRes': tres}
    fluxdensity = afterglow.fluxDensity(time, frequency, **Z)
    return fluxdensity

def cone_afterglow(time, redshift, thv, loge0, thw, thc, logn0, p, logepse, logepsb, ksin, g0, **kwargs):
    dl = cosmo.luminosity_distance(redshift).cgs.value
    spread = kwargs['spread']
    latres = kwargs['latres']
    tres = kwargs['tres']
    jettype = jettype_dict['cone']
    spectype = kwargs['spectype']
    frequency = kwargs['frequency']
    thw = thw * thc
    e0 = 10 ** loge0
    n0 = 10 ** logn0
    epse = 10 ** logepse
    epsb = 10 ** logepsb
    Z = {'jetType': jettype, 'specType': spectype,'thetaObs': thv, 'E0': e0,
         'thetaCore': thc, 'n0': n0,'p': p,'epsilon_e': epse,'epsilon_B': epsb,
         'xi_N': ksin,'d_L': dl, 'z': redshift, 'L0':0,'q':0,'ts':0, 'g0':g0,
         'spread':spread, 'latRes':latres, 'tRes':tres, 'thetaWing':thw}
    fluxdensity = afterglow.fluxDensity(time, frequency, **Z)
    return fluxdensity

def gaussiancore(time, redshift, thv,loge0,thc,thw,logn0,p,logepse,logepsb,ksin,g0,**kwargs):
    dl = cosmo.luminosity_distance(redshift).cgs.value
    spread = kwargs['spread']
    latres = kwargs['latres']
    tres = kwargs['tres']
    jettype = jettype_dict['gaussian_w_core']
    spectype = kwargs['spectype']
    frequency = kwargs['frequency']

    thw = thw * thc
    e0 = 10 ** loge0
    n0 = 10 ** logn0
    epse = 10 ** logepse
    epsb = 10 ** logepsb
    Z = {'jetType': jettype, 'specType': spectype,'thetaObs': thv, 'E0': e0,
         'thetaCore': thc, 'n0': n0,'p': p,'epsilon_e': epse,'epsilon_B': epsb,
         'xi_N': ksin,'d_L': dl, 'z': redshift, 'L0':0,'q':0,'ts':0, 'g0':g0,
         'spread':spread, 'latRes':latres, 'tRes':tres, 'thetaWing':thw}
    fluxdensity = afterglow.fluxDensity(time, frequency, **Z)
    return fluxdensity

def gaussian(time, redshift, thv, loge0, thw, thc, logn0, p, logepse, logepsb, ksin, g0, **kwargs):
    dl = cosmo.luminosity_distance(redshift).cgs.value
    spread = kwargs['spread']
    latres = kwargs['latres']
    tres = kwargs['tres']
    jettype = jettype_dict['gaussian']
    spectype = kwargs['spectype']
    frequency = kwargs['frequency']
    thw = thw * thc
    e0 = 10 ** loge0
    n0 = 10 ** logn0
    epse = 10 ** logepse
    epsb = 10 ** logepsb
    Z = {'jetType': jettype, 'specType': spectype,'thetaObs': thv, 'E0': e0,
         'thetaCore': thc, 'n0': n0,'p': p,'epsilon_e': epse,'epsilon_B': epsb,
         'xi_N': ksin,'d_L': dl, 'z': redshift, 'L0':0,'q':0,'ts':0, 'g0':g0,
         'spread':spread, 'latRes':latres, 'tRes':tres, 'thetaWing':thw}
    fluxdensity = afterglow.fluxDensity(time, frequency, **Z)
    return fluxdensity

def smoothpowerlaw(time, redshift, thv, loge0, thw, thc, beta, logn0, p, logepse, logepsb, ksin, g0, **kwargs):
    dl = cosmo.luminosity_distance(redshift).cgs.value
    spread = kwargs['spread']
    latres = kwargs['latres']
    tres = kwargs['tres']
    jettype = jettype_dict['smooth_power_law']
    spectype = kwargs['spectype']
    frequency = kwargs['frequency']
    thw = thw * thc
    e0 = 10 ** loge0
    n0 = 10 ** logn0
    epse = 10 ** logepse
    epsb = 10 ** logepsb
    Z = {'jetType': jettype, 'specType': spectype,'thetaObs': thv, 'E0': e0,
         'thetaCore': thc, 'n0': n0,'p': p,'epsilon_e': epse,'epsilon_B': epsb,
         'xi_N': ksin,'d_L': dl, 'z': redshift, 'L0':0,'q':0,'ts':0, 'g0':g0,
         'spread':spread, 'latRes':latres, 'tRes':tres, 'thetaWing':thw, 'b':beta}
    fluxdensity = afterglow.fluxDensity(time, frequency, **Z)
    return fluxdensity

def powerlawcore(time, redshift, thv, loge0, thw, thc, beta, logn0, p, logepse, logepsb, ksin, g0, **kwargs):
    dl = cosmo.luminosity_distance(redshift).cgs.value
    spread = kwargs['spread']
    latres = kwargs['latres']
    tres = kwargs['tres']
    jettype = jettype_dict['powerlaw_w_core']
    spectype = kwargs['spectype']
    frequency = kwargs['frequency']
    thw = thw * thc
    e0 = 10 ** loge0
    n0 = 10 ** logn0
    epse = 10 ** logepse
    epsb = 10 ** logepsb
    Z = {'jetType': jettype, 'specType': spectype,'thetaObs': thv, 'E0': e0,
         'thetaCore': thc, 'n0': n0,'p': p,'epsilon_e': epse,'epsilon_B': epsb,
         'xi_N': ksin,'d_L': dl, 'z': redshift, 'L0':0,'q':0,'ts':0, 'g0':g0,
         'spread':spread, 'latRes':latres, 'tRes':tres, 'thetaWing':thw, 'b':beta}
    fluxdensity = afterglow.fluxDensity(time, frequency, **Z)
    return fluxdensity

def tophat(time, redshift, thv, loge0, thc, logn0, p, logepse, logepsb, ksin, g0, **kwargs):
    dl = cosmo.luminosity_distance(redshift).cgs.value
    spread = kwargs['spread']
    latres = kwargs['latres']
    tres = kwargs['tres']
    jettype = jettype_dict['tophat']
    spectype = kwargs['spectype']
    frequency = kwargs['frequency']

    e0 = 10 ** loge0
    n0 = 10 ** logn0
    epse = 10 ** logepse
    epsb = 10 ** logepsb
    Z = {'jetType': jettype, 'specType': spectype, 'thetaObs': thv, 'E0': e0,
         'thetaCore': thc, 'n0': n0, 'p': p, 'epsilon_e': epse, 'epsilon_B': epsb,
         'xi_N': ksin, 'd_L': dl, 'z': redshift, 'L0': 0, 'q': 0, 'ts': 0, 'g0': g0,
         'spread': spread, 'latRes': latres, 'tRes': tres}
    fluxdensity = afterglow.fluxDensity(time, frequency, **Z)
    return fluxdensity

def tophat_integrated(time, redshift, thv, loge0, thc, logn0, p, logepse, logepsb, ksin, g0, **kwargs):
    dl = cosmo.luminosity_distance(redshift).cgs.value
    spread = kwargs['spread']
    latres = kwargs['latres']
    tres = kwargs['tres']
    jettype = jettype_dict['tophat']
    spectype = kwargs['spectype']

    #eventually need this to be smart enough to figure the bounds based on data used
    frequency_bounds = kwargs['frequency'] #should be 2 numbers that serve as start and end point
    e0 = 10 ** loge0
    n0 = 10 ** logn0
    epse = 10 ** logepse
    epsb = 10 ** logepsb
    Z = {'jetType': jettype, 'specType': spectype,'thetaObs': thv, 'E0': e0,
         'thetaCore': thc, 'n0': n0,'p': p,'epsilon_e': epse,'epsilon_B': epsb,
         'xi_N': ksin,'d_L': dl, 'z': redshift, 'L0':0,'q':0,'ts':0, 'g0':g0,
         'spread':spread, 'latRes':latres, 'tRes':tres}

    nu_1d = np.linspace(frequency_bounds[0], frequency_bounds[1], 3)
    t, nu = np.meshgrid(time, nu_1d)  # meshgrid makes 2D t and n
    t = t.flatten()
    nu = nu.flatten()
    fluxdensity = afterglow.fluxDensity(t, nu, **Z)
    lightcurve_at_nu = fluxdensity.reshape(len(nu_1d), len(time))
    prefactor = 1e-26
    lightcurve_at_nu = prefactor * lightcurve_at_nu
    lightcurve = simps(lightcurve_at_nu, axis=0, x=nu_1d)
    return lightcurve
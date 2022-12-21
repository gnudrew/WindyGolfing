"""Scientist classes, which conduct experiments and such"""

from .probabilities import UniformProbGen, NormalProbGen, LogNormalProbGen
from .geometries import EulerAnglesGeometry, SphericalGeometry, CylindricalGeometry
from .sim import SimTrialRunner
from simulator.models import SimTrial
from commons.wranglers import BlobWrangler
from winds.models import WindSpacetime

import numpy as np
import pandas as pd

class Scientist:
    """ Conducts Monte Carlo experiments, sampling many SimTrials for a given parameter set """
    required_keys_params = [
        'windspacetime_id',
        'num_trials',
        'prob_speed_fn_name',
        'max_initial_speed',
        'prob_speed_center',
        'prob_speed_spread',
        'prob_timing_fn_name',
        'max_wait_time',
        'prob_timing_center',
        'prob_timing_spread',
        'prob_aiming_fn_name',
        'prob_aiming_geometry',
        'prob_aiming_X1_min',
        'prob_aiming_X1_max',
        'prob_aiming_X1_center',
        'prob_aiming_X1_spread',
        'prob_aiming_X2_min',
        'prob_aiming_X2_max',
        'prob_aiming_X2_center',
        'prob_aiming_X2_spread',
        'prob_aiming_X3_min',
        'prob_aiming_X3_max',
        'prob_aiming_X3_center',
        'prob_aiming_X3_spread',
        'timestep',
    ]
    optional_keys_params = [
        'g',
        'm',
        'drag_coef',
    ]
    ProbGens = { # probability function generators, keyed by name
        'Uniform': UniformProbGen,
        'Normal': NormalProbGen,
        'Log-normal': LogNormalProbGen,
    }
    Geometries = { # geometry classes, keyed by name
        'EulerAngles': EulerAnglesGeometry,
        'Spherical': SphericalGeometry,
        'Cylindrical': CylindricalGeometry,
    }
    tee_position = np.array(0,0,10)

    def __init__(self, params):
        """
        Parameters:
        -------
        df_windspacetime: pd.DataFrame
            ...
        params: dict
            ...
            keys must include: [
                'windspacetime_id',
                'num_trials',
                'prob_speed_fn_name',
                'max_initial_speed',
                'prob_speed_center',
                'prob_speed_spread',
                'prob_timing_fn_name',
                'max_wait_time',
                'prob_timing_center',
                'prob_timing_spread',
                'prob_aiming_fn_name',
                'prob_aiming_geometry',
                'prob_aiming_X1_min',
                'prob_aiming_X1_max',
                'prob_aiming_X1_center',
                'prob_aiming_X1_spread',
                'prob_aiming_X2_min',
                'prob_aiming_X2_max',
                'prob_aiming_X2_center',
                'prob_aiming_X2_spread',
                'prob_aiming_X3_min',
                'prob_aiming_X3_max',
                'prob_aiming_X3_center',
                'prob_aiming_X3_spread',
                'timestep',
            ],
            keys can optionally include: [
                'g',
                'm',
                'drag_coef,
            ]
        
        """
        # assign params
        self._check_params(params)
        self.params = params

        # load winds
        self.load_windspacetime(self.params)

        # build probability functions
        self.gen_prob_fns()

        # init Random Number Generator with a seed taken from fresh, unpredictable CPU entropy
        self.rng = np.random.default_rng()

    def _check_params(self, params):
        """Checks that supplied params meet requirements."""
        # check for required and optional params
        if not set(self.required_keys_params).issubset(set(params.keys())):
            raise AssertionError('Required params are missing.')        

    def load_windspacetime(self,):
        id = self.params['windspacetime_id']
        o = WindSpacetime.objects.get(pk=id)
        self.df_windspacetime = BlobWrangler().read_blob(o)
        self.arr_windspacetime = self.df_windspacetime.to_numpy()

    def gen_prob_fns(self,):
        # Probability generator classes
        ProbGenTiming = self.ProbGens[self.params['prob_timing_fn_name']]
        ProbGenAiming = self.ProbGens[self.params['prob_aiming_fn_name']]
        ProbGenSpeed = self.ProbGens[self.params['prob_speed_fn_name']]

        # Instantiate probability generators
        pgtime = ProbGenTiming(
            self.params['max_wait_time'],
            self.params['prob_timing_center'],
            self.params['prob_timing_spread'],
        )
        pgaim1 = ProbGenAiming(
            self.params['prob_aiming_X1_min'],
            self.params['prob_aiming_X1_max'],
            self.params['prob_aiming_X1_center'],
            self.params['prob_aiming_X1_spread'],
        )
        pgaim2 = ProbGenAiming(
            self.params['prob_aiming_X2_min'],
            self.params['prob_aiming_X2_max'],
            self.params['prob_aiming_X2_center'],
            self.params['prob_aiming_X2_spread'],
        )
        pgaim3 = ProbGenAiming(
            self.params['prob_aiming_X3_min'],
            self.params['prob_aiming_X3_max'],
            self.params['prob_aiming_X3_center'],
            self.params['prob_aiming_X3_spread'],
        )
        pgspeed = ProbGenSpeed(
            self.params['max_initial_speed'],
            self.params['prob_speed_center'],
            self.params['prob_speed_spread'],
        )

        # Generate prob functions
        prob_fn_timing = pgtime.generate_fn()
        prob_fn_speed = pgspeed.generate_fn()
        prob_fn_aiming_x1 = pgaim1.generate_fn()
        prob_fn_aiming_x2 = pgaim2.generate_fn()
        prob_fn_aiming_x3 = pgaim3.generate_fn()

        # Generate inversions of prob functions to sample (https://stackoverflow.com/questions/21100716/fast-arbitrary-distribution-random-sampling-inverse-transform-sampling)
        inv_prob_fn_timing = pgtime.generate_inv_fn()
        inv_prob_fn_speed = pgspeed.generate_inv_fn()
        inv_prob_fn_aiming_x1 = pgaim1.generate_inv_fn()
        inv_prob_fn_aiming_x2 = pgaim2.generate_inv_fn()
        inv_prob_fn_aiming_x3 = pgaim3.generate_inv_fn()

        self.prob_fns = {
            'timing': prob_fn_timing,
            'speed': prob_fn_speed,
            'aiming_x1': prob_fn_aiming_x1,
            'aiming_x2': prob_fn_aiming_x2,
            'aiming_x3': prob_fn_aiming_x3,
        }
        self.inv_prob_fns = {
            'timing': inv_prob_fn_timing,
            'speed': inv_prob_fn_speed,
            'aiming_x1': inv_prob_fn_aiming_x1,
            'aiming_x2': inv_prob_fn_aiming_x2,
            'aiming_x3': inv_prob_fn_aiming_x3,
        }

    def run_experiment(self,):
        """
        Run the experiment
        
        Returns:
        -------
        simtrial_ids: list
            list of id's for the sim trials created during this experiment
        """
        timestep = self.params['timestep']
        N = self.params['num_trials']
        
        # do the trials
        simtrial_ids = []
        for n in range(N):
            # choose time
            ipt = self.inv_prob_fns['timing'] # inverted probability timing function
            t_initial = ipt(self.rng.random())
            
            # choose aim
            ## choose abstract coordinates
            ipa_x1 = self.inv_prob_fns['aiming_x1'] # inverted probability timing function
            ipa_x2 = self.inv_prob_fns['aiming_x2']
            ipa_x3 = self.inv_prob_fns['aiming_x3']
            x1 = ipa_x1(self.rng.random())
            x2 = ipa_x2(self.rng.random())
            x3 = ipa_x3(self.rng.random())
            ## convert to unit vector via geometry
            G = self.Geometries[self.params['prob_aiming_geometry']]
            v_hat = G(x1, x2, x3).get_unit_vector()
            
            # choose speed
            ips = self.inv_prob_fns['speed'] # inverted probability timing function
            speed_initial = ips(self.rng.random())

            # set initial velocity
            v_initial = speed_initial*v_hat
            
            # run a trial
            runner = SimTrialRunner(t_initial, self.tee_position, v_initial, self.arr_windspacetime, timestep)
            runner.run()

            # extract runner outputs used to save sim trial
            params = self.params

            # save the sim trial
            id = self.save_trial(params)
            simtrial_ids.append(id)

        return simtrial_ids

    def save_trial(self, params):
        """Store blob and simtrial obj then return simtrial_id"""
        # make dataframe
        df = pd.DataFrame(self.ball_position, columns=['x', 'y', 'z'],)
        # save
        simtrial_id = BlobWrangler().write_blob(df, SimTrial, params)
        return simtrial_id
"""Scientist classes, which conduct experiments and such"""

from .probabilities import UniformProbGen, NormalProbGen, LogNormalProbGen
from .geometries import EulerAnglesGeometry, SphericalGeometry, CylindricalGeometry
from .sim import SimTrialRunner
from simulator.models import SimTrial
from commons.wranglers import BlobWrangler
from commons.utilities import trim_dict, list_model_fields
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
        'min_wait_time',
        'min_initial_speed',
        'g',
        'm',
        'drag_coef',
    ]
    ProbGens = { # probability function generators, keyed by function name
        'Uniform': UniformProbGen,
        'Normal': NormalProbGen,
        'Log-normal': LogNormalProbGen,
    }
    Geometries = { # geometry classes, keyed by geometry name
        'EulerAngles': EulerAnglesGeometry,
        'Spherical': SphericalGeometry,
        'Cylindrical': CylindricalGeometry,
    }
    tee_position = np.array([0,0,10])

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
                'min_wait_time',
                'min_initial_speed',
                'g',
                'm',
                'drag_coef,
            ]
        
        """
        # assign params
        self._check_params(params)
        self.params = params

        # load winds
        self.load_windspacetime()

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
            x_min = self.params.get('min_wait_time'), # optional, o.w. None
            x_max = self.params['max_wait_time'],
            x_center = self.params['prob_timing_center'],
            x_spread = self.params['prob_timing_spread'],
        )
        pgaim1 = ProbGenAiming(
            x_min = self.params['prob_aiming_X1_min'],
            x_max = self.params['prob_aiming_X1_max'],
            x_center = self.params['prob_aiming_X1_center'],
            x_spread = self.params['prob_aiming_X1_spread'],
        )
        pgaim2 = ProbGenAiming(
            x_min = self.params['prob_aiming_X2_min'],
            x_max = self.params['prob_aiming_X2_max'],
            x_center = self.params['prob_aiming_X2_center'],
            x_spread = self.params['prob_aiming_X2_spread'],
        )
        pgaim3 = ProbGenAiming(
            x_min = self.params['prob_aiming_X3_min'],
            x_max = self.params['prob_aiming_X3_max'],
            x_center = self.params['prob_aiming_X3_center'],
            x_spread = self.params['prob_aiming_X3_spread'],
        )
        pgspeed = ProbGenSpeed(
            x_min = self.params.get('min_initial_speed'), # optional, o.w. None
            x_max = self.params['max_initial_speed'],
            x_center = self.params['prob_speed_center'],
            x_spread = self.params['prob_speed_spread'],
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
            self.time_initial = time_initial = ipt(self.rng.random())
            ## convert to nearest timestep
            t_initial = int(np.round(time_initial/timestep)) # t denotes an int
            
            # choose aim
            ## choose abstract coordinates
            ### N.B. third coordinate is used in euler angles but is throwaway in spherical geometry.
            ipa_x1 = self.inv_prob_fns['aiming_x1'] # inverted probability timing function
            ipa_x2 = self.inv_prob_fns['aiming_x2']
            ipa_x3 = self.inv_prob_fns['aiming_x3']
            x1 = ipa_x1(self.rng.random())
            x2 = ipa_x2(self.rng.random())
            x3 = ipa_x3(self.rng.random())
            ## convert to unit vector via geometry
            G = self.Geometries[self.params['prob_aiming_geometry']]
            self.direction_initial = v_hat = G(x1, x2, x3).get_unit_vector()
            
            # choose speed
            ips = self.inv_prob_fns['speed'] # inverted probability timing function
            self.speed_initial = speed_initial = ips(self.rng.random())

            # set initial velocity
            v_initial = speed_initial*v_hat
            
            # run a trial
            runner = SimTrialRunner(t_initial, self.tee_position, v_initial, self.arr_windspacetime, timestep)
            runner.run()

            # extract runner outputs used to save sim trial
            params = self.params

            # save the sim trial
            id = self.save_trial(runner.ball_position, params)
            simtrial_ids.append(id)

        return simtrial_ids

    def save_trial(self, arr_ball_position, params):
        """
        Store blob and simtrial obj then return simtrial_id.

        Parameters:
        -------
        arr_ball_position: np.array
            The ball position trajetory in 3D cartesian coordinates. Expects an np.array with 3 columns and arbitrary number of rows, shape=(T, 3).
        params: dict
            The simulation parameters passed to the scientist
        """
        # make dataframe
        df = pd.DataFrame(arr_ball_position, columns=['x', 'y', 'z'],)
        
        # trim parameters to fit SimTrial model
        params_simtrial = trim_dict(params, list_model_fields(SimTrial))

        # add computed parameters in this trial
        params_simtrial['time_initial'] = self.time_initial
        params_simtrial['direction_initial'] = list(self.direction_initial) # convert np.array to list for save
        params_simtrial['speed_initial'] = self.speed_initial

        # save
        simtrial_id = BlobWrangler().write_blob(df, SimTrial, params_simtrial)
        
        return simtrial_id
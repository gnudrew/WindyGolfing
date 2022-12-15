"""Scientist classes, which conduct experiments and such"""

from .probabilities import NormalProbGen, UniformProbGen, LogNormalProbGen
from .sim import SimTrialRunner
from commons.wranglers import BlobWrangler
from winds.models import WindSpacetime



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
        prob_fn_timing = None
        prob_fn_aiming = None
        prob_fn_speed = None

        self.prob_fns = {
            'timing': prob_fn_timing,
            'aiming': prob_fn_aiming,
            'speed': prob_fn_speed,
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
            t_initial = None
            # choose aim
            ## choose geometry coordinates
            ## convert to unit vector
            # choose speed

            # set initial velocity
            v_initial = None
            
            # run a trial
            runner = SimTrialRunner(t_initial, v_initial, self.arr_windspacetime, timestep)
            id = runner.run()
            simtrial_ids.append(id)
        
        return simtrial_ids
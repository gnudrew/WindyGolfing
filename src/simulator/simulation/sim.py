"""The core algorithm for simulation trials"""

class SimTrialRunner:
    """Takes raw inputs and simulates a single ball trajectory"""
    def __init__(self, t_initial, v_initial, arr_windspacetime, timestep):
        """
        Parameters:
        -------
        t_initial: float
            The initial time of the sim, when the ball is hit
        v_initial: np.array
            The initial velocity vector of the ball
        arr_windspacetime: np.array
            The wind velocity data
        timestep: float
            The time between each row of wind speeds, and between simulation compute steps
        """
        self.t_initial = t_initial
        self.v_initial = v_initial
        self.arr_windspacetime = arr_windspacetime
        self.timestep = timestep

    def run(self,):
        # iterate till ball hits ground
        ball_hit_ground = False
        while not ball_hit_ground:
            pass

        # store the trajectory data and return simtrial id
        simtrial_id = self.store_trial()
        return simtrial_id

    def store_trial(self,):
        """Store blob and simtrial obj and return simtrial_id"""
        simtrial_id = None
        return simtrial_id
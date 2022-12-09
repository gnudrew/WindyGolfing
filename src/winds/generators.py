"""The mathematical models used to generate Wind spacetimes"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

WIND_GENERATOR_NAMES = [
    ('windless', 'windless'), # tuples for: (actual value, human-readable name)
    ('constant', 'constant'),
    ('oscillatory', 'oscillatory'),
    ('lorenz', 'lorenz'),
]

class Generator:
    """Base Generator class"""
    def plotx(self,):
        x = self.wind_speeds[:,0]
        t = self.dt * np.arange(len(x))
        plt.plot(t, x)
        plt.show()

    def ploty(self,):
        y = self.wind_speeds[:,1]
        t = self.dt * np.arange(len(y))
        plt.plot(t, y)
        plt.show()

    def plotz(self,):
        z = self.wind_speeds[:,2]
        t = self.dt * np.arange(len(z))
        plt.plot(t, z)
        plt.show()

    def plot3d(self,):
        """show a 3D parametric plot of (vx, vy, vz) over t"""
        # setup x,y,z
        x = self.wind_speeds[:,0]
        y = self.wind_speeds[:,1]
        z = self.wind_speeds[:,2]
        # do plot
        ax = plt.figure().add_subplot(projection='3d')
        ax.plot(x,y,z)
        plt.show()
    
    def to_df(self,):
        """After self.gen, run this to convert dataset to pd.DataFrame"""
        return pd.DataFrame({
            'x': self.wind_speeds[:,0],
            'y': self.wind_speeds[:,1],
            'z': self.wind_speeds[:,2],
            },
            index=self.dt*np.array(range(self.wind_speeds.shape[0])),
        )

class OscillatoryGenerator(Generator):
    default_params = {
        'base_speed': np.array([1,1,1]), # m/s
        'amplitude': np.array([1,1,1]),
        'frequency': np.array([1,1.1,1.2]),
        'phase_shift': np.array([0,0,0]),
        'dt': .001,
    }

    def __init__(self, params=None):
        if params is None:
            params = self.default_params
        self.base_speed = params['base_speed']
        self.amplitude = params['amplitude']
        self.frequency = params['frequency']
        self.phase_shift = params['phase_shift']
        self.dt = params['dt']

    def v(self, t):
        """Calculate velocity vector at a given time, t"""
        return self.base_speed + self.amplitude * np.cos( 2*np.pi * self.frequency * t + self.phase_shift )

    def gen(self, duration):
        """Given a duration in seconds, generate the wind speed trajectory, both returning and assigning it to self.wind_speeds"""
        N = int(duration/self.dt)
        ws = np.empty((N+1,3))
        # initialie
        ws[0,:] = self.base_speed
        # iterate
        for i in range(1,N+1):
            t = self.dt*i
            ws[i,:] = self.v(t)
        self.wind_speeds = ws
        return ws


class LorenzGenerator(Generator):
    default_params = {
        'base_speed': np.array([1.0,1.0,1.0]), # m/s
        'rho': 28,
        'sigma': 10,
        'beta': 8/3,
        'dt': .001, # s
    }

    def __init__(self, params=None):
        if params is None:
            params = self.default_params
        # unpack params
        self.base_speed = params['base_speed']
        self.rho = params['rho']
        self.sigma = params['sigma']
        self.beta = params['beta']
        self.dt = params['dt'] # timestep resolution

    def dx(self, x, y, z):
        f = self.sigma*(y - x)
        return f*self.dt
    def dy(self, x, y, z):
        f = (x*(self.rho - z) - y)
        return f*self.dt
    def dz(self, x, y, z):
        f = (x*y - self.beta*z)
        return f*self.dt
    def dv(self, v):
        """v = (x, y, z)"""
        return self.dx(*v), self.dy(*v), self.dz(*v)

    def gen(self, duration):
        """Given a duration in seconds, generate the wind speed trajectory, both returning and assigning it to self.wind_speeds"""
        N = int(duration / self.dt)
        ws = np.empty((N+1,3)) # wind speeds (x, y, z)
        # initialie
        ws[0,:] = self.base_speed
        # iterate
        for t in range(1,N+1):
            prev_v = ws[t-1,:]
            ws[t,:] = prev_v + self.dv(prev_v)
        self.wind_speeds = ws
        return ws


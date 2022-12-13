"""Probability function generators used by SimTrialRunner"""

class ProbGen:
    """Base class for probability function generators"""
    pass

class UniformProbGen(ProbGen):
    """Generate Uniform probability functions"""
    pass

class NormalProbGen(ProbGen):
    """Generate Normal probabilibty functions"""
    pass

class LogNormalProbGen(ProbGen):
    """Generate Log-normal probability functions"""
    pass

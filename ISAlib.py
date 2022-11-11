#defines the functions to calculate te final valeus
from cmath import exp

#sets up base values
p0 = 101325
T0 = 288.15
R = 287
g = 9.80665

def calc_temp(h,layer):
    if layer.lapseRate == 0:
        T = layer.getBaseTemp()
    else:
        T = layer.getBaseTemp() + layer.lapseRate * (h - layer.hBase)

    return T

def calc_pressure(h,layer):
    T = calc_temp(h, layer)
    if layer.lapseRate == 0:
        p = layer.getBasePressure() * exp((-g/(R*T)) * (h - layer.hBase))
    else:
        p = layer.getBasePressure() * ((T/layer.getBaseTemp())**(-g/(R*layer.lapseRate)))

    return p

def calc_density(p, T):
    return p/(R*T)

class Layer:
    def __init__(self, hBase, hCeil, lapseRate, TBase = None, pBase = None):
        self.hBase = hBase
        self.TBase = TBase
        self.pBase = pBase
        self.hCeil = hCeil
        self.lapseRate = lapseRate

    def getBaseTemp(self):
        if self.TBase is None:
            return calc_temp(self.hBase ,layers[layers.index(self) - 1])
        else:
            return self.TBase
    
    def getBasePressure(self):
        if self.pBase is None:
            return calc_pressure(self.hBase ,layers[layers.index(self) - 1])
        else:
            return self.pBase

layers = [
Layer(0, 11000, -0.0065, T0, p0),
Layer(11000, 20000, 0),
Layer(20000, 32000, 0.001),
Layer(32000, 47000, 0.0028),
Layer(47000, 50000, 0)
]
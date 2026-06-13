import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def criar_variaveis():
    dano = ctrl.Antecedent(np.arange(0, 11, 1), 'dano')
    fadiga = ctrl.Antecedent(np.arange(0, 11, 1), 'fadiga')
    risco = ctrl.Consequent(np.arange(0, 101, 1), 'risco')

    dano['baixo'] = fuzz.trimf(dano.universe, [0, 0, 4])
    dano['medio'] = fuzz.trimf(dano.universe, [2, 5, 8])
    dano['alto'] = fuzz.trimf(dano.universe, [6, 10, 10])

    fadiga['baixa'] = fuzz.trimf(fadiga.universe, [0, 0, 4])
    fadiga['media'] = fuzz.trimf(fadiga.universe, [2, 5, 8])
    fadiga['alta'] = fuzz.trimf(fadiga.universe, [6, 10, 10])

    risco['baixo'] = fuzz.trimf(risco.universe, [0, 0, 40])
    risco['medio'] = fuzz.trimf(risco.universe, [30, 50, 70])
    risco['alto'] = fuzz.trimf(risco.universe, [60, 100, 100])

    return dano, fadiga, risco
import numpy as np

def abc_to_seq(va, vb, vc):
    """
    Transform 3-phase quantities (abc) to symmetrical components (012).
    :param va: phase A value
    :param vb: phase B value
    :param vc: phase C value
    :return: v0, v1, v2 (zero, positive, negative sequence components)
    """
    a = np.exp(1j * 2 * np.pi / 3)
    v0 = (va + vb + vc) / 3
    v1 = (va + a * vb + a**2 * vc) / 3
    v2 = (va + a**2 * vb + a * vc) / 3
    return v0, v1, v2

def seq_to_abc(v0, v1, v2):
    """
    Transform symmetrical components (012) to 3-phase quantities (abc).
    :param v0: zero sequence component
    :param v1: positive sequence component
    :param v2: negative sequence component
    :return: va, vb, vc (phase A, B, C values)
    """
    a = np.exp(1j * 2 * np.pi / 3)
    va = v0 + v1 + v2
    vb = v0 + a**2 * v1 + a * v2
    vc = v0 + a * v1 + a**2 * v2
    return va, vb, vc
import numpy as np

def d(k, l, u, v): # відстань від центру спектру:
    return np.sqrt((k-u)*(k-u)+(l-v)*(l-v))
    

def lowpass_filter(_fourier, _d0, _coef): # зміна частот, де d > d0
    result = _fourier.copy()
    M, N = _fourier.shape
    m, n = M//2, N//2
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            if d(i,j,m,n) > _d0: 
                if _coef == 0: 
                # не множимо на 0 - проблеми при побудові спектру на логарифмічній шкалі
                   result[i,j] = 1
                else: 
                    result[i,j] *= _coef
    return result


def highpass_filter(_fourier, _d0, _coef): # зміни частот d < d0
    result = _fourier.copy()
    M, N = _fourier.shape
    m, n = M//2, N//2
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            if d(i,j,m,n) < _d0:
                if _coef == 0:
                   result[i,j] = 1 
                else: 
                    result[i,j] *= _coef
    return result

def bondstop_filter(_fourier, _d0, _d1, _coef): # зміна частот в діапазоні від d0 до d1
    result = _fourier.copy()
    M, N = _fourier.shape
    m, n = M//2, N//2
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            if _d0 < d(i,j,m,n) < _d1:
                if _coef == 0:
                   result[i,j] = 1 
                else: 
                    result[i,j] *= _coef
    return result

def bondpass_filter(_fourier, _d0, _d1, _coef): # зміна тих частот, що не потрапляють в діапазон d0-d1
    result = _fourier.copy()
    M, N = _fourier.shape
    m, n = M//2, N//2
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            if d(i,j,m,n) > _d1 or d(i,j,m,n) < _d0:
                if _coef == 0:
                   result[i,j] = 1 
                else: 
                    result[i,j] *= _coef
    return result
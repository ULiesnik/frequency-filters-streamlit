import numpy as np


def discrete_ft(x_array):
    N = x_array.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    twiddle_factor = np.exp(-2j * np.pi * k * n / N) # коефіцієнт обертання
    X = np.dot(twiddle_factor, x_array)
    return X


def fast_ft(x_array):
    N = x_array.shape[0]
    # непарні масиви не поділиш порівну і нема особливого сенсу ділити малі:
    if (N % 2 > 0) or (N <= 8): 
        return discrete_ft(x_array)
    else:
        even_fft = fast_ft(x_array[::2]) # рекурсивне застосування
        odd_fft = fast_ft(x_array[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N) # коефіцієнт обертання
        M = int(N / 2)
        fft = np.concatenate([even_fft + factor[:M] * odd_fft, 
                               even_fft + factor[M:] * odd_fft])
        return fft


def fast_ft2(x_2d_array):

    x_2d_array = np.asarray(x_2d_array)
    # одновимірне за рядками:
    fft_rows = np.array([fast_ft(row) for row in x_2d_array]) 
    # одновимірне за стовпцями:
    fft_cols = np.array([fast_ft(col) for col in fft_rows.T]).T 
    
    return fft_cols


def reverse_dft(X_array): 
    N = X_array.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    # зміна знаку для коефіцієнтів у степені е
    x = np.dot(np.exp(2j * np.pi * k * n / N), X_array) 
    return x


def _reverse_fft(X_array): 
    N = X_array.shape[0]
    
    if (N % 2 > 0) or (N <= 8):
        return reverse_dft(X_array) 
    else:
        even = _reverse_fft(X_array[::2])
        odd = _reverse_fft(X_array[1::2])
        M = int(N / 2)
        factor = np.exp(2j * np.pi * np.arange(N) / N) # знову коефіцієнт обертання
        result = np.concatenate([even + factor[:M] * odd, 
                               even + factor[M:] * odd]) 
        
        return result


def reverse_fft(X_array): # ділення на N для нормалізації результату:
    return _reverse_fft(X_array)/ X_array.shape[0] 


def reverse_fft2(X_2d_array):
    # одновимірний варіант за рядками:
    rows = np.array([reverse_fft(row) for row in X_2d_array]) 
    # тепер за стовпцями:
    cols = np.array([reverse_fft(col) for col in rows.T]).T 
    
    return cols


def ft_shift(f_transform): # зміщення результатів для кращого відображення спектру

    M, N = f_transform.shape
    shifted_transform = np.zeros_like(f_transform)
    center_m, center_n = M // 2, N // 2
    # заміна квадратів:
    # верхній лівий до нижнього правого
    shifted_transform[:center_m, :center_n] = f_transform[center_m:, center_n:]
    # верхній правий до нижнього лівого
    shifted_transform[:center_m, center_n:] = f_transform[center_m:, :center_n]
    # нижній лівий до верхнього правого
    shifted_transform[center_m:, :center_n] = f_transform[:center_m, center_n:]
    # нижній правий до верхнього лівого
    shifted_transform[center_m:, center_n:] = f_transform[:center_m, :center_n]
    
    return shifted_transform


def reverse_ft_shift(shifted_transform):

    M, N = shifted_transform.shape
    f_transform = np.zeros_like(shifted_transform)
    center_m, center_n = M // 2, N // 2
    # нижній правий до верхнього лівого
    f_transform[center_m:, center_n:] = shifted_transform[:center_m, :center_n]
    # нижній лівий до верхнього правого
    f_transform[center_m:, :center_n] = shifted_transform[:center_m, center_n:]
    # верхній правий до нижнього лівого
    f_transform[:center_m, center_n:] = shifted_transform[center_m:, :center_n]
    # верхній лівий до нижнього правого
    f_transform[:center_m, :center_n] = shifted_transform[center_m:, center_n:]
    
    return f_transform
    

def spectrum(_ft): # логарифмічна шкала для кращого відображення:
    return 20 * np.log(np.abs(_ft)) 


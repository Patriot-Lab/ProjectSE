import numpy as np
from numba import njit

@njit
def dwt(seq):
    seq = np.copy(seq)
    n = seq.shape[0]

    detail_len = n >> 1
    approx_len = n - detail_len

    for i in range(1, detail_len):
        seq[(i << 1) - 1] -= (seq[(i - 1) << 1] + seq[i << 1]) >> 1
    seq[(detail_len << 1) - 1] -= (seq[(detail_len - 1) << 1] + seq[(approx_len - 1) << 1]) >> 1

    seq[0] += (seq[1] + seq[1] + 2) >> 2
    for i in range(1, approx_len - 1):
        seq[i << 1] += (seq[(i << 1) - 1] + seq[(i << 1) + 1] + 2) >> 2
    seq[(approx_len - 1) << 1] += (seq[(approx_len << 1) - 3] + seq[(detail_len << 1) - 1] + 2) >> 2

    return seq

@njit
def idwt(seq):
    seq = np.copy(seq)
    n = seq.shape[0]

    detail_len = n >> 1
    approx_len = n - detail_len
    
    seq[0] -= (seq[1] + seq[1] + 2) >> 2
    for i in range(1, approx_len - 1):
        seq[i << 1] -= (seq[(i << 1) - 1] + seq[(i << 1) + 1] + 2) >> 2
    seq[(approx_len - 1) << 1] -= (seq[(approx_len << 1) - 3] + seq[(detail_len << 1) - 1] + 2) >> 2

    for i in range(1, detail_len):
        seq[(i << 1) - 1] += (seq[(i - 1) << 1] + seq[i << 1]) >> 1
    seq[(detail_len << 1) - 1] += (seq[(detail_len - 1) << 1] + seq[(approx_len - 1) << 1]) >> 1

    return seq


def dwt2d(seq):
    
    horizontal_transform = np.apply_along_axis(dwt, axis=1, arr=seq)
    l = horizontal_transform[:,::2]
    h = horizontal_transform[:,1::2]
      
    vertical_transform_l = np.apply_along_axis(dwt, axis=0, arr=l)
    ll = np.array(vertical_transform_l[::2,:])
    lh = np.array(vertical_transform_l[1::2,:])
 
    vertical_transform_h = np.apply_along_axis(dwt, axis=0, arr=h)
    hl = np.array(vertical_transform_h[::2,:])    
    hh = np.array(vertical_transform_h[1::2,:])
    
    return ll, hl, lh, hh


def idwt2d(ll, hl, lh, hh):
    
    l_rows = ll.shape[0] + lh.shape[0]
    l_cols = max(ll.shape[1], lh.shape[1])
    vertical_transform_l = np.empty((l_rows, l_cols), dtype=ll.dtype)
    vertical_transform_l[::2, :] = ll
    vertical_transform_l[1::2, :] = lh
    l = np.apply_along_axis(idwt, axis=0, arr=vertical_transform_l)    
    
    h_rows = hl.shape[0] + hh.shape[0]
    h_cols = max(hl.shape[1], hh.shape[1])
    vertical_transform_h = np.empty((h_rows, h_cols), dtype=hl.dtype)
    vertical_transform_h[::2, :] = hl
    vertical_transform_h[1::2, :] = hh
    h = np.apply_along_axis(idwt, axis=0, arr=vertical_transform_h)

    seq_rows = max(l.shape[0], h.shape[0])
    seq_cols = l.shape[1]+h.shape[1]
    horizontal_transform = np.empty((seq_rows, seq_cols), dtype=l.dtype)
    horizontal_transform[:, ::2] = l
    horizontal_transform[:, 1::2] = h
    seq = np.apply_along_axis(idwt, axis=1, arr=horizontal_transform)
    
    return seq
        
import numpy as np
from numba import njit
from utils import time_it

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

@time_it
def dwt2d(seq):
    try:
        # Horizontal transform
        horizontal_transform = np.empty_like(seq)
        for i in range(seq.shape[0]):
            horizontal_transform[i] = dwt(seq[i])

        # Split into approximation and detail coefficients
        l = horizontal_transform[:, ::2]
        h = horizontal_transform[:, 1::2]

        # Vertical transform on l
        vertical_transform_l = np.empty_like(l)
        for i in range(l.shape[1]):
            vertical_transform_l[:, i] = dwt(l[:, i])

        ll = vertical_transform_l[::2, :]
        lh = vertical_transform_l[1::2, :]

        # Vertical transform on h
        vertical_transform_h = np.empty_like(h)
        for i in range(h.shape[1]):
            vertical_transform_h[:, i] = dwt(h[:, i])

        hl = vertical_transform_h[::2, :]
        hh = vertical_transform_h[1::2, :]

        return ll, hl, lh, hh
    except Exception as e:
        raise ValueError(f"Error during DWT2D computation: {str(e)}")


@time_it
def idwt2d(ll, hl, lh, hh):
    try:
        # Combine vertical transform results for l and h
        l = np.empty((ll.shape[0] + lh.shape[0], ll.shape[1]), dtype=ll.dtype)
        l[::2, :] = ll
        l[1::2, :] = lh

        h = np.empty((hl.shape[0] + hh.shape[0], hl.shape[1]), dtype=hl.dtype)
        h[::2, :] = hl
        h[1::2, :] = hh

        # Perform vertical inverse DWT
        for i in range(l.shape[1]):
            l[:, i] = idwt(l[:, i])

        for i in range(h.shape[1]):
            h[:, i] = idwt(h[:, i])

        # Horizontal inverse DWT
        seq = np.empty((l.shape[0], l.shape[1] + h.shape[1]), dtype=l.dtype)
        seq[:, ::2] = l
        seq[:, 1::2] = h

        for i in range(seq.shape[0]):
            seq[i] = idwt(seq[i])

        return seq
    except Exception as e:
        raise ValueError(f"Error during IDWT2D computation: {str(e)}")

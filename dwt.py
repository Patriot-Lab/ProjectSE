import numpy as np
from numba import njit, prange
from utils import time_it

@time_it
@njit(parallel=True)
def dwt2d(seq):
    nrows, ncols = seq.shape

    # Horizontal transform
    horizontal_transform = np.empty_like(seq)
    for i in prange(nrows):  # Parallelizing over rows
        seq_row = np.copy(seq[i])
        detail_len = ncols >> 1
        approx_len = ncols - detail_len

        # Perform 1D DWT on the row
        for j in range(1, detail_len):
            seq_row[(j << 1) - 1] -= (seq_row[(j - 1) << 1] + seq_row[j << 1]) >> 1
        seq_row[(detail_len << 1) - 1] -= (seq_row[(detail_len - 1) << 1] + seq_row[(approx_len - 1) << 1]) >> 1

        seq_row[0] += (seq_row[1] + seq_row[1] + 2) >> 2
        for j in range(1, approx_len - 1):
            seq_row[j << 1] += (seq_row[(j << 1) - 1] + seq_row[(j << 1) + 1] + 2) >> 2
        seq_row[(approx_len - 1) << 1] += (seq_row[(approx_len << 1) - 3] + seq_row[(detail_len << 1) - 1] + 2) >> 2

        horizontal_transform[i] = seq_row

    # Split into approximation and detail coefficients
    l = horizontal_transform[:, ::2]
    h = horizontal_transform[:, 1::2]

    # Vertical transform on l
    vertical_transform_l = np.empty_like(l)
    for i in prange(l.shape[1]):  # Parallelizing over columns
        seq_col = np.copy(l[:, i])
        detail_len = nrows >> 1
        approx_len = nrows - detail_len

        # Perform 1D DWT on the column
        for j in range(1, detail_len):
            seq_col[(j << 1) - 1] -= (seq_col[(j - 1) << 1] + seq_col[j << 1]) >> 1
        seq_col[(detail_len << 1) - 1] -= (seq_col[(detail_len - 1) << 1] + seq_col[(approx_len - 1) << 1]) >> 1

        seq_col[0] += (seq_col[1] + seq_col[1] + 2) >> 2
        for j in range(1, approx_len - 1):
            seq_col[j << 1] += (seq_col[(j << 1) - 1] + seq_col[(j << 1) + 1] + 2) >> 2
        seq_col[(approx_len - 1) << 1] += (seq_col[(approx_len << 1) - 3] + seq_col[(detail_len << 1) - 1] + 2) >> 2

        vertical_transform_l[:, i] = seq_col

    ll = vertical_transform_l[::2, :]
    lh = vertical_transform_l[1::2, :]

    # Vertical transform on h
    vertical_transform_h = np.empty_like(h)
    for i in prange(h.shape[1]):  # Parallelizing over columns
        seq_col = np.copy(h[:, i])
        detail_len = nrows >> 1
        approx_len = nrows - detail_len

        # Perform 1D DWT on the column
        for j in range(1, detail_len):
            seq_col[(j << 1) - 1] -= (seq_col[(j - 1) << 1] + seq_col[j << 1]) >> 1
        seq_col[(detail_len << 1) - 1] -= (seq_col[(detail_len - 1) << 1] + seq_col[(approx_len - 1) << 1]) >> 1

        seq_col[0] += (seq_col[1] + seq_col[1] + 2) >> 2
        for j in range(1, approx_len - 1):
            seq_col[j << 1] += (seq_col[(j << 1) - 1] + seq_col[(j << 1) + 1] + 2) >> 2
        seq_col[(approx_len - 1) << 1] += (seq_col[(approx_len << 1) - 3] + seq_col[(detail_len << 1) - 1] + 2) >> 2

        vertical_transform_h[:, i] = seq_col

    hl = vertical_transform_h[::2, :]
    hh = vertical_transform_h[1::2, :]

    return ll, hl, lh, hh

@time_it
@njit(parallel=True)
def idwt2d(ll, hl, lh, hh):
    nrows, ncols = ll.shape[0] * 2, ll.shape[1]

    # Combine vertical transform results for l and h
    l = np.empty((nrows, ncols), dtype=ll.dtype)
    l[::2, :] = ll
    l[1::2, :] = lh

    h = np.empty((nrows, ncols), dtype=hl.dtype)
    h[::2, :] = hl
    h[1::2, :] = hh

    # Perform vertical inverse DWT
    for i in prange(ncols):  # Parallelizing over columns
        seq_col = np.copy(l[:, i])
        detail_len = nrows >> 1
        approx_len = nrows - detail_len

        # Perform 1D IDWT on the column
        seq_col[0] -= (seq_col[1] + seq_col[1] + 2) >> 2
        for j in range(1, approx_len - 1):
            seq_col[j << 1] -= (seq_col[(j << 1) - 1] + seq_col[(j << 1) + 1] + 2) >> 2
        seq_col[(approx_len - 1) << 1] -= (seq_col[(approx_len << 1) - 3] + seq_col[(detail_len << 1) - 1] + 2) >> 2

        for j in range(1, detail_len):
            seq_col[(j << 1) - 1] += (seq_col[(j - 1) << 1] + seq_col[j << 1]) >> 1
        seq_col[(detail_len << 1) - 1] += (seq_col[(detail_len - 1) << 1] + seq_col[(approx_len - 1) << 1]) >> 1

        l[:, i] = seq_col

    # Perform vertical inverse DWT on h
    for i in prange(ncols):  # Parallelizing over columns
        seq_col = np.copy(h[:, i])
        detail_len = nrows >> 1
        approx_len = nrows - detail_len

        # Perform 1D IDWT on the column
        seq_col[0] -= (seq_col[1] + seq_col[1] + 2) >> 2
        for j in range(1, approx_len - 1):
            seq_col[j << 1] -= (seq_col[(j << 1) - 1] + seq_col[(j << 1) + 1] + 2) >> 2
        seq_col[(approx_len - 1) << 1] -= (seq_col[(approx_len << 1) - 3] + seq_col[(detail_len << 1) - 1] + 2) >> 2

        for j in range(1, detail_len):
            seq_col[(j << 1) - 1] += (seq_col[(j - 1) << 1] + seq_col[j << 1]) >> 1
        seq_col[(detail_len << 1) - 1] += (seq_col[(detail_len - 1) << 1] + seq_col[(approx_len - 1) << 1]) >> 1

        h[:, i] = seq_col

    # Horizontal inverse DWT
    seq = np.empty((nrows, ncols * 2), dtype=l.dtype)
    seq[:, ::2] = l
    seq[:, 1::2] = h

    for i in prange(nrows):  # Parallelizing over rows
        seq_row = np.copy(seq[i])
        detail_len = ncols
        approx_len = ncols * 2 - detail_len

        # Perform 1D IDWT on the row
        seq_row[0] -= (seq_row[1] + seq_row[1] + 2) >> 2
        for j in range(1, approx_len - 1):
            seq_row[j << 1] -= (seq_row[(j << 1) - 1] + seq_row[(j << 1) + 1] + 2) >> 2
        seq_row[(approx_len - 1) << 1] -= (seq_row[(approx_len << 1) - 3] + seq_row[(detail_len << 1) - 1] + 2) >> 2

        for j in range(1, detail_len):
            seq_row[(j << 1) - 1] += (seq_row[(j - 1) << 1] + seq_row[j << 1]) >> 1
        seq_row[(detail_len << 1) - 1] += (seq_row[(detail_len - 1) << 1] + seq_row[(approx_len - 1) << 1]) >> 1

        seq[i] = seq_row

    return seq

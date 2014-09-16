#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


import numpy as np
from scipy.spatial.distance import pdist, squareform
from sklearn.decomposition import PCA as sklearn_PCA
from math import log, sqrt
from scipy.optimize import minimize, newton

def pca(X, dim):
    return np.transpose(sklearn_PCA(dim).fit(np.transpose(X)).components_)


def monotonic_bisect(func, a, b, c, tol = 1e-5, maxiter = 50):
    f = func(c)
    it = 0
    while abs(f) > tol and it < maxiter:
        if f > 0:
            a = c
            if b == np.inf:
                c = c*2.
            else:
                c = (c + b)/2.
        else:
            b = c
            if a == -np.inf:
                c = c/2.
            else:
                c = (a+c)/2.
        f = func(c)
        print (c,f)
        it += 1
    return c
        

def make_P(X, perplexity = 30., square = True):
    n, dim = X.shape

    pair_dist2 = squareform(pdist(X))**2
    P = np.zeros([n,n])
    beta = np.ones(n) 

    def log_actual_perplexity(i, beta, return_P = False):
        D = pair_dist2[i,np.r_[0:i,i+1:n]].copy()
        P = np.exp(-D*beta)
        P_sum = np.sum(P)
        H = np.log(P_sum) + beta*np.dot(D,P)/P_sum
        if return_P:
            return (H, P/P_sum)
        else:
            return H

    log_perplexity = np.log(perplexity)
    # NOTE: The original Maatin version had a bug affecting convergence
    for i in range(n):
        func = lambda beta: (log_actual_perplexity(i, beta) - log_perplexity)
        beta = monotonic_bisect(func, -np.inf, np.inf, 1)
        H, P[i,np.r_[0:i,i+1:n]] = log_actual_perplexity(i, beta, return_P = True)

    return P

def naive_tsne(X, dim = 2, perplexity = 30.):
    n = X.shape[0]
    P = make_P(X, perplexity)
    P = (P + np.transpose(P))/n 

    # Pairwise distance matrix for x
    dist_x = squareform(pdist(X))

    def q(Y):
        dist_y = squareform(pdist(Y))
        # Subtract n for the points that measure distance from themselves
        denom = np.sum( (1+dist_y**2)**(-1)) - n
        Q = (1+dist_y**2)**(-1)/denom
        for j in range(n):
            Q[j,j] = 1
        return Q
    def C(Y):
        Y = Y.reshape([n,dim])
        C = 0
        Q = q(Y)
        for i in range(n):
            for j in range(n):
                if i != j:
                    C += P[i,j]*log(P[i,j]/Q[i,j])
        return C
    
    def C_der(Y):
        Y = Y.reshape([n,dim])
        dC = np.zeros([n, dim])
        Q = q(Y)
        dist_y = squareform(pdist(Y))
        for i in range(n):
            for j in range(n):
                dC[i] += 4*(P[i,j]-Q[i,j])*(1/(1+dist_y[i,j]**2))*(Y[i]-Y[j])
        return dC.reshape(n*dim)
    # Inital estimates via PCA
    Y = pca(X, dim)
    Q = q(Y)
    print Q
    print P
    print C(Y)
    print C_der(Y)
    res = minimize(C,Y.reshape(n*dim))
    return res.x.reshape([n,dim])


if __name__ == '__main__':
    X = np.concatenate( (np.random.randn(2,5), np.random.randn(2,5)+100))
    from maatin_tsne import tsne as mtsne

    from maatin_tsne import x2p

    P1 = x2p(X, perplexity = 1.5)
    P2 = make_P(X, perplexity = 1.5)
    print P1
    print " "
    print P2
    print " "
    print np.max(np.abs(P1 - P2))
    
    Y2 = mtsne(X, perplexity = 5)
    Y = naive_tsne(X, perplexity = 5)
    print Y
    print Y2

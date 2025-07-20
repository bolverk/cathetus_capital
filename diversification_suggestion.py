import os
from glob import glob
import pandas as pd
import numpy as np

def diversification_suggestion(portfolio, n_suggestions=5):

    df = pd.read_csv('unified.csv')
    history = sum((df[k].values*v for k,v in portfolio.items()))

    scores = np.dot(df.to_numpy().T, history)

    return df.columns[np.argsort(scores**2)[:n_suggestions]].values

    import pdb
    pdb.set_trace()


def main():

    print(diversification_suggestion({'spy':0.8, 'bnd':0.2}))

if __name__ == '__main__':

    main()
    

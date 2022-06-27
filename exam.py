# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Programming in Python
# ## Exam: June 27, 2022
#
# You can solve the exercises below by using standard Python 3.10 libraries, NumPy, Matplotlib, Pandas, PyMC3.
# You can browse the documentation: [Python](https://docs.python.org/3.10/), [NumPy](https://numpy.org/doc/stable/user/index.html), [Matplotlib](https://matplotlib.org/stable/users/index.html), [Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html), [PyMC3](https://docs.pymc.io/en/v3/index.html).
# You can also look at the [slides of the course](https://homes.di.unimi.it/monga/lucidi2122/pyqb00.pdf) or your code on [GitHub](https://github.com).
#
# **It is forbidden to communicate with others.** 
#
#
#
#

import numpy as np
import pandas as pd  # type: ignore
import matplotlib.pyplot as plt # type: ignore
import pymc3 as pm   # type: ignore

# ### Exercise 1 (max 3 points)
#
# The file [mice.csv](./mice.csv) (source: https://archive.ics.uci.edu/ml/datasets/Mice+Protein+Expression) contains the expression levels of 77 proteins/protein modifications that produced detectable signals in the nuclear fraction of cortex. 
# The eight classes of mice are described based on features such as genotype, behavior and treatment. According to genotype, mice can be control or trisomic. According to behavior, some mice have been stimulated to learn (context-shock) and others have not (shock-context) and in order to assess the effect of the drug memantine in recovering the ability to learn in trisomic mice, some mice have been injected with the drug and others have not.
#
# Load the data and print the unique values for the columns Genotype, Treatment, Behavior, and class.

data = pd.read_csv('mice.csv')

for col in ['Genotype','Treatment','Behavior','class']:
    print(col, data[col].unique())

# ### Exercise 2 (max 2 points)
#
# Plot a histogram of the "Bcatenin_N" values.
#

# +
fig, ax = plt.subplots()

data['Bcatenin_N'].hist(ax=ax)
_ = ax.set_title('Bcatenin_N')
# -

# ### Exercise 3 (max 3 points)
#
# Make a figure with two columns of plots. In the first column plot together (contrast) the histograms of 'Bcatenin_N' for the two genotypes. In the second column plot together (contrast) the histograms of 'Bcatenin_N' for the two treatments. Use density histograms to make the diagrams easy to compare; add proper titles and legends.
#

# +
fig, ax = plt.subplots(ncols=2)


col = 'Bcatenin_N'
for i, f in enumerate(['Genotype', 'Treatment']):
    for g in data[f].unique():
        ax[i].hist(data[data[f] == g][col], density=True, label=g)
        ax[i].legend()
        ax[i].set_title(f)
# -

# ### Exercise 4 (max 5 points)
#
# Make a (huge) figure with the histograms plotted in the previous exercise for all the proteins (there are 77 proteins columns, note that all ends with `'_N'`), each in a different row of the figure (the figure will have 2 columns and 77 rows; to make it readable set the `figsize` to `(5, 3*77)`). 
#

# +
fig, ax = plt.subplots(ncols=2, nrows=77, figsize=(5, 3*77))


for j, col in enumerate([c for c in data.columns if c.endswith('_N')]):
    for i, f in enumerate(['Genotype', 'Treatment']):
        for g in data[f].unique():
            ax[j, i].hist(data[data[f] == g][col], density=True, label=g)
            ax[j, i].legend()
            ax[j, i].set_title(f'{col} ({f})')
_ = fig.tight_layout()


# -

# ### Exercise 5 (max 7 points)
#
# Define a function `mk_class` that takes three string parameters and returns a string composed by three parts joined by `-`: the first and the third part are the lowercase versions of, respectively, the first or the third letter of the first or the third parameter, the second part is the second parameter with all non-alphabetic characters removed.
# For example, if the parameters are `'Mattia'`, `'s/he makes difficult exercises!'`, `'Professor'`, the return value should be `m-shemakesdifficultexercises-p`.
#
# To get the full marks, you should declare correctly the type hints and add a test within a doctest string.

def mk_class(a: str, b: str, c: str) -> str:
    """Return a composed string.
    
    >>> mk_class('Mattia', 's/he makes difficult exercises!', 'Professor')
    'm-shemakesdifficultexercises-p'
    
    """
    t = ''.join([x for x in b if x.isalpha()])
    return a[0].lower() + '-' + t + '-' + c[0].lower() 


# ### Exercise 6 (max 5 points)
#
# The column `class` can be computed by combining the columns `Genotype`, `Behavior`, and `Treatment` with the same logic described in the previous exercise.
# Use the function `mk_class` to check that the class column of the data is in fact correct for all the rows.
#
# To get full marks, avoid the use of explicit loops.
#

assert data.apply(lambda x: mk_class(x['Genotype'], x['Behavior'], x['Treatment']) == x['class'], 
           axis=1).all()

# ### Exercise 7 (max 4 points)
#
# Draw the scatterplots of the standardized values of `'Bcatenin_N'` vs. (also standardized) `'Tau_N'`. Make a different plot for each class. The standard value $z$ corresponding to a value $v$ taken from a series with mean $\bar v$ and standard deviation $\sigma$ is: $z = \frac{v - \bar v}{\sigma}$.

# +
x = 'Bcatenin_N'
y = 'Tau_N'
classes = data['class'].unique()

def standardize(x: pd.Series) -> pd.Series:
    """For each value assess its distance from the mean, w.r.t. the standard deviation.

    >>> standardize(pd.Series([-1, 0, 1])).tolist() # mean: 0, devstd: 1
    [-1.0, 0.0, 1.0]
    """
    return (x - x.mean()) / x.std()

fig, ax = plt.subplots(len(classes), figsize=(5, 3*len(classes)))
for i, c in enumerate(classes):
    d = data[data['class'] == c]
    ax[i].scatter(standardize(d[x]), standardize(d[y]))
    ax[i].set_title(c)
fig.tight_layout()




# -

# ### Exercise 8 (max 4 points)
#
# Make a picture to compare the distribution of the values of `'Bcatenin_N'` with a Normal (Gaussian) distribution with mean $2.15$ and variance $0.4$.

# +
fig, ax = plt.subplots()

ax.hist(data['Bcatenin_N'], density=True, label='Bcatenin_N')
ax.hist(np.random.normal(2.15, .4, size=data['Bcatenin_N'].count()), 
        density=True, alpha=.5, label='Random')
_ = ax.legend()
# -



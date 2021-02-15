# Import libraries
import pandas as pd
import numpy as np

# Number of random draws from the prior
n_draw = 1000000

# Defining and drawing from the prior distribution 
prior_rate = pd.Series(np.random.uniform(0, 1, size = n_draw)) 

# It's always good to eyeball the prior to make sure it looks ok.
prior_rate.hist()

# Defining the generative model
def gen_model(prob):
    return(np.random.binomial(1232, prob))

#  the generative model
subscribers = list()

# Simulating the data
for p in prior_rate:
    subscribers.append(gen_model(p))
                    
# Observed data
observed_data = 34

# Here you filter off all draws that do not match the data.
post_rate = prior_rate[list(map(lambda x: x == observed_data, subscribers))]

post_rate.hist() # Eyeball the posterior


# See that we got enought draws left after the filtering. 
# There are no rules here, but you probably want to aim for >1000 draws.

# Now you can summarize the posterior, where a common summary is to take the mean or the median posterior, 
# and perhaps a 95% quantile interval.

print('Number of draws left: %d, Posterior mean: %.3f, Posterior median: %.3f, Posterior 95%% quantile interval: %.3f-%.3f' % 
      (len(post_rate), post_rate.mean(), post_rate.median(), post_rate.quantile(.025), post_rate.quantile(.975)))

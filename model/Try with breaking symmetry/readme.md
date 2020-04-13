With the existing model, no obvious evidence of issues from symmetry observed. There isn't multi-modal trend in the traceplot. 
(However it appears in the posterior plot, I am not too sure why)


## Breaking symmetry methods:

1. Use oredered transform -- the learned parameters turn out to be very off. Besides, it does not remove the multiple modes in posterior plots.
2. Use tt.sort() -- the learned parameters still have multiple modes in posterior. Also it largely increased the sampling time (about 2 times slower).

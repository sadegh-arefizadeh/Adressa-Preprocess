# Adressa-Preprocess
Preprocess Adressa to assign session id to each record:

Adressa data is usually used for session-based recommender systems. However, the original data (https://reclab.idi.ntnu.no/dataset/) does not contain the session id. Additionally, it is not in a suitable format to be used for predictive algorithms. The attached code takes care of this problem by converting the data into a data frame and assigning the session id to each record after performing the necessary calculations.

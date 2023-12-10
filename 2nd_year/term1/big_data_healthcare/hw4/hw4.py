import pandas as pd
import numpy as np
import os 
from sklearn.linear_model import LinearRegression
from itertools import combinations
from tqdm import tqdm


DATA_PATH = "./WaitData.Published.xlsx"
assert os.path.exists(DATA_PATH), f"PATH {DATA_PATH} does not exist"


df = pd.read_excel(DATA_PATH, sheet_name='F3')


df = df[~df['DayOfYear'].isna()]
columns_to_drop = ['Wait', 'x_ArrivalDTTM', 'x_ScheduledDTTM', 'x_BeginDTTM']
X = df.drop(columns=columns_to_drop)
y = df['Wait'].values



from sklearn import linear_model
model = linear_model.LinearRegression()
model.fit(X, y)
Ypred = model.predict(X) # use trained regression model to predict
r = y-Ypred # compute prediction error (residual)
e = abs(r).mean() # compute model error

print("Check the correctness: ", np.median(abs(r)))
print("Question 5: ", e)


print("Question 6: ")
# Run Python feature selection
if True: # just in case I want to disable this part
    print('\n>Python feature selection:')
    from sklearn.feature_selection import RFE
    from itertools import compress
    for nFeatures in range(1,4):
        rfe = RFE(model, n_features_to_select=nFeatures)
        X_rfe = rfe.fit_transform(X,y) #transforming data using RFE
     #Fitting the data to model
        model.fit(X_rfe,y)
        #print(rfe.support_)
        #print(rfe.ranking_)
        cols = list(compress(X.columns, rfe.support_))
        model.fit(X[cols],y)
        e = abs(y-model.predict(X[cols])).mean()
        print(e, cols)




def greedy_feature_selection(X, y, num_features_to_select, verbose: bool=False):
    best_feature_set = []
    best_error = float('inf')

    for num_features_selected in range(num_features_to_select):
        remaining_features = [col for col in X.columns if col not in best_feature_set]
        candidate_errors = []

        for feature_to_add in remaining_features:
            current_feature_set = best_feature_set + [feature_to_add]
            X_subset = X[current_feature_set]
            
            model = LinearRegression()
            model.fit(X_subset, y)
            
            absolute_errors = np.abs(model.predict(X_subset) - y)
            candidate_errors.append(absolute_errors.mean())

        best_candidate_index = np.argmin(candidate_errors)
        best_feature_set.append(remaining_features[best_candidate_index])
        best_error = candidate_errors[best_candidate_index]
        if verbose:
            print(f"{num_features_selected + 1}-feature model. Features:", *best_feature_set, sep=' | ')
            print(f"{num_features_selected + 1}-feature model. Error: ", best_error)
    return best_error, best_feature_set


print("Question 7: ")
best_error, best_feature_set = greedy_feature_selection(X, y, 3, verbose=True)

print("Best 3-feature model features:", best_feature_set)
print("Best error for the best 3-feature model:", best_error)



print("Question 8: ")
num_features_to_select = 15

best_error, best_feature_set = greedy_feature_selection(X, y, num_features_to_select, verbose=True)

print(f"Best {num_features_to_select}-feature model features:", best_feature_set)
print("Best error for the best {num_features_to_select}-feature model:", best_error)



print("Question 9: ")


best_model = None
best_error = float('inf')

num_features_to_select = 3

feature_combinations = list(combinations(X.columns, num_features_to_select))

for features in tqdm(feature_combinations):
    X_subset = X[list(features)]
    
    model = LinearRegression()
    model.fit(X_subset, y)
    
    absolute_errors = np.abs(model.predict(X_subset) - y)
    error = absolute_errors.mean()
    
    if error < best_error:
        best_error = error
        best_model = (error, *features)


print(f"Best {num_features_to_select}-feature model features:", best_model[1:])
print(f"Error for the best {num_features_to_select}-feature model:", best_error)
import pandas as pd
import sklearn.metrics
import os 

DATA_PATH = "COVID_Data_Small.xlsx"
assert os.path.exists(DATA_PATH), f"DATA PATH DOES NOT EXIST {DATA_PATH}!!!!"


df = pd.read_excel(DATA_PATH)
nRecords = df.shape[0]

vars = [
    'Temperature', 'AgeYears', 'BMI', 
    'AvgReading_Neuts_pct', 'O2_Saturation',
    'Respiration_Rate'
]


nQ = 4
dQ = 1. / nQ
quantile_list = [x * dQ for x in range(nQ)]

rules = []
count = 0


for nVar1 in range(len(vars)):
    var1 = vars[nVar1]
    for nVar2 in range(nVar1 + 1, len(vars)):
        var2 = vars[nVar2]
        for val1, val1_top in [(df[var1].quantile(q), df[var1].quantile(q+dQ)) for q in quantile_list]:
            for val2, val2_top in [(df[var2].quantile(q), df[var2].quantile(q+dQ)) for q in quantile_list]:

                rule = (df[var1] > val1) & (df[var1] < val1_top) | (df[var2] > val2) & (df[var2] < val2_top)
                count += 1

                dft = df[rule]
                if dft.shape[0] < 0.01 * nRecords:
                    continue

                ModelFit = sklearn.metrics.f1_score(df['Outcome_48Hours_Dispo'], rule)

                rule_tuple = (var1, round(val1, 3), var2, round(val2, 3))
                rules.append((round(ModelFit, 4), rule_tuple))


print("Rules processed: ", count)
rules.sort(key=lambda rule: -rule[0])


fit_list = [f for f, _ in rules]

for rule in rules:
    print("==" * 50)
    print(rule)
    print("==" * 50)

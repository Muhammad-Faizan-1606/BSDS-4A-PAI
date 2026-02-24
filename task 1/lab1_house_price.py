import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

data = pd.read_csv('train.csv')

print(data.head())
print(data.info())

print(data.shape)

missing = 0
for i in range(len(data)):
    if pd.isna(data['LotFrontage'][i]):
        missing = missing + 1
print(missing)

sum = 0
cnt = 0
for i in range(len(data)):
    if pd.isna(data['LotFrontage'][i]) == False:
        sum = sum + data['LotFrontage'][i]
        cnt = cnt + 1

avg = sum/cnt
print(avg)

for i in range(len(data)):
    if pd.isna(data['LotFrontage'][i]):
        data['LotFrontage'][i] = avg

for i in range(len(data)):
    if pd.isna(data['GarageType'][i]) == True:
        data['GarageType'][i] = 'None'

for i in range(len(data)):
    if pd.isna(data['MasVnrType'][i]):
        data['MasVnrType'][i] = 'None'
        
for i in range(len(data)):
    if pd.isna(data['MasVnrArea'][i]):
        data['MasVnrArea'][i] = 0


features = ['OverallQual','GrLivArea','GarageCars','TotalBsmtSF','FullBath','YearBuilt']

X = data[features]
y = data['SalePrice']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = RandomForestRegressor()
model.fit(X_train,y_train)

predictions = model.predict(X_test)

err = mean_absolute_error(y_test,predictions)
print(err)

test = pd.read_csv('test.csv')

for i in range(len(test)):
    if pd.isna(test['LotFrontage'][i]):
        test['LotFrontage'][i] = avg

for i in range(len(test)):
    if pd.isna(test['GarageType'][i]):
        test['GarageType'][i] = 'None'

for i in range(len(test)):
    if pd.isna(test['GarageCars'][i]):
        test['GarageCars'][i] = 0
        
for i in range(len(test)):
    if pd.isna(test['TotalBsmtSF'][i]):
        test['TotalBsmtSF'][i] = 0

X_test = test[features]

preds = model.predict(X_test)

output = pd.DataFrame()
output['Id'] = test['Id']
output['SalePrice'] = preds

output.to_csv('submission.csv',index=False)

print('done')

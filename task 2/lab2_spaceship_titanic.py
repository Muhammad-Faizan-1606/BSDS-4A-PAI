import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data = pd.read_csv('train.csv')

print(data.head())
print(data.shape)

for i in range(len(data)):
    if pd.isna(data['Age'][i]):
        data['Age'][i] = 0

for i in range(len(data)):
    if pd.isna(data['RoomService'][i]):
        data['RoomService'][i] = 0
        
for i in range(len(data)):
    if pd.isna(data['FoodCourt'][i]):
        data['FoodCourt'][i] = 0

for i in range(len(data)):
    if pd.isna(data['ShoppingMall'][i]):
        data['ShoppingMall'][i] = 0

for i in range(len(data)):
    if pd.isna(data['Spa'][i]):
        data['Spa'][i] = 0
        
for i in range(len(data)):
    if pd.isna(data['VRDeck'][i]):
        data['VRDeck'][i] = 0

for i in range(len(data)):
    if pd.isna(data['HomePlanet'][i]):
        data['HomePlanet'][i] = 'Unknown'

for i in range(len(data)):
    if pd.isna(data['CryoSleep'][i]) == True:
        data['CryoSleep'][i] = False
        
for i in range(len(data)):
    if pd.isna(data['Destination'][i]):
        data['Destination'][i] = 'Unknown'

for i in range(len(data)):
    if pd.isna(data['VIP'][i]):
        data['VIP'][i] = False

data['CryoSleep_num'] = 0
for i in range(len(data)):
    if data['CryoSleep'][i] == True:
        data['CryoSleep_num'][i] = 1

data['VIP_num'] = 0
for i in range(len(data)):
    if data['VIP'][i] == True:
        data['VIP_num'][i] = 1

data['Earth'] = 0
for i in range(len(data)):
    if data['HomePlanet'][i] == 'Earth':
        data['Earth'][i] = 1
        
data['Mars'] = 0
for i in range(len(data)):
    if data['HomePlanet'][i] == 'Mars':
        data['Mars'][i] = 1

data['Europa'] = 0
for i in range(len(data)):
    if data['HomePlanet'][i] == 'Europa':
        data['Europa'][i] = 1

data['TRAPPIST'] = 0        
for i in range(len(data)):
    if data['Destination'][i] == 'TRAPPIST-1e':
        data['TRAPPIST'][i] = 1

data['PSO'] = 0
for i in range(len(data)):
    if data['Destination'][i] == 'PSO J318.5-22':
        data['PSO'][i] = 1
        
data['Cancri'] = 0
for i in range(len(data)):
    if data['Destination'][i] == '55 Cancri e':
        data['Cancri'][i] = 1

X = data[['Age','RoomService','FoodCourt','ShoppingMall','Spa','VRDeck','CryoSleep_num','VIP_num','Earth','Mars','Europa','TRAPPIST','PSO','Cancri']]
y = data['Transported']

y_num = []
for i in range(len(y)):
    if y.iloc[i] == True:
        y_num.append(1)
    else:
        y_num.append(0)

X_train,X_test,y_train,y_test = train_test_split(X,y_num,test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train,y_train)

pred = model.predict(X_test)

acc = accuracy_score(y_test,pred)
print(acc)

test = pd.read_csv('test.csv')

for i in range(len(test)):
    if pd.isna(test['Age'][i]):
        test['Age'][i] = 0

for i in range(len(test)):
    if pd.isna(test['RoomService'][i]):
        test['RoomService'][i] = 0
        
for i in range(len(test)):
    if pd.isna(test['FoodCourt'][i]):
        test['FoodCourt'][i] = 0

for i in range(len(test)):
    if pd.isna(test['ShoppingMall'][i]):
        test['ShoppingMall'][i] = 0

for i in range(len(test)):
    if pd.isna(test['Spa'][i]):
        test['Spa'][i] = 0
        
for i in range(len(test)):
    if pd.isna(test['VRDeck'][i]):
        test['VRDeck'][i] = 0

for i in range(len(test)):
    if pd.isna(test['HomePlanet'][i]):
        test['HomePlanet'][i] = 'Unknown'

for i in range(len(test)):
    if pd.isna(test['CryoSleep'][i]):
        test['CryoSleep'][i] = False
        
for i in range(len(test)):
    if pd.isna(test['Destination'][i]):
        test['Destination'][i] = 'Unknown'

for i in range(len(test)):
    if pd.isna(test['VIP'][i]):
        test['VIP'][i] = False

test['CryoSleep_num'] = 0
for i in range(len(test)):
    if test['CryoSleep'][i] == True:
        test['CryoSleep_num'][i] = 1

test['VIP_num'] = 0
for i in range(len(test)):
    if test['VIP'][i] == True:
        test['VIP_num'][i] = 1

test['Earth'] = 0
for i in range(len(test)):
    if test['HomePlanet'][i] == 'Earth':
        test['Earth'][i] = 1
        
test['Mars'] = 0
for i in range(len(test)):
    if test['HomePlanet'][i] == 'Mars':
        test['Mars'][i] = 1

test['Europa'] = 0
for i in range(len(test)):
    if test['HomePlanet'][i] == 'Europa':
        test['Europa'][i] = 1

test['TRAPPIST'] = 0        
for i in range(len(test)):
    if test['Destination'][i] == 'TRAPPIST-1e':
        test['TRAPPIST'][i] = 1

test['PSO'] = 0
for i in range(len(test)):
    if test['Destination'][i] == 'PSO J318.5-22':
        test['PSO'][i] = 1
        
test['Cancri'] = 0
for i in range(len(test)):
    if test['Destination'][i] == '55 Cancri e':
        test['Cancri'][i] = 1

X_test = test[['Age','RoomService','FoodCourt','ShoppingMall','Spa','VRDeck','CryoSleep_num','VIP_num','Earth','Mars','Europa','TRAPPIST','PSO','Cancri']]

preds = model.predict(X_test)

output = pd.DataFrame()
output['PassengerId'] = test['PassengerId']

result = []
for i in range(len(preds)):
    if preds[i] == 1:
        result.append(True)
    else:
        result.append(False)

output['Transported'] = result

output.to_csv('submission.csv',index=False)

print('done')

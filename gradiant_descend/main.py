import csv
import numpy as np
import matplotlib.pyplot as plt

with open("housing.csv", 'r') as f:
    list_data = list(csv.reader(f, delimiter=","))

#data
x_data_new = np.zeros(62)

first_data = np.genfromtxt("housing.csv", delimiter=",", skip_header=1)
x_data = np.zeros((20640,14))
x_data[:,0]=1
x_data[:,1:9] = first_data[:,0:8]
for i in range(1,len(list_data)):
    x_data[i-1][dic[list_data[i][9]]]=1
x_data= np.nan_to_num(x_data)
y_data = first_data[:,8]
q=0

for i in range(1,14):
    x_data[:,i]=(x_data[:,i]-np.mean(x_data[:,i]))/np.std(x_data[:,i])

train_percent = 70
p = train_percent/100
random_choice = np.random.choice(a=[False, True], size=len(x_data),p=[1-p,p])

train_data = x_data[random_choice]
train_value = y_data[random_choice]
test_data = x_data[random_choice==False]
test_value = y_data[random_choice==False]

def gradientDescent(learning_rate):
    weight = np.zeros(14)
    max_iter = 1000
    costs = np.zeros(max_iter)

    for i in range(max_iter):
        xw = train_data.dot(weight)
        diff = xw - train_value
        gradient = (1/len(train_value))*train_data.T.dot(diff)
        weight = weight - learning_rate * gradient
        cost =  (1/ (2 * len(test_value))) *np.sum((test_data.dot(weight) - test_value) ** 2)
        costs[i] = np.sqrt(cost)
    print()
    print('learning rate = ',learning_rate,':')
    print('cost = ',costs[-1])
    print('weights = ',weight)
    return costs

def gradientDescentWithRegularization(learning_rate,landa):
    weight = np.zeros(14)
    max_iter = 1000
    costs = np.zeros(max_iter)

    for i in range(max_iter):
        xw = train_data.dot(weight)
        diff = xw - train_value
        gradient = (1 / len(train_value)) * train_data.T.dot(diff) + 2*(landa)*weight
        weight = weight - learning_rate * gradient
        cost = (1 / (2 * len(test_value))) * np.sum((test_data.dot(weight) - test_value) ** 2)+landa*np.sum(weight**2)
        costs[i] = np.sqrt(cost)
    print()
    print('Regularization with learning rate = ',learning_rate, 'and landa = ',landa,':')
    print('cost = ',costs[-1])
    print('weights = ',weight)
    return costs





# MSE1 = (1/(2m)) * sigma (y - xw)**2
# MSE2 = (1/(2m)) * sigma (y - xw)**2 + landa * ||w||^2




landa = 0.05

plt.subplot(2,2,1)
plt.title('learning_rate = 0.1')
plt.plot(gradientDescentWithRegularization(learning_rate = 0.1, landa=landa),label='GD with ||w||')
plt.plot(gradientDescent(0.1),label='GD')
plt.legend()

plt.subplot(2,2,2)
plt.title('learning_rate = 0.01')
plt.plot(gradientDescentWithRegularization(learning_rate = 0.01, landa=landa),label='GD with ||w||')
plt.plot(gradientDescent(0.01),label='GD')
plt.legend()

plt.subplot(2,2,3)
plt.title('learning_rate = 0.05')
plt.plot(gradientDescentWithRegularization(learning_rate = 0.05, landa=landa),label='GD with ||w||')
plt.plot(gradientDescent(0.05),label='GD')
plt.legend()

plt.subplot(2,2,4)
plt.title('learning_rate = 0.001')
plt.plot(gradientDescentWithRegularization(learning_rate = 0.001, landa=landa),label='GD with ||w||')
plt.plot(gradientDescent(0.001),label='GD')
plt.legend()
plt.show()
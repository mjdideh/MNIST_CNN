
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns


from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import itertools

from keras.utils.np_utils import to_categorical # convert to one-hot-encoding
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau

"""Loading data"""

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

train.shape

test.shape

train.head(5)

# Grabbing the labels
y = train['label']

# Grabbing everything else
X = train.drop('label', axis= 1)

# Counts of different digits
sns.countplot(y)

# Normalizing 

X = X/255.0
test = test/255.0

# Reshaping into 3D 

X = X.values.reshape(-1, 28, 28, 1)
test = test.values.reshape(-1, 28, 28, 1)

# One-hot encoding 
y = to_categorical(y, num_classes=10)



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=20, random_state=42)

# A smaple image 
plt.imshow(X_train[0][:,:,0])
plt.show()

"""CNN"""

model = Sequential([
Conv2D(filters = 32, kernel_size = (5,5),padding = 'Same',activation ='relu', input_shape = (28,28,1)),
Conv2D(filters = 32, kernel_size = (5,5),padding = 'Same', activation ='relu'),
MaxPool2D(pool_size=(2,2)),
Dropout(0.25),
Conv2D(filters = 64, kernel_size = (3,3),padding = 'Same',activation ='relu'),
Conv2D(filters = 64, kernel_size = (3,3),padding = 'Same', activation ='relu'),
MaxPool2D(pool_size=(2,2), strides=(2,2)),
Dropout(0.25),
Flatten(),
Dense(256, activation = "relu"),
Dropout(0.5),
Dense(10, activation = "softmax")
])

# Optimizer
optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

# Compile
model.compile(optimizer , loss = "categorical_crossentropy", metrics=["accuracy"])

# Set a learning rate annealer
learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc', 
                                            patience=3, 
                                            verbose=1, 
                                            factor=0.5, 
                                            min_lr=0.00001)



# Training

history = model.fit(X_train, y_train, batch_size=86, epochs=30, validation_data=(X_test, y_test), verbose=1)

# prediction

y_pred = model.predict(test)

y_pred[0:2,:]

# Selecting the index with maximum probability
y_pred = np.argmax(y_pred,axis=1)

y_pred[:10]

sub = pd.DataFrame({
    'ImageId':range(1,28001),
    'Label': y_pred 
})

sub.to_csv('MNIST_CNN.csv', index=False)


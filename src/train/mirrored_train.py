import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

def texto_array(text):
    x, y = map(int, text.strip('()').split(', '))
    return [x, y]

dataset = "../../data/bariumDataCd.csv"
dados = pd.read_csv(dataset)

# mudei aqui
x = dados.loc[:, ~dados.columns.str.contains('referencial|diagonal')].drop(['movimento'], axis=1).values
# até aqui

videos = np.zeros(((x.shape[0]*2), 20, 21, 2))

count_videos = 0

for video in x:

    count_coord = 0
    count_img = 0

    imagens = np.zeros((20, 21, 2))
    imagens_espelhadas = np.zeros((20, 21, 2))

    imagem = np.zeros((21, 2))
    imagem_espelhada = np.zeros((21, 2))
    for coordenada in video:

        array = texto_array(coordenada)
        imagem[count_coord][0], imagem[count_coord][1] = array[0], array[1] 
        imagem_espelhada[count_coord][0], imagem_espelhada[count_coord][1] = (100 - array[0]), array[1] 
        
        if count_coord <= 19:
            count_coord += 1

        else:
            imagens[count_img] = imagem
            imagens_espelhadas[count_img] = imagem_espelhada
            imagem = np.zeros((21, 2))
            imagem_espelhada = np.zeros((21, 2))
            count_img += 1
            count_coord = 0
            
    videos[count_videos] = imagens
    videos[count_videos*2] = imagens_espelhadas
    count_videos += 1

x = videos

y = dados['movimento']

new_y = np.zeros((y.shape[0] * 2))
a = 0
for dado in y:
    new_y[a] = dado
    new_y[a*2] = dado
    a += 1

y = new_y

quantidade_movimentos = len(np.unique(y))

y_encoded = pd.get_dummies(y)

x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size=0.2, random_state=42)

x_train = x_train.reshape(x_train.shape[0], 20, 21, 2)
x_test = x_test.reshape(x_test.shape[0], 20, 21, 2)

model = Sequential()

# Modelo mais simples
# model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(20, 21, 2)))
# model.add(MaxPooling2D((2, 2)))
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(MaxPooling2D((2, 2)))
# model.add(Flatten())
# model.add(Dense(64, activation='relu'))
# model.add(Dense(quantidade_movimentos, activation='softmax'))

# Modelo mais complexo
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(20, 21, 2)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(quantidade_movimentos, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10, batch_size=32, validation_data=(x_test, y_test))

loss, accuracy = model.evaluate(x_test, y_test)
print(f"Acurácia do modelo: {accuracy*100:.2f}%")

model.save("../../models/modelMirror.keras")
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Input, Dense, Flatten, Dropout
from keras.utils import to_categorical

def texto_array(text):
    x, y = map(int, text.strip('()').split(', '))
    return [x, y]

dataset = "../../data/bariumDataCd.csv"
dados = pd.read_csv(dataset)

x = dados.loc[:, ~dados.columns.str.contains('referencial|diagonal')].drop(['movimento'], axis=1).values

videos = np.zeros(((x.shape[0]), 20, 21, 2))

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
    count_videos += 1

x = videos

y = dados['movimento']

quantidade_movimentos = len(np.unique(y))

y = to_categorical(y, quantidade_movimentos)

print(quantidade_movimentos)

print(y)
x = x.reshape(x.shape[0], 840)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

x_test = x_test.reshape(x_test.shape[0], 840)
x_train = x_train.reshape(x_train.shape[0], 840)


model = Sequential()

# model.add(Input(shape=(840)))
# model.add(Flatten())
# model.add(Dense(32, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(64, activation='relu'))
# model.add(Dense(128, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(512, activation='sigmoid'))
# model.add(Dense(quantidade_movimentos, activation='softmax'))

model.add(Input(shape=(840)))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.15))
model.add(Dense(quantidade_movimentos, activation='softmax'))


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=300, batch_size=256, validation_data=(x_test, y_test))

loss, accuracy = model.evaluate(x, y)
print(f"Acurácia do modelo: {accuracy*100:.2f}%")

model.save("../../models/modelTest2.keras")
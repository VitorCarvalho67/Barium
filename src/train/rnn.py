import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dropout, Dense, LSTM

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

X_train, X_test, Y_train, Y_test = train_test_split(x, y_encoded, test_size=0.2, random_state=42)

X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], -1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], -1)

# Crie um modelo RNN
model = Sequential()
model.add(LSTM(94, input_shape=(20, 21 * 2)))
model.add(Dropout(0.2088))
model.add(Dense(quantidade_movimentos, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

loss0, accuracy0 = model.evaluate(X_test, Y_test)

model.fit(X_train, Y_train, epochs=10, batch_size=32, validation_split=0.2)

loss, accuracy = model.evaluate(x.reshape(x.shape[0], x.shape[1], -1), y_encoded)
print(f'Acurácia no conjunto total antes do treinamento: {accuracy0*100:.2f}%')
print(f'Acurácia no conjunto de teste pós treinamento: {accuracy*100:.2f}%')
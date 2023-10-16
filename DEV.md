# Barium

Arquivo para fazer a coleta de dados e transformar em um dataset
Objetivo: Criar um dataset com os dados coletados através da webcam para treinar um modelo de machine learning

Colunas do dataset:
p0_0,p1_0,p2_0,p3_0,p4_0,p5_0,p6_0,p7_0,p8_0,p9_0,p10_0,p11_0,p12_0,p13_0,p14_0,p15_0,p16_0,p17_0,p18_0,p19_0,p20_0,diagonal0,referencial0,
p0_1,p1_1,p2_1,p3_1,p4_1,p5_1,p6_1,p7_1,p8_1,p9_1,p10_1,p11_1,p12_1,p13_1,p14_1,p15_1,p16_1,p17_1,p18_1,p19_1,p20_1,diagonal1,referencial1,
p0_2,p1_2,p2_2,p3_2,p4_2,p5_2,p6_2,p7_2,p8_2,p9_2,p10_2,p11_2,p12_2,p13_2,p14_2,p15_2,p16_2,p17_2,p18_2,p19_2,p20_2,diagonal2,referencial2,
p0_3,p1_3,p2_3,p3_3,p4_3,p5_3,p6_3,p7_3,p8_3,p9_3,p10_3,p11_3,p12_3,p13_3,p14_3,p15_3,p16_3,p17_3,p18_3,p19_3,p20_3,diagonal3,referencial3,
p0_4,p1_4,p2_4,p3_4,p4_4,p5_4,p6_4,p7_4,p8_4,p9_4,p10_4,p11_4,p12_4,p13_4,p14_4,p15_4,p16_4,p17_4,p18_4,p19_4,p20_4,diagonal4,referencial4,
p0_5,p1_5,p2_5,p3_5,p4_5,p5_5,p6_5,p7_5,p8_5,p9_5,p10_5,p11_5,p12_5,p13_5,p14_5,p15_5,p16_5,p17_5,p18_5,p19_5,p20_5,diagonal5,referencial5,
p0_6,p1_6,p2_6,p3_6,p4_6,p5_6,p6_6,p7_6,p8_6,p9_6,p10_6,p11_6,p12_6,p13_6,p14_6,p15_6,p16_6,p17_6,p18_6,p19_6,p20_6,diagonal6,referencial6,
p0_7,p1_7,p2_7,p3_7,p4_7,p5_7,p6_7,p7_7,p8_7,p9_7,p10_7,p11_7,p12_7,p13_7,p14_7,p15_7,p16_7,p17_7,p18_7,p19_7,p20_7,diagonal7,referencial7,
p0_8,p1_8,p2_8,p3_8,p4_8,p5_8,p6_8,p7_8,p8_8,p9_8,p10_8,p11_8,p12_8,p13_8,p14_8,p15_8,p16_8,p17_8,p18_8,p19_8,p20_8,diagonal8,referencial8,
p0_9,p1_9,p2_9,p3_9,p4_9,p5_9,p6_9,p7_9,p8_9,p9_9,p10_9,p11_9,p12_9,p13_9,p14_9,p15_9,p16_9,p17_9,p18_9,p19_9,p20_9,diagonal9,referencial9,
p0_10,p1_10,p2_10,p3_10,p4_10,p5_10,p6_10,p7_10,p8_10,p9_10,p10_10,p11_10,p12_10,p13_10,p14_10,p15_10,p16_10,p17_10,p18_10,p19_10,p20_10,diagonal10,referencial10,
p0_11,p1_11,p2_11,p3_11,p4_11,p5_11,p6_11,p7_11,p8_11,p9_11,p10_11,p11_11,p12_11,p13_11,p14_11,p15_11,p16_11,p17_11,p18_11,p19_11,p20_11,diagonal11,referencial11,
p0_12,p1_12,p2_12,p3_12,p4_12,p5_12,p6_12,p7_12,p8_12,p9_12,p10_12,p11_12,p12_12,p13_12,p14_12,p15_12,p16_12,p17_12,p18_12,p19_12,p20_12,diagonal12,referencial12,
p0_13,p1_13,p2_13,p3_13,p4_13,p5_13,p6_13,p7_13,p8_13,p9_13,p10_13,p11_13,p12_13,p13_13,p14_13,p15_13,p16_13,p17_13,p18_13,p19_13,p20_13,diagonal13,referencial13,
p0_14,p1_14,p2_14,p3_14,p4_14,p5_14,p6_14,p7_14,p8_14,p9_14,p10_14,p11_14,p12_14,p13_14,p14_14,p15_14,p16_14,p17_14,p18_14,p19_14,p20_14,diagonal14,referencial14,
p0_15,p1_15,p2_15,p3_15,p4_15,p5_15,p6_15,p7_15,p8_15,p9_15,p10_15,p11_15,p12_15,p13_15,p14_15,p15_15,p16_15,p17_15,p18_15,p19_15,p20_15,diagonal15,referencial15,
p0_16,p1_16,p2_16,p3_16,p4_16,p5_16,p6_16,p7_16,p8_16,p9_16,p10_16,p11_16,p12_16,p13_16,p14_16,p15_16,p16_16,p17_16,p18_16,p19_16,p20_16,diagonal16,referencial16,
p0_17,p1_17,p2_17,p3_17,p4_17,p5_17,p6_17,p7_17,p8_17,p9_17,p10_17,p11_17,p12_17,p13_17,p14_17,p15_17,p16_17,p17_17,p18_17,p19_17,p20_17,diagonal17,referencial17,
p0_18,p1_18,p2_18,p3_18,p4_18,p5_18,p6_18,p7_18,p8_18,p9_18,p10_18,p11_18,p12_18,p13_18,p14_18,p15_18,p16_18,p17_18,p18_18,p19_18,p20_18,diagonal18,referencial18,
p0_19,p1_19,p2_19,p3_19,p4_19,p5_19,p6_19,p7_19,p8_19,p9_19,p10_19,p11_19,p12_19,p13_19,p14_19,p15_19,p16_19,p17_19,p18_19,p19_19,p20_19,diagonal19,referencial19,
movimento

Onde:
p0 até p20 são os pontos da mão

time é o tempo em segundos desde o início da coleta

O arquivo de saída será um arquivo CSV com os dados de todos os movimentos
Exemplo de arquivo de saída:
movimento1/movimento1_01.csv
movimento1/movimento1_02.csv
movimento1/movimento1_03.csv
...
movimento2/movimento2_01.csv
movimento2/movimento2_02.csv
movimento2/movimento2_03.csv
...

Onde:
movimento1, movimento2, ... são os nomes dos movimentos
movimento1_01, movimento1_02, ... são os arquivos de cada movimento
movimento1_01.csv, movimento1_02.csv, ... são os arquivos CSV de cada movimento com os dados coletados

O arquivo CSV terá o seguinte formato:
p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, ..., p20_x, p20_y, reference_z, time
(1)
(2)
(3)
...
(20)

Onde:
p0_x, p0_y são as coordenadas x e y do ponto 0 da mão
p1_x, p1_y são as coordenadas x e y do ponto 1 da mão
...
p20_x, p20_y são as coordenadas x e y do ponto 20 da mão
reference_z é a coordenada z do ponto de referência da mão
time é o tempo em 3 em 3 segundos desde o início da coleta

O arquivo CSV será utilizado para treinar um modelo de machine learning
O modelo de machine learning será utilizado para reconhecer os movimentos da mão
O modelo de machine learning será utilizado para controlar o computador com os movimentos da mão, tendo alguns movimentos pré-definidos resultando em ações 

pré-definidas como:

- movimento1: não fazer nada (não reconhecer o movimento)
```python
    print('Nada')
```

- movimento2: Windows + E (mão reta para o lado direito)
```python
    pyautogui.hotkey('win', 'e')
```

- movimento3: Windows + D (tchau)
```python
pyautogui.hotkey('win', 'd')
```

- movimento4: Windows + S (estende a mão para cima)
```python
pyautogui.hotkey('win', 's')
```

- movimento5: aumentar o volume (dedo indicador para cima)
```python
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

current_volume = volume.GetMasterVolumeLevelScalar()
new_volume = min(1.0, current_volume + 0.1)
volume.SetMasterVolumeLevelScalar(new_volume, None)
```

- movimento6: diminuir o volume (dedo indicador para baixo)
```python
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

current_volume = volume.GetMasterVolumeLevelScalar()
new_volume = min(1.0, current_volume - 0.1)
volume.SetMasterVolumeLevelScalar(new_volume, None)
```

- movimento7: aumentar o brilho (pinça com os dedos indicador e polegar para cima)
```python
import wmi

def increase_brightness(delta):
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()[0]

    current_brightness = methods.WmiGetBrightness()
    new_brightness = min(current_brightness + delta, 100)  # Garantir que o brilho não ultrapasse 100

    methods.WmiSetBrightness(1, new_brightness)

# Aumentar o brilho atual em 10 unidades
increase_brightness(10)
```

- movimento8: diminuir o brilho (pinça com os dedos indicador e polegar para baixo)
```python
import wmi

def decrease_brightness(delta):
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()[0]

    current_brightness = methods.WmiGetBrightness()
    new_brightness = max(current_brightness - delta, 0)  # Garantir que o brilho não seja negativo

    methods.WmiSetBrightness(1, new_brightness)

# Diminuir o brilho atual em 10 unidades
decrease_brightness(10)
```

- movimento9:  ctrl + z (like para o lado esquerdo)
```python
pyautogui.hotkey('ctrl', 'z')
```

- movimento10: ctrl + y (like para o lado direito)
```python
pyautogui.hotkey('ctrl', 'y')
```

- movimento11: abrir/fechar o menu iniciar (mão com se estivesse segurando uma maçã girando)
```python
pyautogui.hotkey('win')
```

- movimento12: alt + f4 (dedos para o pulso menos o polegar)
```python
pyautogui.hotkey('alt', 'f4')
```
- movimento13: alt + tab (estralar os dedos indicador e médio)
```python
pyautogui.hotkey('alt', 'tab')
```

- movimento14: ctrl + shift + esc (mão reta para o lado esquerdo)
```python
pyautogui.hotkey('ctrl', 'shift', 'esc')
```

- movimento15: ctrl + shift + t (dedos do puslo para cima)
```python
pyautogui.hotkey('ctrl', 'shift', 't')
```

- movimento16: print screen (Abrir a mão)
```python
pyautogui.hotkey('win', 'prtsc')
pyautogui.hotkey('ctrl', 'a')
pyautogui.hotkey('ctrl', 'c')
```

- movimento17: Abrir a nagevação mouse (Z com o indicador)
```python
mouse.mouse_virtual()
```

- movimento18: confirmar ação (like)
```python
pyautogui.hotkey('enter')
```

- movimento19: f11 (V em libras para U em libras)
```python
pyautogui.hotkey('f11')
```

- movimento20: abrir o navegador (mão reta para cima)
```python
pyautogui.hotkey('win', 's')
pyautogui.typewrite('chrome')
pyautogui.hotkey('enter')
```

Proximas ações:

1. Add também um registro de nada

2. Script para popular o dataset com movimentos de erro

3. Arrumar o modo mouse (Ele tem que verificar a cada milissegundo  se houve uma alteração na posição dos dedos e ai sim dar um set += / Se tiver um diferença muito grande não muda nada)

4. Treinar ela com a posição do quadrado (Deixar relativo / As câmeras têm dimensões diferentes)

5. Add é mais movimentos

6. Outra coisa é fazer outro ativador de coleta do movimento (All time / Comando de voz)

7. Interface gráfica para o usuário descktop

8. Site informativo e para download

9. Criação de um vídeo de apresentação do projeto

10. Criação dos slides de apresentação do projeto

11. Criação do artigo científico
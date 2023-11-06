# Barium

Arquivo para fazer a coleta de dados e transformar em um dataset
Objetivo: Criar um dataset com os dados coletados através da webcam para treinar um modelo de machine learning

Colunas do dataset:
p0_0,p1_0,p2_0,p3_0,p4_0,p5_0,p6_0,p7_0,p8_0,p9_0,p10_0,p11_0,p12_0,p13_0,p14_0,p15_0,p16_0,p17_0,p18_0,p19_0,p20_0,diagonal0,referencial0,p0_1,p1_1,p2_1,p3_1,p4_1,p5_1,p6_1,p7_1,p8_1,p9_1,p10_1,p11_1,p12_1,p13_1,p14_1,p15_1,p16_1,p17_1,p18_1,p19_1,p20_1,diagonal1,referencial1 ... p0_19,p1_19,p2_19,p3_19,p4_19,p5_19,p6_19,p7_19,p8_19,p9_19,p10_19,p11_19,p12_19,p13_19,p14_19,p15_19,p16_19,p17_19,p18_19,p19_19,p20_19,diagonal19,referencial19,
movimento

Onde:
p0 até p20 são os pontos da mão

time é o tempo em segundos desde o início da coleta

O arquivo de saída será um arquivo CSV com os dados de todos os movimentos
Exemplo de arquivo de saída:

```csv
"(75, 95)","(87, 79)","(91, 55)","(90, 37)","(89, 23)","(59, 37)","(48, 18)","(40, 9)","(32, 3)","(46, 42)","(34, 23)","(26, 13)","(18, 6)","(38, 50)","(25, 34)","(18, 26)","(11, 19)","(32, 62)","(21, 50)","(14, 43)","(8, 36)","(280, 308)",384.66608896548183,"(42, 96)","(58, 85)","(70, 67)","(75, 53)","(79, 43)","(52, 43)","(51, 24)","(51, 14)","(50, 5)","(41, 42)","(40, 23)","(39, 12)","(39, 3)","(31, 45)","(29, 27)","(29, 16)","(29, 7)","(22, 52)","(20, 37)","(19, 28)","(20, 19)","(327, 326)",434.16356364854016," ... "(76, 95)","(88, 78)","(89, 56)","(87, 41)","(86, 29)","(56, 36)","(43, 20)","(33, 11)","(26, 3)","(47, 42)","(33, 25)","(25, 16)","(19, 8)","(39, 50)","(26, 34)","(18, 25)","(12, 17)","(32, 61)","(21, 47)","(15, 38)","(10, 30)","(277, 297)",377.59502115361636,0
```

Onde:
As linhas podem ser interpretadas como vídeos dos pontos da mão em movimento sendo que cada linha é 21 frames do vídeo (20 pontos da mão)

Onde:
p0_0 são as coordenadas x e y do ponto 0 da mão no frame 0
p1_0 são as coordenadas x e y do ponto 1 da mão no frame 0
...
p20_0 são as coordenadas x e y do ponto 20 da mão no frame 0

O arquivo CSV será utilizado para treinar um modelo de machine learning
O modelo de machine learning será utilizado para reconhecer os movimentos da mão
O modelo de machine learning será utilizado para controlar o computador com os movimentos da mão, tendo alguns movimentos pré-definidos resultando em ações

pré-definidas como:

- movimento1: não fazer nada (não reconhecer o movimento)

```python
    print('Nada')
```

- movimento2: Windows + E (mão reta para o lado direito) ✔

```python
    pyautogui.hotkey('win', 'e')
```

- movimento3: Windows + D (tchau) ✔

```python
pyautogui.hotkey('win', 'd')
```

- movimento4: Windows + S (estende a mão para cima) ✔

```python
pyautogui.hotkey('win', 's')
```

- movimento5: aumentar o volume (dedo indicador para cima) ✔

```python
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

current_volume = volume.GetMasterVolumeLevelScalar()
new_volume = min(1.0, current_volume + 0.1)
volume.SetMasterVolumeLevelScalar(new_volume, None)
```

- movimento6: diminuir o volume (dedo indicador para baixo) ✔

```python
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

current_volume = volume.GetMasterVolumeLevelScalar()
new_volume = min(1.0, current_volume - 0.1)
volume.SetMasterVolumeLevelScalar(new_volume, None)
```

- movimento7: aumentar o brilho (pinça com os dedos indicador e polegar para cima) ✔

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

- movimento8: diminuir o brilho (pinça com os dedos indicador e polegar para baixo) ✔

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

- movimento9:  ctrl + z (like para o lado esquerdo) ✔

```python
pyautogui.hotkey('ctrl', 'z')
```

- movimento10: ctrl + y (like para o lado direito) ✔

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

- movimento16: print screen (Abrir a mão) ✔

```python
pyautogui.hotkey('win', 'prtsc')
pyautogui.hotkey('ctrl', 'a')
pyautogui.hotkey('ctrl', 'c')
```

- movimento17: Abrir a nagevação mouse (Z com o indicador) ✔

```python
mouse.mouse_virtual()
```

- movimento18: confirmar ação (like) ✔

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
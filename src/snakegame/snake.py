import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Constantes
LARGURA, ALTURA = 400, 400
TAMANHO_GRADE = 20
LARGURA_GRADE, ALTURA_GRADE = LARGURA // TAMANHO_GRADE, ALTURA // TAMANHO_GRADE
FPS = 10

# Cores
CORES = {
    "preto": (0, 0, 0),
    "branco": (255, 255, 255),
    "verde": (0, 255, 0),
    "vermelho": (255, 0, 0),
    "azul": (0, 0, 255)
}

# Direções
CIMA = (0, -1)
BAIXO = (0, 1)
ESQUERDA = (-1, 0)
DIREITA = (1, 0)

icone_janela = pygame.image.load("LOGO.png")
pygame.display.set_icon(icone_janela)


# Inicializa a tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Barium Snake")

# Inicializa o relógio
relogio = pygame.time.Clock()

class Cobra:
    def __init__(self):
        self.corpo = [(LARGURA_GRADE // 2, ALTURA_GRADE // 2)]
        self.direcao = DIREITA

    def mover(self):
        cabeca = self.corpo[0]
        nova_cabeca = (cabeca[0] + self.direcao[0], cabeca[1] + self.direcao[1])
        self.corpo.insert(0, nova_cabeca)

    def crescer(self):
        calda = self.corpo[-1]
        nova_calda = (calda[0] - self.direcao[0], calda[1] - self.direcao[1])
        self.corpo.append(nova_calda)

    def verificar_colisao(self):
        cabeca = self.corpo[0]
        if (
            cabeca in self.corpo[1:] or
            cabeca[0] < 0 or cabeca[0] >= LARGURA_GRADE or
            cabeca[1] < 0 or cabeca[1] >= ALTURA_GRADE
        ):
            return True
        return False

class Comida:
    def __init__(self):
        self.posicao = self.randomizar_posicao()

    def randomizar_posicao(self):
        return (random.randint(0, LARGURA_GRADE - 1), random.randint(0, ALTURA_GRADE - 1))

    def desenhar(self):
        pygame.draw.rect(
            tela, CORES["verde"], 
            (self.posicao[0] * TAMANHO_GRADE, self.posicao[1] * TAMANHO_GRADE, TAMANHO_GRADE, TAMANHO_GRADE)
        )

def reiniciar_jogo():
    global cobra, comida, pontuacao
    cobra = Cobra()
    comida = Comida()
    pontuacao = 0

cobra = Cobra()
comida = Comida()
pontuacao = 0

def main():
    global cobra, comida, pontuacao

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and cobra.direcao != BAIXO:
                    cobra.direcao = CIMA
                elif evento.key == pygame.K_DOWN and cobra.direcao != CIMA:
                    cobra.direcao = BAIXO
                elif evento.key == pygame.K_LEFT and cobra.direcao != DIREITA:
                    cobra.direcao = ESQUERDA
                elif evento.key == pygame.K_RIGHT and cobra.direcao != ESQUERDA:
                    cobra.direcao = DIREITA
                elif evento.key == pygame.K_r:
                    reiniciar_jogo()

        cobra.mover()
        if cobra.corpo[0] == comida.posicao:
            cobra.crescer()
            comida.posicao = comida.randomizar_posicao()
            pontuacao += 10

        if cobra.verificar_colisao():
            reiniciar_jogo()

        tela.fill(CORES["preto"])
        comida.desenhar()
        for segmento in cobra.corpo:
            pygame.draw.rect(
                tela, CORES["branco"], 
                (segmento[0] * TAMANHO_GRADE, segmento[1] * TAMANHO_GRADE, TAMANHO_GRADE, TAMANHO_GRADE)
            )

        desenhar_grade()

        fonte = pygame.font.Font(None, 36)
        texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, CORES["branco"])
        tela.blit(texto_pontuacao, (10, 10))

        fonte = pygame.font.Font(None, 36)
        texto_reiniciar = fonte.render('Pressione R para reiniciar', True, CORES["branco"])
        tela.blit(texto_reiniciar, (10, ALTURA - 40))

        pygame.display.flip()
        relogio.tick(FPS)

def desenhar_grade():
    for linha in range(1, LARGURA_GRADE):
        pygame.draw.line(tela, CORES["branco"], (linha * TAMANHO_GRADE, 0), (linha * TAMANHO_GRADE, ALTURA))
    for coluna in range(1, ALTURA_GRADE):
        pygame.draw.line(tela, CORES["branco"], (0, coluna * TAMANHO_GRADE), (LARGURA, coluna * TAMANHO_GRADE))

if __name__ == "__main__":
    main()

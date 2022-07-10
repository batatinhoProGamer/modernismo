import pygame
from pygame.locals import *
from random import randint

pygame.init()

class Carregar_texto():
    def __init__(self, conteudo, fonte, tamanho, posição_x, posição_y, cor_fundo=None, italico=True, cor_texto=(20, 20, 20)):
        self.fonte_texto = pygame.font.SysFont(fonte, tamanho, True, italico)
        self.texto_formatado = self.fonte_texto.render(conteudo, True, cor_texto, cor_fundo)
        self.coordenadas = self.texto_formatado.get_rect()
        self.largura = tuple(self.coordenadas)[2]
        self.altura = tuple(self.coordenadas)[3]
        self.valor_fade = 0
        self.rect = self.texto_formatado.get_rect()
        self.posição_x = posição_x
        self.posição_y = posição_y
        self.rect.topleft = (posição_x - self.largura // 2, posição_y)
        self.escurecer = False

    def clarear(self):
        self.fade = self.texto_formatado.set_alpha(255)
        self.valor_fade = 255

    def centralizar(self):
        self.rect.topleft = (self.posição_x - self.largura // 2, self.posição_y - self.altura // 2)
    
    def fade_in_out(self, fade_, valor=1.5):
        if fade_:
            self.valor_fade += valor
        else:
            self.valor_fade -= valor
        self.fade = self.texto_formatado.set_alpha(int(self.valor_fade))


class Carregar_imagem(pygame.sprite.Sprite):
    def __init__(self, imagem, posição_x, posição_y, tamanho_original=False, tamanho_tela=False, ajuste=[0, 0]):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/" + imagem + ".png").convert_alpha()
        self.posição_x = posição_x
        self.posição_y = posição_y
        self.valor_fade = 0
        self.rect = self.image.get_rect()
        self.largura = tuple(self.rect)[2]
        self.altura = tuple(self.rect)[3]
        self.ajuste = ajuste
        self.escurecer = False

        if tamanho_tela != False:
            self.image = pygame.transform.scale(self.image, (tamanho_original[0] / tamanho_original[1] * tamanho_tela // 1, tamanho_tela))
            self.rect.topleft = (tamanho_tela // 2 - tamanho_original[0] / tamanho_original[1] * tamanho_tela // 2, posição_y)
        else:
            self.rect.topleft = (posição_x, posição_y)
        
    def clarear(self):
        self.fade = self.image.set_alpha(255)
        self.valor_fade = 255

    def fade_in_out(self, fade_, valor=1):
        if fade_:
            self.valor_fade += valor
        else:
            self.valor_fade -= valor
        self.fade = self.image.set_alpha(int(self.valor_fade))

    def escala(self, tamanho_a_aumentar):
        self.fade = self.image.set_alpha(255)
        self.image = pygame.transform.scale(self.image, (tamanho_a_aumentar[0], tamanho_a_aumentar[1]))
        self.largura = tamanho_a_aumentar[0]
        self.altura = tamanho_a_aumentar[1]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posição_x, self.posição_y)


class Carlos_drumond(pygame.sprite.Sprite):
    def __init__(self, sentido=0):
        pygame.sprite.Sprite.__init__(self)
        self.sentido = sentido
        self.sprites = [[], [], []]
        direções = ["frente", "esquerda", "costas"]
        self.posição = [-1, -1]
        self.vidas = 0
        self.pergaminho_pego = False
        for direção in range(0, 3):
            for c in range(0, 1):
                self.image = pygame.image.load("sprites/1_geracao/carlos_drumond_" + direções[direção] + "_" + str(c) + ".png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (40, 100))
                self.sprites[direção].append(self.image)
        self.image = self.sprites[self.sentido][0]
    
    def update(self):
        self.image = self.sprites[self.sentido][0]
        self.posição = self.posição


class Botão(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, tamanho):
        pygame.sprite.Sprite.__init__(self)

        self.tamanho = tamanho
        self.image = pygame.image.load("sprites/" + str(imagem) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pass


class Carregar_dialogo():
    def __init__(self, imagem):
        pygame.sprite.Sprite.__init__(self)
        self.atual = 0
        self.quantidade = len(imagem)
        self.dialogos = []
        self.quadrado_largura = []
        self.quadrado_altura = []
        for c in range(0, len(imagem)):
            im = pygame.image.load("dialogos/" + imagem[c] + ".png").convert_alpha()
            self.dialogos.append(im)
        self.image = self.dialogos[0]
        self.valor_fade = 0
        self.rect = self.image.get_rect()
        self.largura = tuple(self.rect)[2]
        self.altura = tuple(self.rect)[3]
        self.escurecer = False

    def clarear(self):
        self.fade = self.image.set_alpha(255)
        self.valor_fade = 255

    def fade_in_out(self, fade_, valor=1):
        if fade_:
            self.valor_fade += valor
        else:
            self.valor_fade -= valor
        self.fade = self.image.set_alpha(int(self.valor_fade))


class Passaro():
    def __init__(self, altura_tela):
        pygame.sprite.Sprite.__init__(self)
        self.valor_fade = 255
        self.vidas = 5
        self.atual = 0
        self.imagens =[]
        for c in range(0, 3):
            imagem = pygame.image.load("sprites/pos_modernismo/passaro_" + str(c) + ".png").convert_alpha()
            imagem = pygame.transform.scale(imagem, (150, 150))
            imagem = pygame.transform.flip(imagem, True, False)
            self.imagens.append(imagem)
        
        self.image = self.imagens[self.atual]
        tamanho = altura_tela // 200 * 200
        self.posições = [(altura_tela - tamanho) // 2, altura_tela // 2 - 75, (altura_tela + tamanho) // 2 - 150]
        self.posição_atual = 1
        self.posição = self.posições[self.posição_atual]

    def trocar_posição(self, posição):
        self.posição_atual = posição
        self.posição = self.posições[self.posição_atual]

    def trocar_cor(self):
        cor = randint(0, 2)
        self.atual = cor
        self.image = self.imagens[self.atual]

    def fade_out(self, valor):
        self.valor_fade -= valor
        for c in range(0, 3):
            self.imagens[c].set_alpha(int(self.valor_fade))
    

class Bloco():
    def __init__(self, largura_tela, cores=[]):
        pygame.sprite.Sprite.__init__(self)
        self.valor_fade = 255
        self.cor_atual = 0
        self.cores = []
        for c in range(0, 3):
            imagem = pygame.image.load("sprites/pos_modernismo/cor_" + str(c) + ".png").convert_alpha()
            imagem = pygame.transform.scale(imagem, (150, 150))
            self.cores.append(imagem)

        self.tamanho = 150
        self.original = False
        self.posições = []
        self.lugares = []
        lugares = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18, 20, 21, 22, 23, 25, 26, 27, 28]
        for c in range(1, 4):
            for t in range(0, 24):
                lugares.append(lugares[t] + 30 * c)
        self.blocos_cores = cores
        for c in range(0, len(lugares)):
            self.lugares.append((largura_tela - 550 + lugares[c] * 74 * 8) / (74 / 8) // 1)
            self.posições.append(-150)

    def trocar_cor(self, cor):
        self.cor_atual = cor
        self.image = self.cores[self.cor_atual]

    def esticar(self, tamanho):
        self.image = pygame.transform.scale(self.image, (150, tamanho))
        self.tamanho = tamanho

    def fade_out(self, valor):
        self.valor_fade -= valor
        for c in range(0, 3):
            self.cores[c].set_alpha(int(self.valor_fade))
    

class Carlos_animação():
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.atual = 0
        self.posição_x = 0
        self.imagens = []
        for c in range(0, 5):
            imagem = pygame.image.load("sprites/pos_modernismo/carlos_animação_" + str(c) + ".png").convert_alpha()
            imagem = pygame.transform.scale(imagem, (110, 110))
            self.imagens.append(imagem)

        self.costas = pygame.image.load("sprites/pos_modernismo/carlos_animação_costas.png").convert_alpha()
        self.costas = pygame.transform.scale(self.costas, (110, 110))
        self.image = self.imagens[self.atual]
    
    def update(self):
        self.atual += 0.1
        if self.atual >= 5:
            self.atual = 0
        self.image = self.imagens[int(self.atual)]
        
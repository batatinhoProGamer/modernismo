import pygame
from pygame.locals import *
from sys import exit
from classes import *
from time import sleep
from random import randint

pygame.init()

info = pygame.display.Info()
largura_tela = info.current_w
altura_tela = info.current_h
janela = pygame.display.set_mode((largura_tela, altura_tela))
relogio = pygame.time.Clock()
pygame.display.set_caption("NO MEIO DO CAMINHO")
icone_tela_imagem = pygame.image.load("sprites/icone_tela.png").convert_alpha()
pygame.display.set_icon(icone_tela_imagem)

# especificações gerais
fim_do_final = False
final = False
menu_inicio = False
fade_janela = 0
poema_atual = 0
final_jogo = False
voltar = False
click = False
fps = 74
fonte_vidas = pygame.font.SysFont("04b", 100, True, False)

# especificações
tela_atual = "menu"
imagem_fundo_menu = Carregar_imagem("menu/fundo_menu", largura_tela // 2, 0, [1920, 1080], largura_tela)
imagem_fundo_menu.escala([largura_tela, altura_tela])
titulo_menu = Carregar_texto("NO MEIO DO CAMINHO", "04b", 100, largura_tela // 2, 20)
botão_jogar_menu = Carregar_texto("JOGAR", "04b", 80, largura_tela // 2, altura_tela // 2 - 150, (123, 123, 123), False)
botão_configurações_menu = Carregar_texto("CONFIGURAÇÕES", "04b", 80, largura_tela // 2, altura_tela // 2 - 50, (123, 123, 123), False)
botão_sair_menu = Carregar_texto("SAIR", "04b", 80, largura_tela // 2, altura_tela // 2 + 70, (123, 123, 123), False)
imagem_mouse = Carregar_imagem("menu/mouse", 0, 0)
imagem_mouse.escala([150, 150])

# audios
volume = 1
audio_andar = pygame.mixer.Sound("audios/efeitos/andar.wav")
audio_andar.set_volume(volume * 0.6)

audio_abre_folha = pygame.mixer.Sound("audios/efeitos/abre_folha.wav")
audio_abre_folha.set_volume(volume)

audio_fecha_folha = pygame.mixer.Sound("audios/efeitos/fecha_folha.wav")
audio_fecha_folha.set_volume(volume)

audio_select = pygame.mixer.Sound("audios/efeitos/select.wav")
audio_select.set_volume(volume)

audio_erro = pygame.mixer.Sound("audios/efeitos/combobreak.wav")
audio_erro.set_volume(0.1 * volume)

audio_fade_in = pygame.mixer.Sound("audios/efeitos/fade_in.wav")
audio_fade_in.set_volume(volume)

# tela configurações
posição_bolinha = volume * 500
imagem_audio = Carregar_imagem("menu/audio_imagem", 0, 0)
imagem_audio.escala([100, 100])

# pré-modernismo
fase_atual = 0
carlos_drumond = Carlos_drumond(0)
pedra = Carregar_imagem("pre_modernismo/caveira", 0, 0)
pedra.escala([54, 54])
mesa = Carregar_imagem("pre_modernismo/tumulo", 0, 0)
mesa.escala([100, 100])

seta_pos = -10
seta_mov = 1
seta = Carregar_imagem("menu/seta", 0, 0)
seta.escala([74, 74])

botão_restart = Botão("menu/botão_restart", largura_tela - 100, 0, 100)
fundo = Carregar_imagem("pre_modernismo/cemiterio", 0, 0)
fundo.escala([768, 768])

altura_pergaminho = -15
movimento_pergaminho = 0.5
pergaminho = Carregar_imagem("menu/pergaminho", 0, 0)
pergaminho.escala([60, 60])

# pos modernismo / fase final
velocidade_blocos = 8
timing = 0
tamanho_final = altura_tela // 200 * 200
passaro = Passaro(altura_tela)

# textos história
texto_inicial = Carregar_dialogo(["dialogo_inicial", "dialogo_inicial2", "dialogo_inicial3", "dialogo_inicial4", "dialogo_inicial5"])

texto_pré_1 = Carregar_dialogo(["dialogo_pre_1", "dialogo_pre_12"])

texto_1_2 = Carregar_dialogo(["dialogo_1_2", "dialogo_1_22"])

texto_2_pos = Carregar_dialogo(["dialogo_2_pos", "dialogo_2_pos2", "dialogo_2_pos3", "dialogo_2_pos4", "dialogo_2_pos5", "dialogo_2_pos6"])

# poemas
poema1 = Carregar_imagem("poemas/poema_0", 0, 0)
poema1.escala([altura_tela, altura_tela])

poema2 = Carregar_imagem("poemas/poema_1", 0, 0)
poema2.escala([altura_tela, altura_tela])

poema3 = Carregar_imagem("poemas/poema_2", 0, 0)
poema3.escala([altura_tela, altura_tela])

poema4 = Carregar_imagem("poemas/poema_3", 0, 0)
poema4.escala([altura_tela, altura_tela])

poema5 = Carregar_imagem("poemas/poema_4", 0, 0)
poema5.escala([altura_tela, altura_tela])

poema6 = Carregar_imagem("poemas/poema_5", 0, 0)
poema6.escala([altura_tela, altura_tela])

poema7 = Carregar_imagem("poemas/poema_6", 0, 0)
poema7.escala([altura_tela, altura_tela])

poema8 = Carregar_imagem("poemas/poema_7", 0, 0)
poema8.escala([altura_tela, altura_tela])

poema9 = Carregar_imagem("poemas/poema_8", 0, 0)
poema9.escala([altura_tela, altura_tela])

todos_poemas = [poema1, poema2, poema3, poema4, poema5, poema6, poema7, poema8, poema9]

# C = Carlos
# P = Pedra / objeto movim.
# M = Mesa / objeto fixo
# S = Seta / proxima fase
# R = poema / chave
fase1 = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["C"], [" "], ["P"], [" "], ["M"], [" "], [" "], [" "]],
         [["M"], ["M"], ["P"], ["M"], ["M"], ["M"], ["M"], [" "]],
         [[" "], ["M"], [" "], ["P"], [" "], [" "], [" "], ["M"]],
         [[" "], ["M"], [" "], [" "], ["M"], ["P"], ["M"], [" "]],
         [["M"], ["R"], [" "], ["P"], [" "], [" "], ["P"], [" "]],
         [[" "], ["M"], ["M"], [" "], [" "], [" "], [" "], ["S"]]]

fase2 = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["M"], ["M"], ["R"], [" "], ["P"], ["M"], ["M"], ["M"]],
         [["M"], [" "], ["P"], [" "], ["M"], ["M"], [" "], ["M"]],
         [["M"], ["P"], ["P"], [" "], [" "], ["M"], [" "], ["S"]],
         [["M"], [" "], [" "], ["M"], ["M"], ["M"], [" "], ["M"]],
         [["C"], ["P"], [" "], ["P"], [" "], [" "], ["P"], ["M"]],
         [["M"], ["M"], [" "], ["P"], [" "], ["P"], [" "], [" "]]]

fase3 = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["M"], ["M"], ["M"], ["M"], [" "], [" "], [" "], ["S"]],
         [["M"], ["M"], ["P"], [" "], [" "], ["M"], ["M"], ["M"]],
         [["P"], ["M"], ["P"], [" "], [" "], ["M"], [" "], ["M"]],
         [[" "], [" "], ["P"], ["P"], ["P"], [" "], [" "], ["R"]],
         [["P"], ["P"], ["P"], [" "], [" "], ["P"], ["P"], [" "]],
         [["C"], [" "], ["P"], [" "], [" "], ["P"], [" "], ["M"]]]

fase4 = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["C"], ["M"], ["P"], [" "], ["R"], ["M"], ["M"], ["M"]],
         [[" "], ["P"], [" "], [" "], ["P"], [" "], ["P"], [" "]],
         [["P"], [" "], ["P"], ["P"], ["P"], ["P"], [" "], [" "]],
         [[" "], ["P"], [" "], ["P"], [" "], ["P"], ["M"], [" "]],
         [["M"], [" "], ["P"], [" "], [" "], ["S"], [" "], ["M"]]]

fase5 = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["M"], ["R"], ["P"], [" "], ["M"], ["M"], [" "], ["M"]],
         [[" "], [" "], [" "], [" "], [" "], ["P"], ["P"], ["M"]],
         [[" "], ["P"], [" "], ["P"], ["M"], ["M"], [" "], [" "]],
         [[" "], [" "], ["P"], [" "], ["P"], [" "], ["P"], ["P"]],
         [[" "], ["M"], [" "], [" "], [" "], ["S"], ["M"], ["C"]]]

fase6 = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["M"], [" "], ["M"], ["M"], ["M"], ["M"], [" "], [" "]],
         [[" "], [" "], ["P"], [" "], ["P"], [" "], ["M"], [" "]],
         [[" "], ["P"], ["P"], ["C"], ["P"], [" "], [" "], ["M"]],
         [["M"], [" "], [" "], ["P"], [" "], ["M"], ["P"], [" "]],
         [["M"], [" "], [" "], [" "], [" "], ["S"], [" "], ["R"]]]

fase7 = [[["P"], ["M"], [" "], ["C"], [" "], ["M"], ["M"], ["P"]],
         [["M"], ["M"], ["P"], ["P"], ["P"], ["M"], ["P"], ["P"]],
         [["M"], [" "], [" "], [" "], ["R"], ["M"], ["M"], ["M"]],
         [["M"], ["M"], [" "], ["P"], [" "], [" "], ["M"], ["M"]],
         [["P"], ["M"], [" "], ["M"], ["P"], ["P"], [" "], [" "]],
         [["M"], ["P"], [" "], ["M"], [" "], [" "], [" "], ["M"]],
         [["P"], ["M"], ["M"], ["M"], ["M"], ["P"], ["P"], [" "]],
         [["P"], ["P"], ["M"], ["P"], ["M"], [" "], [" "], ["S"]]]

fase8 = [[["M"], ["M"], [" "], ["M"], ["M"], ["M"], ["M"], ["M"]],
         [["M"], ["M"], [" "], [" "], ["P"], [" "], ["M"], ["M"]],
         [["M"], ["M"], ["P"], ["M"], [" "], [" "], [" "], [" "]],
         [["M"], ["M"], [" "], ["M"], ["M"], ["P"], ["P"], ["P"]],
         [["M"], [" "], [" "], ["M"], ["M"], [" "], [" "], [" "]],
         [["C"], ["P"], [" "], ["M"], ["M"], [" "], ["M"], [" "]],
         [["M"], ["P"], ["R"], ["M"], ["M"], ["P"], [" "], ["M"]],
         [["M"], [" "], ["M"], ["M"], ["M"], [" "], [" "], ["S"]]]

fase9 = [[[" "], ["M"], ["M"], [" "], [" "], ["M"], [" "], ["S"]],
         [["M"], [" "], ["M"], [" "], ["P"], [" "], [" "], [" "]],
         [[" "], ["M"], ["M"], ["P"], [" "], ["M"], [" "], ["M"]],
         [["M"], [" "], [" "], ["P"], ["P"], ["M"], ["M"], [" "]],
         [[" "], ["M"], ["R"], ["M"], [" "], ["P"], [" "], ["M"]],
         [["P"], [" "], ["M"], [" "], [" "], ["M"], ["P"], ["S"]],
         [["C"], ["P"], [" "], ["P"], [" "], [" "], ["P"], [" "]],
         [["M"], [" "], ["M"], ["M"], [" "], ["M"], ["M"], ["M"]]]


fases = [fase1, fase2, fase3, fase4, fase5, fase6, fase7, fase8, fase9]
vidas = [21,    35,    34,    23,    27,    30,    19,    33,    31   ]


def jogo_principal(fase):
    # vidas
    texto_vidas = fonte_vidas.render(str(carlos_drumond.vidas), True, (255, 255, 255))
    janela.blit(texto_vidas, (0, altura_tela - 100))

    fase_escolhida = fases[fase]
    janela.blit(fundo.image, ((largura_tela - fundo.largura) // 2 + fundo.ajuste[0], (altura_tela - fundo.altura) // 2 + fundo.ajuste[1]))
    # botão
    janela.blit(botão_restart.image, (botão_restart.rect.x, botão_restart.rect.y))
    for linha in range(0, 8):
        for coluna in range(0, 8):
            if fase_escolhida[linha][coluna][0] == "C":
                janela.blit(carlos_drumond.image, ((largura_tela - 592) // 2 + 15 + 74 * coluna, (altura_tela - 592) // 2 - 45 + 74 * linha))
                carlos_drumond.posição = [linha, coluna]

            elif fase_escolhida[linha][coluna][0] == "P":
                janela.blit(pedra.image, ((largura_tela - 592) // 2 + 10 + 74 * coluna + pedra.ajuste[0], (altura_tela - 592) // 2 + 15 + 74 * linha + pedra.ajuste[1]))

            elif fase_escolhida[linha][coluna][0] == "M":
                janela.blit(mesa.image, ((largura_tela - 592) // 2 - (mesa.largura - 74) // 2 + 74 * coluna + mesa.ajuste[0], (altura_tela - 592) // 2 - 20 + 74 * linha + mesa.ajuste[1]))
            
            elif fase_escolhida[linha][coluna][0] == "S":
                janela.blit(seta.image, (seta_pos + (largura_tela - 592) // 2 + 74 * coluna + seta.ajuste[0], (altura_tela - 592) // 2 + 74 * linha + seta.ajuste[1]))

            elif fase_escolhida[linha][coluna][0] == "R":
                janela.blit(pergaminho.image, ((largura_tela - 592) // 2 + 10 + 74 * coluna + pergaminho.ajuste[0], altura_pergaminho + (altura_tela - 592) // 2 + 74 * linha + pergaminho.ajuste[1]))


def mover_carlos(sentido):
    # horizontal
    if sentido[0] != 0:
        # direita
        if sentido[0] == 1 and carlos_drumond.posição[1] < 7:
            if fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] + 1][0] == " " or fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] + 1][0] == "R":
                if fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] + 1][0] == "R":
                    fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] + 1][0] = "C"
                    fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1]][0] = " "
                    carlos_drumond.posição[1] += 1
                    carlos_drumond.vidas -= 1
                    carlos_drumond.pergaminho_pego = True
                    audio_andar.play()
                    return "poema"
                fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] + 1][0] = "C"
                fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1]][0] = " "
                carlos_drumond.posição[1] += 1
                carlos_drumond.vidas -= 1
                audio_andar.play()
                return False

            elif fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] + 1][0] == "S" and carlos_drumond.pergaminho_pego:
                carlos_drumond.vidas = 0
                audio_andar.play()
                return True

            elif carlos_drumond.posição[1] < 6 and fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] + 1][0] == "P" and fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] + 2][0] == " ":
                fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] + 2][0] = "P"
                fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] + 1][0] = " "
                carlos_drumond.vidas -= 1
                audio_andar.play()
                return False
        
        # esquerda
        elif sentido[0] == -1 and carlos_drumond.posição[1] > 0:
            if fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] - 1][0] == " " or fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] - 1][0] == "R":
                if fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] - 1][0] == "R":
                    carlos_drumond.pergaminho_pego = True
                    fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] - 1][0] = "C"
                    fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1]][0] = " "
                    carlos_drumond.posição[1] -= 1
                    carlos_drumond.vidas -= 1
                    audio_andar.play()
                    return "poema"
                fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] - 1][0] = "C"
                fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1]][0] = " "
                carlos_drumond.posição[1] -= 1
                carlos_drumond.vidas -= 1
                audio_andar.play()
                return False

            elif carlos_drumond.posição[1] > 1 and fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] - 1][0] == "P" and fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] - 2][0] == " ":
                fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] - 2][0] = "P"
                fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1] - 1][0] = " "
                carlos_drumond.vidas -= 1
                audio_andar.play()
                return False

    # vertical
    elif sentido[1] != 0:
        # baixo
        if sentido[1] == 1 and carlos_drumond.posição[0] < 7:
            if fases[fase_atual][carlos_drumond.posição[0] + 1][carlos_drumond.posição[1]][0] == " " or fases[fase_atual][carlos_drumond.posição[0] + 1][carlos_drumond.posição[1]][0] == "R":
                if fases[fase_atual][carlos_drumond.posição[0] + 1][carlos_drumond.posição[1]][0] == "R":
                    carlos_drumond.pergaminho_pego = True
                    fases[fase_atual][carlos_drumond.posição[0] + 1][carlos_drumond.posição[1]][0] = "C"
                    fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1]][0] = " "
                    carlos_drumond.posição[0] += 1
                    carlos_drumond.vidas -= 1
                    audio_andar.play()
                    return "poema"
                fases[fase_atual][carlos_drumond.posição[0] + 1][carlos_drumond.posição[1]][0] = "C"
                fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1]][0] = " "
                carlos_drumond.posição[0] += 1
                carlos_drumond.vidas -= 1
                audio_andar.play()
                return False

            elif carlos_drumond.posição[0] < 6 and fases[fase_atual][carlos_drumond.posição[0] + 1][carlos_drumond.posição[1]][0] == "P" and fases[fase_atual][carlos_drumond.posição[0] + 2][carlos_drumond.posição[1]][0] == " ":
                fases[fase_atual][carlos_drumond.posição[0] + 2][carlos_drumond.posição[1]][0] = "P"
                fases[fase_atual][carlos_drumond.posição[0] + 1][carlos_drumond.posição[1]][0] = " "
                carlos_drumond.vidas -= 1
                audio_andar.play()
                return False
        
        # cima
        elif sentido[1] == -1 and carlos_drumond.posição[0] > 0:
            if fases[fase_atual][carlos_drumond.posição[0] - 1][carlos_drumond.posição[1]][0] == " " or fases[fase_atual][carlos_drumond.posição[0] - 1][carlos_drumond.posição[1]][0] == "R":
                if fases[fase_atual][carlos_drumond.posição[0] - 1][carlos_drumond.posição[1]][0] == "R":
                    carlos_drumond.pergaminho_pego = True
                    fases[fase_atual][carlos_drumond.posição[0] - 1][carlos_drumond.posição[1]][0] = "C"
                    fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1]][0] = " "
                    carlos_drumond.posição[0] -= 1
                    carlos_drumond.vidas -= 1
                    audio_andar.play()
                    return "poema"
                fases[fase_atual][carlos_drumond.posição[0] - 1][carlos_drumond.posição[1]][0] = "C"
                fases[fase_atual][carlos_drumond.posição[0]][carlos_drumond.posição[1]][0] = " "
                carlos_drumond.posição[0] -= 1
                carlos_drumond.vidas -= 1
                audio_andar.play()
                return False

            elif carlos_drumond.posição[0] > 1 and fases[fase_atual][carlos_drumond.posição[0] - 1][carlos_drumond.posição[1]][0] == "P" and fases[fase_atual][carlos_drumond.posição[0] - 2][carlos_drumond.posição[1]][0] == " ":
                fases[fase_atual][carlos_drumond.posição[0] - 2][carlos_drumond.posição[1]][0] = "P"
                fases[fase_atual][carlos_drumond.posição[0] - 1][carlos_drumond.posição[1]][0] = " "
                carlos_drumond.vidas -= 1
                audio_andar.play()
                return False
        else:
            return False


def restart():
    carlos_drumond.pergaminho_pego = False
    carlos_drumond.vidas = 0
    if fase_atual == 0:
        fases[fase_atual] = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["C"], [" "], ["P"], [" "], ["M"], [" "], [" "], [" "]],
         [["M"], ["M"], ["P"], ["M"], ["M"], ["M"], ["M"], [" "]],
         [[" "], ["M"], [" "], ["P"], [" "], [" "], [" "], ["M"]],
         [[" "], ["M"], [" "], [" "], ["M"], ["P"], ["M"], [" "]],
         [["M"], ["R"], [" "], ["P"], [" "], [" "], ["P"], [" "]],
         [[" "], ["M"], ["M"], [" "], [" "], [" "], [" "], ["S"]]]

    elif fase_atual == 1:
        fases[fase_atual] = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["M"], ["M"], ["R"], [" "], ["P"], ["M"], ["M"], ["M"]],
         [["M"], [" "], ["P"], [" "], ["M"], ["M"], [" "], ["M"]],
         [["M"], ["P"], ["P"], [" "], [" "], ["M"], [" "], ["S"]],
         [["M"], [" "], [" "], ["M"], ["M"], ["M"], [" "], ["M"]],
         [["C"], ["P"], [" "], ["P"], [" "], [" "], ["P"], ["M"]],
         [["M"], ["M"], [" "], ["P"], [" "], ["P"], [" "], [" "]]]

    elif fase_atual == 2:
        fases[fase_atual] = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["M"], ["M"], ["M"], ["M"], [" "], [" "], [" "], ["S"]],
         [["M"], ["M"], ["P"], [" "], [" "], ["M"], ["M"], ["M"]],
         [["P"], ["M"], ["P"], [" "], [" "], ["M"], [" "], ["M"]],
         [[" "], [" "], ["P"], ["P"], ["P"], [" "], [" "], ["R"]],
         [["P"], ["P"], ["P"], [" "], [" "], ["P"], ["P"], [" "]],
         [["C"], [" "], ["P"], [" "], [" "], ["P"], [" "], ["M"]]]
    
    elif fase_atual == 3:
        fases[fase_atual] = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["C"], ["M"], ["P"], [" "], ["R"], ["M"], ["M"], ["M"]],
         [[" "], ["P"], [" "], [" "], ["P"], [" "], ["P"], [" "]],
         [["P"], [" "], ["P"], ["P"], ["P"], ["P"], [" "], [" "]],
         [[" "], ["P"], [" "], ["P"], [" "], ["P"], ["M"], [" "]],
         [["M"], [" "], ["P"], [" "], [" "], ["S"], [" "], ["M"]]]
    
    elif fase_atual == 4:
        fases[fase_atual] = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["M"], ["R"], ["P"], [" "], ["M"], ["M"], [" "], ["M"]],
         [[" "], [" "], [" "], [" "], [" "], ["P"], ["P"], ["M"]],
         [[" "], ["P"], [" "], ["P"], ["M"], ["M"], [" "], [" "]],
         [[" "], [" "], ["P"], [" "], ["P"], [" "], ["P"], ["P"]],
         [[" "], ["M"], [" "], [" "], [" "], ["S"], ["M"], ["C"]]]
    
    elif fase_atual == 5:
        fases[fase_atual] = [[["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"], ["V"]],
         [["M"], [" "], ["M"], ["M"], ["M"], ["M"], [" "], [" "]],
         [[" "], [" "], ["P"], [" "], ["P"], [" "], ["M"], [" "]],
         [[" "], ["P"], ["P"], ["C"], ["P"], [" "], [" "], ["M"]],
         [["M"], [" "], [" "], ["P"], [" "], ["M"], ["P"], [" "]],
         [["M"], [" "], [" "], [" "], [" "], ["S"], [" "], ["R"]]]
    
    elif fase_atual == 6:
        fases[fase_atual] = [[["P"], ["M"], [" "], ["C"], [" "], ["M"], ["M"], ["P"]],
         [["M"], ["M"], ["P"], ["P"], ["P"], ["M"], ["P"], ["P"]],
         [["M"], [" "], [" "], [" "], ["R"], ["M"], ["M"], ["M"]],
         [["M"], ["M"], [" "], ["P"], [" "], [" "], ["M"], ["M"]],
         [["P"], ["M"], [" "], ["M"], ["P"], ["P"], [" "], [" "]],
         [["M"], ["P"], [" "], ["M"], [" "], [" "], [" "], ["M"]],
         [["P"], ["M"], ["M"], ["M"], ["M"], ["P"], ["P"], [" "]],
         [["P"], ["P"], ["M"], ["P"], ["M"], [" "], [" "], ["S"]]]
    
    elif fase_atual == 7:
        fases[fase_atual] = [[["M"], ["M"], [" "], ["M"], ["M"], ["M"], ["M"], ["M"]],
         [["M"], ["M"], [" "], [" "], ["P"], [" "], ["M"], ["M"]],
         [["M"], ["M"], ["P"], ["M"], [" "], [" "], [" "], [" "]],
         [["M"], ["M"], [" "], ["M"], ["M"], ["P"], ["P"], ["P"]],
         [["M"], [" "], [" "], ["M"], ["M"], [" "], [" "], [" "]],
         [["C"], ["P"], [" "], ["M"], ["M"], [" "], ["M"], [" "]],
         [["M"], ["P"], ["R"], ["M"], ["M"], ["P"], [" "], ["M"]],
         [["M"], [" "], ["M"], ["M"], ["M"], [" "], [" "], ["S"]]]
    
    elif fase_atual == 8:
        fases[fase_atual] = [[[" "], ["M"], ["M"], [" "], [" "], ["M"], [" "], ["S"]],
         [["M"], [" "], ["M"], [" "], ["P"], [" "], [" "], [" "]],
         [[" "], ["M"], ["M"], ["P"], [" "], ["M"], [" "], ["M"]],
         [["M"], [" "], [" "], ["P"], ["P"], ["M"], ["M"], [" "]],
         [[" "], ["M"], ["R"], ["M"], [" "], ["P"], [" "], ["M"]],
         [["P"], [" "], ["M"], [" "], [" "], ["M"], ["P"], ["S"]],
         [["C"], ["P"], [" "], ["P"], [" "], [" "], ["P"], [" "]],
         [["M"], [" "], ["M"], ["M"], [" "], ["M"], ["M"], ["M"]]]
    

def mensagem(objeto, tela, nome=""):
    if objeto.valor_fade < 255 and not objeto.escurecer:
        objeto.fade_in_out(True, 3)
    if objeto.valor_fade >= 255 and click:
        audio_select.play()
        objeto.escurecer = True
    if objeto.escurecer:
        objeto.fade_in_out(False, 5)
    if nome == "" or objeto.atual != 3:
        janela.blit(objeto.image, ((largura_tela - objeto.largura) // 2, (altura_tela - objeto.altura) // 2))
    elif objeto.atual == 3:
        janela.blit(objeto.image, ((largura_tela - 900) // 2, (altura_tela - 675) // 2))
    janela.blit(imagem_mouse.image, (-10, 20))
    if objeto.valor_fade <= 0 and objeto.escurecer:
        if objeto.atual == objeto.quantidade - 1:
            if final:
                return "pos_modernismo"
            else:
                return "jogo"
        else:
            objeto.atual += 1
            objeto.image = objeto.dialogos[objeto.atual]
            objeto.escurecer = False
            objeto.valor_fade = 0
            return tela
    else:
        return tela


while True:
    relogio.tick(fps)
    janela.fill((0, 0, 0))
    posição_mouse = pygame.mouse.get_pos()

    proxima_fase = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == MOUSEBUTTONDOWN:
            click = True

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                voltar = True
            if tela_atual == "jogo":
                if event.key == K_s or event.key == K_DOWN:
                    carlos_drumond.sentido = 0
                    proxima_fase = mover_carlos([0, 1])
                
                elif event.key == K_d or event.key == K_RIGHT:
                    carlos_drumond.sentido = 0
                    proxima_fase = mover_carlos([1, 0])
                
                elif event.key == K_a or event.key == K_LEFT:
                    carlos_drumond.sentido = 1
                    proxima_fase = mover_carlos([-1, 0])
                
                elif event.key == K_w or event.key == K_UP:
                    carlos_drumond.sentido = 2
                    proxima_fase = mover_carlos([0, -1])

                if carlos_drumond.vidas == 0:
                    restart()
                
                if proxima_fase == True:
                    carlos_drumond.pergaminho_pego = False
                    poema_atual = 0
                    if fase_atual < 12:
                        fase_atual += 1
                        if str(fase_atual) in "369":
                            if fase_atual == 9:
                                final = True
                            tela_atual = "inicio"
                        else:
                            tela_atual = "entre_fases"
                    else:
                        final_jogo = True
                    # mudança de paisagem 
                    # 1 geração
                    if fase_atual == 3:
                        fundo = Carregar_imagem("1_geracao/sala_preparatoria", 0, 0, False, False, [0, -30])
                        fundo.escala([700, 700])
                        pedra = Carregar_imagem("1_geracao/pedra", 0, 0, False, False, [-4, -4])
                        pedra.escala([60, 60])
                        mesa = Carregar_imagem("1_geracao/pintura", 0, 0, False, False, [0, -30])
                        mesa.escala([120, 120])
                        carlos_drumond.vidas = vidas[fase_atual]
                    # 2 geração
                    elif fase_atual == 6:
                        fundo = Carregar_imagem("2_geracao/deserto", 0, 0, False, False, [0, 0])
                        fundo.escala([768, 768])
                        pedra = Carregar_imagem("2_geracao/feno", 0, 0, False, False, [-10, -20])
                        pedra.escala([70, 70])
                        mesa = Carregar_imagem("2_geracao/cacto", 0, 0, False, False, [0, -20])
                        mesa.escala([100, 100])
                        carlos_drumond.vidas = vidas[fase_atual]
                    # pos modernismo
                    elif fase_atual == 9:
                        tela_atual = "inicio"
                        pygame.mixer.music.stop()

                elif proxima_fase == "poema":
                    tela_atual = "poema"

                carlos_drumond.update()

            elif tela_atual == "pos_modernismo":
                if passaro.posição_atual > 0:
                    if event.key == K_UP or event.key == K_w:
                        passaro.trocar_posição(passaro.posição_atual - 1)
                
                if passaro.posição_atual < 2:
                    if event.key == K_DOWN or event.key == K_s:
                        passaro.trocar_posição(passaro.posição_atual + 1)

    if tela_atual == "menu":
        if not menu_inicio:
            pygame.mixer.music.stop()
            musica_menu = pygame.mixer.music.load("audios/musicas/musica_menu.mp3")
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            menu_inicio = True
            

        # fade in e fade out
        if imagem_fundo_menu.valor_fade < 255:
            imagem_fundo_menu.fade_in_out(True)
            titulo_menu.fade_in_out(True)
            botão_jogar_menu.fade_in_out(True)
            botão_configurações_menu.fade_in_out(True)
            botão_sair_menu.fade_in_out(True)
        
        if click:
            titulo_menu.clarear()
            imagem_fundo_menu.clarear()
            botão_jogar_menu.clarear()
            botão_configurações_menu.clarear()
            botão_sair_menu.clarear()

            if botão_jogar_menu.rect.collidepoint(posição_mouse):
                audio_select.play()
                menu_inicio = False
                pygame.mixer.music.stop()
                musica_jogo= pygame.mixer.music.load("audios/musicas/musica_jogo.mp3")
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                while imagem_fundo_menu.valor_fade > 0:
                    imagem_fundo_menu.fade_in_out(False, 5)
                    titulo_menu.fade_in_out(False, 5)
                    botão_jogar_menu.fade_in_out(False, 5)
                    botão_configurações_menu.fade_in_out(False, 5)
                    botão_sair_menu.fade_in_out(False, 5)

                    janela.blit(imagem_fundo_menu.image, (0, 0))
                    janela.blit(titulo_menu.texto_formatado, (titulo_menu.rect.x, titulo_menu.rect.y))

                    janela.blit(botão_jogar_menu.texto_formatado, (botão_jogar_menu.rect.x, botão_jogar_menu.rect.y))
                    janela.blit(botão_configurações_menu.texto_formatado, (botão_configurações_menu.rect.x, botão_configurações_menu.rect.y))
                    janela.blit(botão_sair_menu.texto_formatado, (botão_sair_menu.rect.x, botão_sair_menu.rect.y))
                    pygame.display.update()
                janela.fill((0, 0, 0))
                pygame.display.update()
                sleep(1)
                if fase_atual > 0:
                    tela_atual = "jogo"
                else:
                    tela_atual = "inicio"
            elif botão_configurações_menu.rect.collidepoint(posição_mouse):
                audio_select.play()
                tela_atual = "configurações"
            elif botão_sair_menu.rect.collidepoint(posição_mouse):
                audio_select.play()
                pygame.quit()
                exit()

        # carregar as coisas na tela
        janela.blit(imagem_fundo_menu.image, (0, 0))
        janela.blit(titulo_menu.texto_formatado, (titulo_menu.rect.x, titulo_menu.rect.y))

        # botões
        janela.blit(botão_jogar_menu.texto_formatado, (botão_jogar_menu.rect.x, botão_jogar_menu.rect.y))
        janela.blit(botão_configurações_menu.texto_formatado, (botão_configurações_menu.rect.x, botão_configurações_menu.rect.y))
        janela.blit(botão_sair_menu.texto_formatado, (botão_sair_menu.rect.x, botão_sair_menu.rect.y))
    
    elif tela_atual == "configurações":
        if voltar:
            audio_select.play()
            tela_atual = "menu"
        janela.blit(imagem_fundo_menu.image, (0, 0))
        janela.blit(titulo_menu.texto_formatado, (titulo_menu.rect.x, titulo_menu.rect.y))

        janela.blit(imagem_audio.image, (largura_tela // 2 - 200, altura_tela // 2 - 50))
        pygame.draw.line(janela, (20, 20, 20), (largura_tela // 2 - 16, altura_tela // 2 + 250), (largura_tela // 2 - 16, altura_tela // 2 + 250 - posição_bolinha), 20)
        bolinha = pygame.draw.circle(janela, (0, 0, 0), (largura_tela // 2 - 15, altura_tela // 2 + 250 - posição_bolinha), 30)

        if pygame.mouse.get_pressed()[0] and bolinha.collidepoint(posição_mouse) and altura_tela // 2 + 250 >= posição_mouse[1] >= altura_tela // 2 - 250:
            posição_bolinha = altura_tela // 2 + 250 - posição_mouse[1]
            volume = posição_bolinha / 500
            pygame.mixer.music.set_volume(volume)
            audio_fade_in.set_volume(volume)
            audio_erro.set_volume(0.1 * volume)
            audio_abre_folha.set_volume(volume)
            audio_andar.set_volume(volume* 0.6)
            audio_fecha_folha.set_volume(volume)
            audio_select.set_volume(volume)

    elif tela_atual == "inicio":
        if fase_atual == 0:
            tela_atual = mensagem(texto_inicial, tela_atual)

        elif fase_atual == 3:
            tela_atual = mensagem(texto_pré_1, tela_atual)
        
        elif fase_atual == 6:
            tela_atual = mensagem(texto_1_2, tela_atual)

        elif fase_atual == 9:
            tela_atual = mensagem(texto_2_pos, tela_atual, ".")

        if tela_atual == "jogo" or tela_atual == "pos_modernismo":
            texto_inicial.escurecer = False
            texto_pré_1.escurecer = False
            texto_1_2.escurecer = False
            texto_2_pos.escurecer = False
            
    elif tela_atual == "jogo":
        if not final_jogo:
            if voltar:
                audio_select.play()
                tela_atual = "menu"

            # animações
            # pergaminho
            if altura_pergaminho == 15:
                movimento_pergaminho = -0.5
            elif altura_pergaminho == -15:
                movimento_pergaminho = 0.5
            altura_pergaminho += movimento_pergaminho

            # seta
            if seta_pos == 10:
                seta_mov = -1
            elif seta_pos == -10:
                seta_mov = 1
            seta_pos += seta_mov

            if click and botão_restart.rect.collidepoint(posição_mouse):
                audio_select.play()
                restart()

            if carlos_drumond.vidas <= 0:
                carlos_drumond.vidas = vidas[fase_atual]          

            jogo_principal(fase_atual)

    elif tela_atual == "poema":
        if poema_atual == 0:
            audio_abre_folha.play()
            poema_atual = 1
        janela.blit(todos_poemas[fase_atual].image, ((largura_tela - todos_poemas[fase_atual].largura) // 2, 0))
        janela.blit(imagem_mouse.image, (-10, 20))

        if voltar or click:
            audio_fecha_folha.play()
            tela_atual = "jogo"

    elif tela_atual == "entre_fases":
        fade_janela += 2
        if fade_janela == 80:
            fade_janela = 0
            tela_atual = "jogo"

    elif tela_atual == "pos_modernismo":
        texto_passaro = Carregar_texto(str(passaro.vidas), "04b", 100, 0, 0, None, True, (255, 255, 255))
        if not fim_do_final:
            timing += 1
            if timing == 1:
                b_all = [[], [], []]

                for c in range(0, 96):
                    lista = [0, 0, 0]

                    numero_aleatorio = randint(0, 2)
                    lista[numero_aleatorio] = 1

                    numero_aleatorio2 = randint(0,2)
                    while numero_aleatorio2 == numero_aleatorio or lista[numero_aleatorio2] == 1:
                        numero_aleatorio2 = randint(0,2)
                    lista[numero_aleatorio2] = 2

                    for p in range(0, 3):
                        b_all[p].append(lista[p])
                        
                bloco1 = Bloco(largura_tela, b_all[0])

                bloco2 = Bloco(largura_tela, b_all[1])

                bloco3 = Bloco(largura_tela, b_all[2])

                blocos = [bloco1, bloco2, bloco3]

                blocos_passados = 0
                bloco_certo = 0
                for c in range(0, 3):
                    if blocos[c].cor_atual == passaro.atual:
                        bloco_certo = c

            for c in range(0, len(bloco1.posições)):
                if bloco1.posições[c] >= largura_tela - 250 >= bloco1.posições[c] - 10:
                    blocos_passados += 1

                    if blocos_passados >= 4:
                        passaro.trocar_cor()
                        blocos_passados = 0
                        bloco_certo = 0
                        for c in range(0, 3):
                            if blocos[c].cor_atual == passaro.atual:
                                bloco_certo = c

            if timing == 222:
                pygame.mixer.music.load("audios/musicas/musica_final.mp3")
                pygame.mixer.music.play(1)

            for c in range(0, 3):
                for t in range(0, len(blocos[c].lugares)):
                    if blocos[c].lugares[t] <= timing:
                        blocos[c].posições[t] += velocidade_blocos

            for c in range(0, len(blocos[passaro.posição_atual].posições)):
                if bloco_certo != passaro.atual and blocos[passaro.posição_atual].posições[c] + 142 <= largura_tela - 250 <= blocos[passaro.posição_atual].posições[c] + 150 and passaro.atual != blocos[passaro.posição_atual].blocos_cores[c]:
                    audio_erro.play()
                    passaro.vidas -= 1
                    if passaro.vidas == 0:
                        fim_do_final = True
                        pygame.mixer.music.fadeout(3000)
            if timing == 5550:
                fim_do_final = True
                pygame.mixer.music.fadeout(3000)

            for c in range(0, len(bloco1.lugares)):
                if not bloco1.posições[c] <= -150 or not bloco1.posições[c] >= largura_tela:
                    janela.blit(bloco1.cores[bloco1.blocos_cores[c]], (bloco1.posições[c], (altura_tela - altura_tela // 200 * 200) // 2))

            for c in range(0, len(bloco2.lugares)):
                if not bloco2.posições[c] <= -150 or not bloco2.posições[c] >= largura_tela:
                    janela.blit(bloco2.cores[bloco2.blocos_cores[c]], (bloco2.posições[c], altura_tela // 2 - 75))

            for c in range(0, len(bloco3.lugares)):
                if not bloco3.posições[c] <= -150 or not bloco3.posições[c] >= largura_tela:
                    janela.blit(bloco3.cores[bloco3.blocos_cores[c]], (bloco3.posições[c], (altura_tela + altura_tela // 200 * 200) // 2 - 150))
            
            janela.blit(passaro.image, (largura_tela - 250, passaro.posição))
            janela.blit(texto_passaro.texto_formatado, (0, altura_tela - 100))

        else:
            for c in range(0, len(bloco1.lugares)):
                if not bloco1.posições[c] <= -150 or not bloco1.posições[c] >= largura_tela:
                    bloco1.fade_out(1)
                    janela.blit(bloco1.cores[bloco1.blocos_cores[c]], (bloco1.posições[c], (altura_tela - altura_tela // 200 * 200) // 2))

            for c in range(0, len(bloco2.lugares)):
                if not bloco2.posições[c] <= -150 or not bloco2.posições[c] >= largura_tela:
                    bloco2.fade_out(1)
                    janela.blit(bloco2.cores[bloco2.blocos_cores[c]], (bloco2.posições[c], altura_tela // 2 - 75))

            for c in range(0, len(bloco3.lugares)):
                if not bloco3.posições[c] <= -150 or not bloco3.posições[c] >= largura_tela:
                    bloco3.fade_out(1)
                    janela.blit(bloco3.cores[bloco3.blocos_cores[c]], (bloco3.posições[c], (altura_tela + altura_tela // 200 * 200) // 2 - 150))

            janela.blit(passaro.image, (largura_tela - 250, passaro.posição))
            janela.blit(texto_passaro.texto_formatado, (0, altura_tela - 100))
            
            passaro.fade_out(1)
            if passaro.valor_fade <= 0:
                tela_atual = "animação_final"
                fundo_animação = Carregar_imagem("pos_modernismo/animação_fundo", 0, 0)
                fundo_animação.escala([768, 768])
                animação_imagem_inicial = Carregar_imagem("pos_modernismo/animação_imagem1", 0, 0)
                animação_imagem_inicial.escala([768, 768])
                carlos_final = Carlos_animação()
                contagem = 0
                contagem2 = 0
                audio_fade_in.play()

    elif tela_atual == "animação_final":
        contagem += 1
        
        if contagem >= 120:
            janela.blit(fundo_animação.image, ((largura_tela - 768) // 2, (altura_tela - 768) // 2))
            janela.blit(carlos_final.image, ((largura_tela - 768) // 2 + 240 + carlos_final.posição_x, (altura_tela - 768) // 2 + 270))


            if contagem < 296:
                janela.blit(animação_imagem_inicial.image, ((largura_tela - 768) // 2, (altura_tela - 768) // 2))
            elif contagem > 360:
                if carlos_final.posição_x >= 123:
                    if carlos_final.posição_x == 123:
                        carlos_final.image = carlos_final.costas
                    contagem2 += 1
                    if contagem2 >= 150:
                        tela_atual = "poema_final"
                        fechar_jogo = False
                        mensagem_final = Carregar_texto("Era tudo um sonho. Obrigado por jogar!", "04b" , 80, 0, 0, None, True, (255, 255, 255))
                        contagem = 0
                        audio_abre_folha.play()
                        poema_final = Carregar_imagem("poemas/poema_final", 0, 0)
                        poema_final.escala([altura_tela, altura_tela])
                else:
                    carlos_final.update()
                    carlos_final.posição_x += 1

    elif tela_atual == "poema_final":
        if not fechar_jogo:
            janela.blit(poema_final.image, ((largura_tela - altura_tela) // 2, 0))
            janela.blit(imagem_mouse.image, (-10, 20))

            if voltar or click:
                fechar_jogo = True
                audio_fecha_folha.play()

        if fechar_jogo:
            contagem += 1
            janela.blit(mensagem_final.texto_formatado, ((largura_tela - mensagem_final.largura) // 2, (altura_tela - mensagem_final.altura) // 2))
            if contagem == 518:
                pygame.quit()
                exit()

    voltar = False
    click = False
    pygame.display.update()

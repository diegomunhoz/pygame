import pygame
import random
import time

class Recs(object):
    def __init__(self, numeroinicial):
        self.lista = []

        for x in range(numeroinicial):
            leftrandom = random.randrange(2,560)
            toprandom = random.randrange(-580,-10)
            width = random.randrange(10,30)
            height = random.randrange(15,30)
            self.lista.append(pygame.Rect(leftrandom,toprandom,width,height))

    def mover(self):
        for retangulo in self.lista:
            retangulo.move_ip(0,2)

    def cor(self, superficie):
        for retangulo in self.lista:
            pygame.draw.rect(superficie,(165,214,254),retangulo)

    def recriar(self):
        for x in range(len(self.lista)):
            if self.lista[x].top > 481:
                leftrandom = random.randrange(2,560)
                toprandom = random.randrange(-580,-10)
                width = random.randrange(10,30)
                height = random.randrange(15,30)
                self.lista[x] = (pygame.Rect(leftrandom,toprandom,width,height))

    def fimJogo(self):
        self.lista.clear()

class Player(pygame.sprite.Sprite):

    def __init__(self, imagem):
        self.imagem = imagem
        self.rect = self.imagem.get_rect()
        self.rect.top, self.rect.left = (100,200)

    def mover(self,vx,vy):
        self.rect.move_ip(vx,vy)

    def update(self, superficie):
        superficie.blit(self.imagem, self.rect)

def colisao(player, recs):
    for rec in recs.lista:
        if player.rect.colliderect(rec):
            return True
    return False

def main():
    pygame.init()

    tela = pygame.display.set_mode((480,300))
    relogio = pygame.time.Clock()

    cor_vermelha = (227,57,9)
    cor_branca = (255,255,255)

    img_asteroide = pygame.image.load("imagens/asteroide.png").convert_alpha()

    img_nave = pygame.image.load("imagens/nave.png").convert_alpha()
    jogador = Player(img_nave)

    img_fundo = pygame.image.load("imagens/fundo.png").convert_alpha()
    img_explosao = pygame.image.load("imagens/explosao.png").convert_alpha()

    pygame.mixer.music.load("audios/musica.mp3")
    pygame.mixer.music.play(3)

    som_explosao = pygame.mixer.Sound("audios/explosao.wav")
    som_movimento = pygame.mixer.Sound("audios/movimento.wav")

    contFim = 0

    vx, vy = (0,0)
    velocidade = 10
    leftpress, rightpress, uppress, downpress = False, False, False, False

    texto = pygame.font.SysFont("Arial",15,True,False)

    txt_perdeu = texto.render('VOCÊ PERDEU!!!', 1, cor_branca)
    txt_continuar = texto.render('Pressione <ENTER> para continuar ou <ESC> para sair!', 1, cor_vermelha)

    ret = Recs(30)

    colidiu = False
    sair = False

    while sair != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair  = True

            if colidiu == False:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        leftpress = True
                        vx = - velocidade
                        som_movimento.play()

                    if event.key == pygame.K_RIGHT:
                        rightpress = True
                        vx = velocidade
                        som_movimento.play()

                    if event.key == pygame.K_UP:
                        uppress = True
                        vy = - velocidade
                        som_movimento.play()

                    if event.key == pygame.K_DOWN:
                        downpress = True
                        vy = velocidade
                        som_movimento.play()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        leftpress = False
                        if rightpress:
                            vx = velocidade
                        else:
                            vx = 0

                    if event.key == pygame.K_RIGHT:
                        rightpress = False
                        if leftpress:
                            vx = -velocidade
                        else:
                            vx = 0

                    if event.key == pygame.K_UP:
                        uppress = False
                        if downpress: vx = velocidade
                        vy = 0

                    if event.key == pygame.K_DOWN:
                        downpress = False
                        if uppress: vx = -velocidade
                        vy = 0
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:

                        som_explosao.stop()
                        main()

                    if event.key == pygame.K_ESCAPE:
                        sair = True

        if colisao(jogador, ret):
            colidiu = True
            jogador.imagem = img_explosao
            pygame.mixer.music.stop()
            som_explosao.play()

        if colidiu == False:
            ret.mover()
            jogador.mover(vx, vy)

            segundos = pygame.time.get_ticks() / 1000
            segundos = str(segundos)
            contador = texto.render("Pontuação:{}".format(segundos), 0, cor_branca)

        relogio.tick(20)
        tela.blit(img_fundo, (0, 0))
        tela.blit(contador, (350, 10))
        ret.cor(tela)
        ret.recriar()
        jogador.update(tela)

        pygame.display.update()

        if colidiu == True:
            jogador.mover(600,600)
            ret.fimJogo()
            tela.blit(txt_perdeu, (180, 120))
            tela.blit(txt_continuar, (50, 140))
            pygame.display.update()
            pygame.init()

    pygame.quit()

main()
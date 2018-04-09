from random import *
import sys
import time
import pygame

LARGURA = 640
ALTURA = 480

cor_azul = (0, 0, 64)
cor_branca = (255,255,255)
cor_violeta = (159,95,159)
cor_wood = (165,128,100)

vel = 0

pygame.init()

class Cena:
    def __init__(self):
        "Inicialização"
        self.proximaCena = False
        self.jogando = True

    def ler_eventos(self, eventos):
        "Le lista de todos os eventos"
        pass

    def atualizar(self):
        "Calculos e lógica"
        pass

    def desenhar(self, tela):
        "Desenhas os objetos na tela"
        pass

    def mudar_cena(self,cena):
        "Seleciona nova cena a ser exibida"
        self.proximaCena = cena

class Diretor:
    def __init__(self, titulo ="", res = ((LARGURA,ALTURA))):
        # Inicializando a tela
        self.tela = pygame.display.set_mode(res)
        # Configurar título de tela
        pygame.display.set_caption(titulo)
        # Criar o relogio
        self.reloj = pygame.time.Clock()
        self.cena = None
        self.cenas = {}

    def executar(self, cena_inicial, fps = 60):
        self.cena = self.cenas[cena_inicial]
        jogando = True
        while jogando:
            self.reloj.tick(fps)
            eventos = pygame.event.get()
            # Verificar todos os eventos
            for evento in eventos:
                # Se pressionar o 'X' da barra de titulo da tela
                if evento.type == pygame.QUIT:
                    # encerra o jogo

                    sys.exit()

            self.cena.ler_eventos(eventos)
            self.cena.atualizar()
            self.cena.desenhar(self.tela)

            self.escolherCena(self.cena.proximaCena)

            if jogando:
                jogando = self.cena.jogando

            pygame.display.flip()

        time.sleep(2)

    def escolherCena(self, proximaCena):
        if proximaCena:
            if proximaCena not in self.cenas:
                self.agregarCena(proximaCena)
            self.cena = self.cenas[proximaCena]

    def agregarCena(self,cena):
        cenaClasse = 'Cena'+cena
        cenaObj = globals()[cenaClasse]
        self.cenas[cena] = cenaObj();

class CenaNivel1(Cena):
    def __init__(self):
        Cena.__init__(self)
        self.bola = Bola()
        self.jogador = Paleta()
        self.ganharVida = Vida()
        # self.muro = Muro(1)
        self.muro = Muro(config.getQtd())

        self.pontos = config.getPontos()
        self.vidas = config.getVidas()
        self.esperando_saque = True

        config.setGanhou(False)

        # Ajustar  repetição de evento de tecla pressionada
        pygame.key.set_repeat(30)

    def ler_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                self.jogador.update(evento)
                if self.esperando_saque == True and evento.key == pygame.K_SPACE:
                    self.esperando_saque = False
                    if self.bola.rect.centerx < LARGURA / 2:
                        self.bola.speed = [3, -3]
                    else:
                        self.bola.speed = [-3, -3]

    def atualizar(self):
        # Libera vida adicional ao jogador
        if self.vidas < 2:
            self.ganharVida.update()

        # Atualizar posição da bola
        if self.esperando_saque == False:
            self.bola.update()
        else:
            self.bola.rect.midbottom = self.jogador.rect.midtop

        # Verificar colisão entre a bola e o jogador
        if pygame.sprite.collide_rect(self.bola, self.jogador):
            self.bola.speed[1] = -self.bola.speed[1]

        # Verificar colisão entre a vida e o jogador
        if pygame.sprite.collide_rect(self.ganharVida, self.jogador):
            self.ganharVida.apagar()
            self.vidas += 1

        # Colisão entre a bola e o tijolo
        # pygame.sprite.spritecollide(bola,muro,True)
        lista = pygame.sprite.spritecollide(self.bola, self.muro, False)
        if lista:
            tijolo = lista[0]
            cx = self.bola.rect.centerx
            if cx < tijolo.rect.left or cx > tijolo.rect.right:
                self.bola.speed[0] = -self.bola.speed[0]
            else:
                self.bola.speed[1] = -self.bola.speed[1]
            self.muro.remove(tijolo)
            self.pontos += 10

        # Verificar se a bola sai da tela
        if self.bola.rect.top > ALTURA:
            self.vidas -= 1
            self.esperando_saque = True

        if self.vidas <= 0:
            self.mudar_cena('JogoFinalizado')

        if len(self.muro) == 0:
            config.setNivel(2)
            config.setPontos(self.pontos)
            config.setVidas(self.vidas)
            config.setGanhou(True)
            self.mudar_cena('Proximo')

    def desenhar(self, tela):
        # Preencher a cor na tela
        tela.fill(cor_azul)
        # Mostrar pontuação
        self.exibir_pontos(tela)
        # Mostrar vidas
        self.exibir_vida(tela)
        # Desenhar a bola na tela
        tela.blit(self.bola.image, self.bola.rect)
        # Desenhar o jogador na tela
        tela.blit(self.jogador.image, self.jogador.rect)
        # Desenhar os tijolos na tela
        self.muro.draw(tela)
        # Desenhar a vida na tela
        tela.blit(self.ganharVida.image, self.ganharVida.rect)

    def exibir_pontos(self, tela):
        font = pygame.font.SysFont('Consolas', 20)
        pontuacao = 'Pontos:' + str(self.pontos).zfill(5)
        texto = font.render(pontuacao, True, cor_branca)
        texto_rect = texto.get_rect()
        texto_rect.topleft = [0,0]
        tela.blit(texto, texto_rect)

    def exibir_vida(self, tela):
        font = pygame.font.SysFont('Consolas', 20)
        totalVidas = 'Vidas:' + str(self.vidas).zfill(2)
        texto = font.render(totalVidas, True, cor_branca)
        texto_rect = texto.get_rect()
        texto_rect.topright = [LARGURA,0]
        tela.blit(texto, texto_rect)

class CenaNivel2(Cena):
    def __init__(self):
        Cena.__init__(self)
        self.bola = Bola()
        self.jogador = Paleta()
        self.ganharVida = Vida()
        # self.muro = Muro(1)
        self.muro = Muro(config.getQtd())

        self.pontos = config.getPontos()
        self.vidas = config.getVidas()
        self.esperando_saque = True

        config.setGanhou(False)

        # Ajustar  repetição de evento de tecla pressionada
        pygame.key.set_repeat(30)

    def ler_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                self.jogador.update(evento)
                if self.esperando_saque == True and evento.key == pygame.K_SPACE:
                    self.esperando_saque = False
                    if self.bola.rect.centerx < LARGURA / 2:
                        self.bola.speed = [5, -5]
                    else:
                        self.bola.speed = [-5, -5]

    def atualizar(self):
        if self.vidas < 2:
            self.ganharVida.update()

        # Atualizar posição da bola
        if self.esperando_saque == False:
            self.bola.update()
        else:
            self.bola.rect.midbottom = self.jogador.rect.midtop

        # Verificar colisão entre a vida e o jogador
        if pygame.sprite.collide_rect(self.ganharVida, self.jogador):
            self.ganharVida.apagar()
            self.vidas += 1

        # Verificar colisão entre a bola e o jogador
        if pygame.sprite.collide_rect(self.bola, self.jogador):
            self.bola.speed[1] = -self.bola.speed[1]

        # Colisão entre a bola e o tijolo
        # pygame.sprite.spritecollide(bola,muro,True)
        lista = pygame.sprite.spritecollide(self.bola, self.muro, False)
        if lista:
            tijolo = lista[0]
            cx = self.bola.rect.centerx
            if cx < tijolo.rect.left or cx > tijolo.rect.right:
                self.bola.speed[0] = -self.bola.speed[0]
            else:
                self.bola.speed[1] = -self.bola.speed[1]
            self.muro.remove(tijolo)
            self.pontos += 10

        # Verificar se a bola sai da tela
        if self.bola.rect.top > ALTURA:
            self.vidas -= 1
            self.esperando_saque = True

        if self.vidas <= 0:
            self.mudar_cena('JogoFinalizado')

        if len(self.muro) == 0:
            config.setNivel(3)
            config.setPontos(self.pontos)
            config.setVidas(self.vidas)
            config.setGanhou(True)
            self.mudar_cena('Proximo')

    def desenhar(self, tela):
        # Preencher a cor na tela
        tela.fill(cor_wood)
        # Mostrar pontuação
        self.exibir_pontos(tela)
        # Mostrar vidas
        self.exibir_vida(tela)
        # Desenhar a bola na tela
        tela.blit(self.bola.image, self.bola.rect)
        # Desenhar o jogador na tela
        tela.blit(self.jogador.image, self.jogador.rect)
        # Desenhar os tijolos na tela
        self.muro.draw(tela)
        # Desenhar a vida na tela
        tela.blit(self.ganharVida.image, self.ganharVida.rect)

    def exibir_pontos(self, tela):
        font = pygame.font.SysFont('Consolas', 20)
        pontuacao = 'Pontos:' + str(self.pontos).zfill(5)
        texto = font.render(pontuacao, True, cor_branca)
        texto_rect = texto.get_rect()
        texto_rect.topleft = [0,0]
        tela.blit(texto, texto_rect)

    def exibir_vida(self, tela):
        font = pygame.font.SysFont('Consolas', 20)
        totalVidas = 'Vidas:' + str(self.vidas).zfill(2)
        texto = font.render(totalVidas, True, cor_branca)
        texto_rect = texto.get_rect()
        texto_rect.topright = [LARGURA,0]
        tela.blit(texto, texto_rect)

class CenaNivel3(Cena):
    def __init__(self):
        Cena.__init__(self)
        self.bola = Bola()
        self.jogador = Paleta()
        self.ganharVida = Vida()
        # self.muro = Muro(1)
        self.muro = Muro(config.getQtd())

        self.pontos = config.getPontos()
        self.vidas = config.getVidas()
        self.esperando_saque = True

        config.setGanhou(False)

        # Ajustar  repetição de evento de tecla pressionada
        pygame.key.set_repeat(30)

    def ler_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                self.jogador.update(evento)
                if self.esperando_saque == True and evento.key == pygame.K_SPACE:
                    self.esperando_saque = False
                    if self.bola.rect.centerx < LARGURA / 2:
                        self.bola.speed = [7, -7]
                    else:
                        self.bola.speed = [-7, -7]

    def atualizar(self):
        if self.vidas < 2:
            self.ganharVida.update()

        # Atualizar posição da bola
        if self.esperando_saque == False:
            self.bola.update()
        else:
            self.bola.rect.midbottom = self.jogador.rect.midtop

        # Verificar colisão entre a vida e o jogador
        if pygame.sprite.collide_rect(self.ganharVida, self.jogador):
            self.ganharVida.apagar()
            self.vidas += 1

        # Verificar colisão entre a bola e o jogador
        if pygame.sprite.collide_rect(self.bola, self.jogador):
            self.bola.speed[1] = -self.bola.speed[1]

        # Colisão entre a bola e o tijolo
        # pygame.sprite.spritecollide(bola,muro,True)
        lista = pygame.sprite.spritecollide(self.bola, self.muro, False)
        if lista:
            tijolo = lista[0]
            cx = self.bola.rect.centerx
            if cx < tijolo.rect.left or cx > tijolo.rect.right:
                self.bola.speed[0] = -self.bola.speed[0]
            else:
                self.bola.speed[1] = -self.bola.speed[1]
            self.muro.remove(tijolo)
            self.pontos += 10

        # Verificar se a bola sai da tela
        if self.bola.rect.top > ALTURA:
            self.vidas -= 1
            self.esperando_saque = True

        if self.vidas <= 0:
            self.mudar_cena('JogoFinalizado')

        if len(self.muro) == 0:
            self.mudar_cena('JogoGanho')

    def desenhar(self, tela):
        # Preencher a cor na tela
        tela.fill(cor_violeta)
        # Mostrar pontuação
        self.exibir_pontos(tela)
        # Mostrar vidas
        self.exibir_vida(tela)
        # Desenhar a bola na tela
        tela.blit(self.bola.image, self.bola.rect)
        # Desenhar o jogador na tela
        tela.blit(self.jogador.image, self.jogador.rect)
        # Desenhar os tijolos na tela
        self.muro.draw(tela)
        # Desenhar a vida na tela
        tela.blit(self.ganharVida.image, self.ganharVida.rect)

    def exibir_pontos(self, tela):
        font = pygame.font.SysFont('Consolas', 20)
        pontuacao = 'Pontos:' + str(self.pontos).zfill(5)
        texto = font.render(pontuacao, True, cor_branca)
        texto_rect = texto.get_rect()
        texto_rect.topleft = [0,0]
        tela.blit(texto, texto_rect)

    def exibir_vida(self, tela):
        font = pygame.font.SysFont('Consolas', 20)
        totalVidas = 'Vidas:' + str(self.vidas).zfill(2)
        texto = font.render(totalVidas, True, cor_branca)
        texto_rect = texto.get_rect()
        texto_rect.topright = [LARGURA,0]
        tela.blit(texto, texto_rect)

class CenaProximo(Cena):
    def atualizar(self):
        self.jogando = False

class CenaJogoGanho(Cena):
    def atualizar(self):
        self.jogando = False
        config.setGanhou(True)

    def desenhar(self,tela):
        font = pygame.font.SysFont('Arial', 80, bold=True)
        texto = font.render('Você ganhou :)', True, cor_branca)
        texto_rect = texto.get_rect()
        texto_rect.center = [LARGURA / 2, ALTURA / 2]
        tela.blit(texto, texto_rect)

class CenaJogoFinalizado(Cena):
    def atualizar(self):
        self.jogando = False
        config.setGanhou(False)

    def desenhar(self,tela):
        font = pygame.font.SysFont('Arial', 80, bold=True)
        texto = font.render('Você perdeu :(', True, cor_branca)
        texto_rect = texto.get_rect()
        texto_rect.center = [LARGURA / 2, ALTURA / 2]
        tela.blit(texto, texto_rect)

class Bola(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        if config.getNivel() == 1:
            self.image = pygame.image.load('imagens/bola1.png')
        elif config.getNivel() == 2:
            self.image = pygame.image.load('imagens/bola2.png')
        elif config.getNivel() == 3:
            self.image = pygame.image.load('imagens/bola3.png')
        # Obter retangulo da tela
        self.rect = self.image.get_rect()
        # Posição inicial central na tela
        self.rect.centerx = LARGURA / 2
        self.rect.centery = ALTURA / 2
        # Estabelecer velocidade inicial
        self.speed = [3, 3]

    def update(self):
        # Evitar que saia por cima da tela
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        # Evitar que saia pela direita e esquerda da tela
        elif self.rect.right >= LARGURA or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # Mover com base na posição atual e velocidade
        self.rect.move_ip(self.speed)

class Vida(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('imagens/vida.png')
        # Obter retangulo da tela
        self.rect = self.image.get_rect()
        # Obtem posição aleatória
        self.x = int(randint(0,640))
        # Posição inicial central na tela em X
        self.rect.midbottom = (self.x,0)
        # Obtem posição aleatória
        self.x = int(randint(0,640))
        # Posição inicial central na tela em X
        self.rect.midbottom = (self.x,0)
        self.rect.move_ip((0,0))

    def update(self):
        # Mover com base na posição atual e velocidade
        self.rect.move_ip((0,2))

    def apagar(self):
        self.rect.move_ip((700,700))

class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        if config.getNivel() == 1:
            self.image = pygame.image.load('imagens/paleta1.png')
        elif config.getNivel() == 2:
            self.image = pygame.image.load('imagens/paleta2.png')
        elif config.getNivel() == 3:
            self.image = pygame.image.load('imagens/paleta3.png')
        # Obter retangulo da tela
        self.rect = self.image.get_rect()
        # Posição inicial central na tela em X
        self.rect.midbottom = (LARGURA / 2, ALTURA - 20)
        # Estabelecer velocidade inicial
        self.speed = [0, 0]

    def update(self, evento):
        self.nivel = config.getNivel()
        if self.nivel == 1:
            vel = 5
        elif self.nivel == 2:
            vel = 10
        elif self.nivel == 3:
            vel = 15
        # Verificar se foi pressionado a telca esquerda
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-vel,0]
        # Se pressionou a tecla direita
        elif evento.key == pygame.K_RIGHT and self.rect.right < LARGURA:
            self.speed = [vel,0]
        else:
            self.speed = [0,0]
        # Mover com base na posição atual e velocidade
        self.rect.move_ip(self.speed)

        if evento.key == pygame.K_RETURN:
            fim = 'N'

        if evento.key == pygame.K_ESCAPE:
            fim = 'S'

class Tijolo(pygame.sprite.Sprite):
    def __init__(self, posicao):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        if config.getNivel() == 1:
            self.image = pygame.image.load('imagens/tijolo1.png')
        elif config.getNivel() == 2:
            self.image = pygame.image.load('imagens/tijolo2.png')
        elif config.getNivel() == 3:
            self.image = pygame.image.load('imagens/tijolo3.png')
        # Obter retangulo da tela
        self.rect = self.image.get_rect()
        # Posição Inicial
        self.rect.topleft = posicao

class Muro(pygame.sprite.Group):
    def __init__(self,quantidadeTijolos):
        pygame.sprite.Group.__init__(self)
        pos_x = 0
        pos_y = 20
        for i in range(quantidadeTijolos):
            tijolo = Tijolo((pos_x,pos_y))
            self.add(tijolo)
            pos_x += tijolo.rect.width
            if pos_x >= LARGURA:
                pos_x = 0
                pos_y += tijolo.rect.height

class Config:
    def __init__(self, nivel, ponto, vida, ganhou):
        self.nivel = nivel
        self.ponto = ponto
        self.vida = vida
        self.ganhou = ganhou

    def setNivel(self, nivel):
        self.nivel = nivel

    def setPontos(self, ponto):
        self.ponto = ponto

    def setVidas(self, vida):
        self.vida = vida

    def setGanhou(self, ganhou):
        self.ganhou = ganhou

    def getNivel(self):
        return self.nivel

    def getPontos(self):
        return self.ponto

    def getVidas(self):
        return self.vida

    def getQtd(self):
        if self.nivel == 1:
            return 32
        elif self.nivel == 2:
            return 64
        elif self.nivel == 2:
            return 128

    def getGanhou(self):
        return self.ganhou

config = Config(1,0,3,False)
diretor = Diretor('Breakout Game', (LARGURA,ALTURA))

diretor.agregarCena('Nivel1')
diretor.executar('Nivel1')

if config.getGanhou() == True:
    diretor.agregarCena('Nivel2')
    diretor.executar('Nivel2')

if config.getGanhou() == True:
    diretor.agregarCena('Nivel3')
    diretor.executar('Nivel3')

sys.exit()
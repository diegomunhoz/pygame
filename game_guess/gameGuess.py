# **********************************************************************************************************************
# ******   Programação II -  2º Ciclo Jogos Digitais                                                              ******
# ******   Programa: Jogo Guess - adivinhe o numero                                                               ******
# ******   Nome....: Diego Vinicius de Mello Munhoz    RA: 1430961723002                                          ******
# ******   Data....: 27/04/2018                                                                                   ******
# **********************************************************************************************************************

import socket, argparse, os, time, pygame

ALTURA = 800
LARGURA = 600

titulo = 'GUESS: Adinhe o Numero - Diego Vinicius de Mello Munhoz'

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

class GameGuess:
    def __init__(self, titulo="", res=((LARGURA, ALTURA))):
        self.mensagem_cliente = ' '
        self.mensagem_servidor = ' '
        self.running = True
        self.jogada = 0
        self.tentativas = 0
        self.terminal_select = ''
        self.numero_escolhido_cliente = 0
        self.numero_escolhido_servidor = 0
        self.window = pygame.display.set_mode((res))
        pygame.display.set_caption(titulo)
        self.telaInicial()
        self.processar(self.terminal_select)

    def telaInicial(self):
        escolha = pygame.image.load("img/escolha_terminal.png").convert()
        x_escolha = 50;
        y_escolha = 35;
        self.window.blit(escolha, (x_escolha, y_escolha))
        pygame.display.flip()

        img_cliente = pygame.image.load("img/cliente.png").convert()
        x_cliente = 110;
        y_cliente = 300;
        self.window.blit(img_cliente, (x_cliente, y_cliente))
        pygame.display.flip()

        img_servidor = pygame.image.load("img/servidor.png").convert()
        x_servidor = 410;
        y_servidor = 300;
        self.window.blit(img_servidor, (x_servidor, y_servidor))
        pygame.display.flip()

        rect_cliente = img_cliente.get_rect()
        rect_servidor = img_servidor.get_rect()

        rect_cliente.left = 110
        rect_cliente.top = 300

        rect_servidor.left = 410
        rect_servidor.top = 300

        self.running = True
        while self.running:
            pos = pygame.mouse.get_pos()
            pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos

                    if rect_cliente.collidepoint(x_pos, y_pos):
                        img_cliente = pygame.image.load("img/cliente_click.png").convert()
                        self.window.blit(img_cliente, (x_cliente, y_cliente))  # paint to screen
                        pygame.display.flip()  # paint screen one time
                        self.terminal_select = 'client'
                        time.sleep(1)
                        self.jogada += 1
                        self.running = False

                    if rect_servidor.collidepoint(x_pos, y_pos):
                        img_servidor = pygame.image.load("img/servidor_click.png").convert()
                        self.window.blit(img_servidor, (x_servidor, y_servidor))
                        pygame.display.flip()
                        self.terminal_select = 'server'
                        time.sleep(1)
                        self.jogada += 1
                        self.running = False

        fundo = pygame.image.load("img/fundo_tela.png").convert()
        x_fundo = 0
        y_fundo = 0;
        self.window.blit(fundo, (x_fundo, y_fundo))
        pygame.display.flip()

    def telaCliente(self):
        s = socket.socket()
        # host = socket.gethostname()
        host = '10.0.0.1'
        port = 8080

        s.connect((host, port))

        while True:
            if self.jogada == 1:
                fundo = pygame.image.load("img/fundo_tela.png").convert()
                x_fundo = 0;
                y_fundo = 0;
                self.window.blit(fundo, (x_fundo, y_fundo))
                pygame.display.flip()

                escolha = pygame.image.load("img/escolha.png").convert()
                x_escolha = 15;
                y_escolha = 20;
                self.window.blit(escolha, (x_escolha, y_escolha))

                self.tentativas = 0
                self.numero_escolhido_cliente = self.tabuleiro()

                self.jogada += 1
            else:
                fundo = pygame.image.load("img/fundo_tela.png").convert()
                x_fundo = 0;
                y_fundo = 0;
                self.window.blit(fundo, (x_fundo, y_fundo))
                pygame.display.flip()

                adivinhe = pygame.image.load("img/adivinhe.png").convert()
                x_adivinhe = 4;
                y_adivinhe = 20;
                self.window.blit(adivinhe, (x_adivinhe, y_adivinhe))

                self.tentativas = 0
                self.numero_escolhido_cliente = self.tabuleiro()

                self.jogada = 1

                fundo = pygame.image.load("img/fundo_tela.png").convert()
                x_fundo = 0;
                y_fundo = 0;
                self.window.blit(fundo, (x_fundo, y_fundo))
                pygame.display.flip()

                escolha = pygame.image.load("img/escolha.png").convert()
                x_escolha = 15;
                y_escolha = 20;
                self.window.blit(escolha, (x_escolha, y_escolha))

                self.tentativas = 0
                self.numero_escolhido_cliente = self.tabuleiro()

            fundo = pygame.image.load("img/fundo.png").convert()
            x_fundo = 40;
            y_fundo = 140;
            self.window.blit(fundo, (x_fundo, y_fundo))
            pygame.display.flip()

            aguarde_jogador = pygame.image.load("img/aguarde_jogador.png").convert()
            x_aguarde_jogador = 230;
            y_aguarde_jogador = 240;
            self.window.blit(aguarde_jogador, (x_aguarde_jogador, y_aguarde_jogador))
            pygame.display.flip()

            request = (str(self.mensagem_cliente) + str(self.numero_escolhido_cliente))

            bytes_text = bytes(request, 'utf-8')
            s.send(bytes_text)

            msg = s.recv(1024)
            msg_convert = str(msg.decode("utf-8"))

            ganhou_servidor = msg_convert[0]
            self.numero_escolhido_servidor = msg_convert[1]+msg_convert[2]

            if ganhou_servidor == 'S':
                fundo = pygame.image.load("img/fundo_tela.png").convert()
                x_fundo = 0;
                y_fundo = 0;
                self.window.blit(fundo, (x_fundo, y_fundo))
                pygame.display.flip()

                jogador_acertou = pygame.image.load("img/jogador_acertou.png").convert()
                x_jogador_acertou = 20;
                y_jogador_acertou = 180;
                self.window.blit(jogador_acertou, (x_jogador_acertou, y_jogador_acertou))
                pygame.display.flip()

            else:
                fundo = pygame.image.load("img/fundo.png").convert()
                x_fundo = 0;
                y_fundo = 0;
                self.window.blit(fundo, (x_fundo, y_fundo))
                pygame.display.flip()

                jogador_errou = pygame.image.load("img/jogador_errou.png").convert()
                x_jogador_errou = 20;
                y_jogador_errou = 180;
                self.window.blit(jogador_errou, (x_jogador_errou, y_jogador_errou))
                pygame.display.flip()

    def telaServidor(self):
        fundo = pygame.image.load("img/fundo_tela.png").convert()
        x_fundo = 0;
        y_fundo = 0;
        self.window.blit(fundo, (x_fundo, y_fundo))
        pygame.display.flip()

        conexao = pygame.image.load("img/conexao.png").convert()
        x_conexao = 220;
        y_conexao = 150;
        self.window.blit(conexao, (x_conexao, y_conexao))
        pygame.display.flip()

        s = socket.socket()
        # host = socket.gethostname()
        host = '10.0.0.1'
        port = 8080

        s.bind((host, port))
        s.listen(5)

        c, addr = s.accept()

        while True:
            msg = c.recv(1024)
            msg_convert =  str(msg.decode("utf-8"))

            ganhou_cliente = msg_convert[0]
            self.numero_escolhido_cliente = msg_convert[1]+msg_convert[2]

            fundo = pygame.image.load("img/fundo.png").convert()
            x_fundo = 20;
            y_fundo = 140;
            self.window.blit(fundo, (x_fundo, y_fundo))
            pygame.display.flip()

            adivinhe = pygame.image.load("img/adivinhe.png").convert()
            x_adivinhe = 4;
            y_adivinhe = 20;
            self.window.blit(adivinhe, (x_adivinhe, y_adivinhe))
            pygame.display.flip()

            self.tentativas = 0
            self.tabuleiro()

            self.jogada += 1

            fundo = pygame.image.load("img/fundo_tela.png").convert()
            x_fundo = 0;
            y_fundo = 0;
            self.window.blit(fundo, (x_fundo, y_fundo))
            pygame.display.flip()

            escolha = pygame.image.load("img/escolha.png").convert()
            x_escolha = 15;
            y_escolha = 20;
            self.window.blit(escolha, (x_escolha, y_escolha))
            pygame.display.flip()

            self.tentativas = 0
            self.numero_escolhido_servidor = self.tabuleiro()

            fundo = pygame.image.load("img/fundo.png").convert()
            x_fundo = 40;
            y_fundo = 140;
            self.window.blit(fundo, (x_fundo, y_fundo))
            pygame.display.flip()

            aguarde_jogador = pygame.image.load("img/aguarde_jogador.png").convert()
            x_aguarde_jogador = 230;
            y_aguarde_jogador = 240;
            self.window.blit(aguarde_jogador, (x_aguarde_jogador, y_aguarde_jogador))
            pygame.display.flip()

            request = (str(self.mensagem_servidor) + str(self.numero_escolhido_servidor))

            bytes_text = bytes(request, 'utf-8')
            c.send(bytes_text)

            self.jogada = 1

    def tabuleiro(self):

        img_01 = pygame.image.load("img/01.png").convert()
        x_01 = 110;
        y_01 = 180;
        self.window.blit(img_01, (x_01, y_01))
        pygame.display.flip()

        img_02 = pygame.image.load("img/02.png").convert()
        x_02 = 260;
        y_02 = 180;
        self.window.blit(img_02, (x_02, y_02))
        pygame.display.flip()

        img_03 = pygame.image.load("img/03.png").convert()
        x_03 = 410;
        y_03 = 180;
        self.window.blit(img_03, (x_03, y_03))
        pygame.display.flip()

        img_04 = pygame.image.load("img/04.png").convert()
        x_04 = 560;
        y_04 = 180;
        self.window.blit(img_04, (x_04, y_04))
        pygame.display.flip()

        img_05 = pygame.image.load("img/05.png").convert()
        x_05 = 110;
        y_05 = 300;
        self.window.blit(img_05, (x_05, y_05))
        pygame.display.flip()

        img_06 = pygame.image.load("img/06.png").convert()
        x_06 = 260;
        y_06 = 300;
        self.window.blit(img_06, (x_06, y_06))
        pygame.display.flip()

        img_07 = pygame.image.load("img/07.png").convert()
        x_07 = 410;
        y_07 = 300;
        self.window.blit(img_07, (x_07, y_07))
        pygame.display.flip()

        img_08 = pygame.image.load("img/08.png").convert()
        x_08 = 560;
        y_08 = 300;
        self.window.blit(img_08, (x_08, y_08))
        pygame.display.flip()

        img_09 = pygame.image.load("img/09.png").convert()
        x_09 = 110;
        y_09 = 420;
        self.window.blit(img_09, (x_09, y_09))
        pygame.display.flip()

        img_10 = pygame.image.load("img/10.png").convert()
        x_10 = 260;
        y_10 = 420;
        self.window.blit(img_10, (x_10, y_10))
        pygame.display.flip()

        img_11 = pygame.image.load("img/11.png").convert()
        x_11 = 410;
        y_11 = 420;
        self.window.blit(img_11, (x_11, y_11))
        pygame.display.flip()

        img_12 = pygame.image.load("img/12.png").convert()
        x_12 = 560;
        y_12 = 420;
        self.window.blit(img_12, (x_12, y_12))
        pygame.display.flip()

        rect_01 = img_01.get_rect()
        rect_02 = img_02.get_rect()
        rect_03 = img_03.get_rect()
        rect_04 = img_04.get_rect()
        rect_05 = img_05.get_rect()
        rect_06 = img_06.get_rect()
        rect_07 = img_07.get_rect()
        rect_08 = img_08.get_rect()
        rect_09 = img_09.get_rect()
        rect_10 = img_10.get_rect()
        rect_11 = img_11.get_rect()
        rect_12 = img_12.get_rect()

        rect_01.left = 110
        rect_01.top = 180

        rect_02.left = 260
        rect_02.top = 180

        rect_03.left = 410
        rect_03.top = 180

        rect_04.left = 560
        rect_04.top = 180

        rect_05.left = 110
        rect_05.top = 300

        rect_06.left = 260
        rect_06.top = 300

        rect_07.left = 410
        rect_07.top = 300

        rect_08.left = 560
        rect_08.top = 300

        rect_09.left = 110
        rect_09.top = 420

        rect_10.left = 260
        rect_10.top = 420

        rect_11.left = 410
        rect_11.top = 420

        rect_12.left = 560
        rect_12.top = 420

        pygame.display.update()

        self.running = True
        while self.running:
            pos = pygame.mouse.get_pos()
            pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos

                    if rect_01.collidepoint(x_pos, y_pos):
                        img_01 = pygame.image.load("img/01_click.png").convert()
                        self.window.blit(img_01, (x_01, y_01))
                        pygame.display.flip()
                        self.tentativas += 1
                        num_select = '01'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_02.collidepoint(x_pos, y_pos):
                        img_02 = pygame.image.load("img/02_click.png").convert()
                        self.window.blit(img_02, (x_02, y_02))
                        pygame.display.flip()
                        self.tentativas += 1
                        num_select = '02'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_03.collidepoint(x_pos, y_pos):
                        img_03 = pygame.image.load("img/03_click.png").convert()
                        self.window.blit(img_03, (x_03, y_03))
                        pygame.display.flip()
                        self.tentativas += 1
                        num_select = '03'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_04.collidepoint(x_pos, y_pos):
                        img_04 = pygame.image.load("img/04_click.png").convert()
                        self.window.blit(img_04, (x_04, y_04))
                        pygame.display.flip()
                        self.tentativas += 1
                        num_select = '04'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_05.collidepoint(x_pos, y_pos):
                        img_05 = pygame.image.load("img/05_click.png").convert()
                        self.window.blit(img_05, (x_05, y_05))  # paint to screen
                        pygame.display.flip()  # paint screen one time
                        self.tentativas += 1
                        num_select = '05'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_06.collidepoint(x_pos, y_pos):
                        img_06 = pygame.image.load("img/06_click.png").convert()
                        self.window.blit(img_06, (x_06, y_06))
                        pygame.display.flip()
                        self.tentativas += 1
                        num_select = '06'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_07.collidepoint(x_pos, y_pos):
                        img_07 = pygame.image.load("img/07_click.png").convert()
                        self.window.blit(img_07, (x_07, y_07))
                        pygame.display.flip()
                        self.tentativas += 1
                        num_select = '07'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_08.collidepoint(x_pos, y_pos):
                        img_08 = pygame.image.load("img/08_click.png").convert()
                        self.window.blit(img_08, (x_08, y_08))
                        pygame.display.flip()
                        self.tentativas += 1
                        num_select = '08'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_09.collidepoint(x_pos, y_pos):
                        img_09 = pygame.image.load("img/09_click.png").convert()
                        self.window.blit(img_09, (x_09, y_09))  # paint to screen
                        pygame.display.flip()  # paint screen one time
                        self.tentativas += 1
                        num_select = '09'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_10.collidepoint(x_pos, y_pos):
                        img_10 = pygame.image.load("img/10_click.png").convert()
                        self.window.blit(img_10, (x_10, y_10))
                        pygame.display.flip()
                        self.tentativas += 1
                        num_select = '10'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_11.collidepoint(x_pos, y_pos):
                        img_11 = pygame.image.load("img/11_click.png").convert()
                        self.window.blit(img_11, (x_11, y_11))
                        pygame.display.flip()
                        self.tentativas += 1
                        num_select = '11'
                        time.sleep(1)
                        self.processarClick(num_select)

                    if rect_12.collidepoint(x_pos, y_pos):
                        img_12 = pygame.image.load("img/12_click.png").convert()
                        self.window.blit(img_12, (x_12, y_12))
                        pygame.display.flip()
                        self.tentativas += 1
                        num_select = 12
                        time.sleep(1)
                        self.processarClick(num_select)

        return num_select

    def processarClick(self, numero):

        print(self.tentativas)

        if self.tentativas > 3:
            if self.terminal_select == 'client':
                self.mensagem_cliente = 'N'
            else:
                self.mensagem_servidor = 'N'

            self.tentativas = 0
            fundo = pygame.image.load("img/fundo.png").convert()
            x_fundo = 20;
            y_fundo = 140;
            self.window.blit(fundo, (x_fundo, y_fundo))
            pygame.display.flip()

            img_tentativas = pygame.image.load("img/tentativas.png").convert()
            x_tentativas = 100;
            y_tentativas = 220;
            self.window.blit(img_tentativas, (x_tentativas, y_tentativas))
            pygame.display.flip()

            self.running = False

            time.sleep(3)
        else:
            if self.terminal_select == 'client':
                if self.jogada == 1:
                    self.running = False
                else:
                    print('numero escolhido servidor: ', self.numero_escolhido_servidor)
                    print('numero clicado cliente: ', numero)
                    if int(self.numero_escolhido_servidor) == int(numero):
                        self.mensagem_cliente = 'S'
                        self.imprimeResultadoJogador()
            else:
                if self.jogada == 1:
                    print('numero escolhido cliente: ', self.numero_escolhido_cliente)
                    print('numero clicado servidor: ', numero)
                    if int(self.numero_escolhido_cliente) == int(numero):
                        self.mensagem_servidor = 'S'
                        self.imprimeResultadoJogador()
                else:
                    self.running = False

    def imprimeResultadoJogador(self):
        fundo = pygame.image.load("img/fundo.png").convert()
        x_fundo = 20;
        y_fundo = 140;
        self.window.blit(fundo, (x_fundo, y_fundo))
        pygame.display.flip()

        acertou = pygame.image.load("img/acertou.png").convert()
        x_acertou = 180;
        y_acertou = 240;
        self.window.blit(acertou, (x_acertou, y_acertou))
        pygame.display.flip()

        time.sleep(3)

        self.running = False

    def processar(self,terminal):
        if terminal == 'client':
            self.telaCliente()
        else:
            self.telaServidor()

if __name__ == '__main__':
    jogo = GameGuess(titulo,(ALTURA,LARGURA))
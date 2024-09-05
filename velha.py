import pygame # BIBLIOTECA JOGOS
import sys # SYSTEMA OP FUNCIONALIDADES
import random # GERADOR DE ALEATORIDADE
import time # CONTADOR DE TEMPO

# OBJETO JOGO DA VELHA
class JogoDaVelha:
    # VARIAVEIS
    def __init__(self, dimensao=3): # VALOR DA DIMENSÃO 3
        pygame.init() # INICIA JOGO
        pygame.mixer.init() # INICIA SOM
        self.dimensao = dimensao # DIMENSÃO
        self.jogadores = ["X", "O"] # JOGADORES
        self.rodada = 0 # CONTADOR RODADA
        self.tempo_inicio = None # TEMPO 0
        self.tempo_decorrido = None # TEMPO DECORRIDO 0
        self.mensagem_status = "" # MESSAGEM STATUS APAGADA
        self.jogo_acabou = False # JOGO NÃO ACABOU
        self.tabuleiro = [[" " for _ in range(dimensao)] for _ in range(dimensao)] # TABULEIRO COM BASE NA DIMENSÃO
        self.jogador_atual = "X" # JOGADOR INICIAL
        self.oponente = "O" # OPONENTE CPU
        self.vencedor_linha = None # LINHA DO VENCEDOR SEM COR
        self.tempo_fim = None # TEMPO DA PARTIDA
        self.modo_jogo = None # MODO DE JOGO CPU/JOGADOR

        # Configurações da Tela
        self.cor_fundo = (255, 255, 255)        # BRANCO 
        self.cor_linha = (0, 0, 0)              # PRETO
        self.cor_texto = (0, 0, 0)              # PRETO
        self.cor_texto2 = (255, 255, 255)       # BRANCO
        self.cor_info = (0, 0, 0)               # PRETO
        self.cor_fundo_info = (200, 200, 200)   # CINZA CLARO
        self.cor_botao = (0, 0, 0)              # PRETO
        self.largura, self.altura = dimensao * 100, dimensao * 100 # 300PX
        self.largura_info = 300 # 300PX
        self.tamanho_celula = self.largura // dimensao # 100PX 
        self.tela = pygame.display.set_mode((self.largura + self.largura_info, self.altura)) # 600PX LARGURA | 300PX ALTURA
        pygame.display.set_caption("Jogo da Velha Enrico Malta") # NOME NA JANELA DO WINDOWS
    
    # MOSTRA TABULEIRO
    def desenhar_tabuleiro(self):
        self.tela.fill(self.cor_fundo) # COR BRANCO TELA
        for linha in range(1, self.dimensao): # TRAÇÃ UMA LINHA POR QUADRADO NA DIMENSÃO
            pygame.draw.line(self.tela, self.cor_linha, (0, linha * self.tamanho_celula), (self.largura, linha * self.tamanho_celula), 2) # LINHA HORIZONTAL
            pygame.draw.line(self.tela, self.cor_linha, (linha * self.tamanho_celula, 0), (linha * self.tamanho_celula, self.altura), 2) # LINHA VERTICAL

        if self.vencedor_linha: # SE VENCER
            pygame.draw.line(self.tela, (255, 0, 0), self.vencedor_linha[0], self.vencedor_linha[1], 5) # ALTERAR COR DA LINHA DO VENCEDOR PARA VERMELHO
    
    # MOSTRA MARCAÇÕES
    def desenhar_movimentos(self):
        fonte = pygame.font.Font(None, 100) # TAMANHO FONTE DA MARCAÇÃO
        for i in range(self.dimensao): # RASTREIA LINHA
            for j in range(self.dimensao): # RASTREIA COLUNA
                if self.tabuleiro[i][j] != " ": # RASTREIA ESPAÇO VAZIO
                    texto = fonte.render(self.tabuleiro[i][j], True, self.cor_texto) # MARCA JOGADA
                    self.tela.blit(texto, (j * self.tamanho_celula + 25, i * self.tamanho_celula + 20)) # POSIONA JOGADA
    
    # MOSTRA DISPLAY INFORMAÇÕES
    def desenhar_informacoes(self):
        
        info_area = pygame.Rect(self.largura, 0, self.largura_info, self.altura) # RASTREIA AREA DA INFORMAÇÃO
        pygame.draw.rect(self.tela, self.cor_fundo_info, info_area) # DESENHA INFORMAÇÕES
        fonte_info = pygame.font.Font(None, 30) # TAMANHO FONTE INFORMAÇÃO

        if self.tempo_inicio is not None: # RASTREIA SE O JOGO COMEÇOU APARTIR DO CONTADOR DE TEMPO
            if self.tempo_fim is None: # RASTREIA SE O JOGO TERMINOU
                self.tempo_decorrido = time.time() - self.tempo_inicio # MOSTRA O TEMPO DA PARTIDA
            else:
                self.tempo_decorrido = self.tempo_fim - self.tempo_inicio # SE NÃO TERMINOU CONTINUA CONTANDO
            minutos = int(self.tempo_decorrido // 60) # FORMATA EM MINUTOS
            segundos = int(self.tempo_decorrido % 60) # FORMATA EM SEGUNDOS
            texto_tempo = fonte_info.render(f"Tempo: {minutos:02}:{segundos:02}", True, self.cor_info) # DESENHA NA TELA
            self.tela.blit(texto_tempo, (self.largura + 10, 10)) # TAMANGO FONTE

        if not self.jogo_acabou and self.modo_jogo == "CPU": # SE FOR P1 X CPU
            jogador = self.obter_jogador() # RASTREIA JOGADOR
            texto_jogador = fonte_info.render("Sua vez!", True, self.cor_info) # SUA VEZ PORQUE A CPU É MUITO RAPIDA E NÃO PENSA
            self.tela.blit(texto_jogador, (self.largura + 10, 50)) # TAMANHO FONTE
        if not self.jogo_acabou and self.modo_jogo == "JOGADOR": # SE FOR P1 X P2
            jogador = self.obter_jogador() # RASTREIA JOGADOR
            texto_jogador = fonte_info.render(f"Jogador: {jogador}", True, self.cor_info) # MOSTRA JOGADOR DA VEZ
            self.tela.blit(texto_jogador, (self.largura + 10, 50)) # TAMANHO FONTE


        if self.mensagem_status: # INFORMAÇÕES
            texto_status = fonte_info.render(self.mensagem_status, True, self.cor_info) # MOSTRA STATUS DA PARTIDA VENCEU/PERDEU
            self.tela.blit(texto_status, (self.largura + 10, 50)) # TAMANHO FONTE
    
    # BOTÃO DINAMICO
    def desenhar_botao(self, texto, posicao, largura, altura): # BOTÃO RECEBE TEXTO POSIÇÃO ALTURA E LARGURA
        retangulo = pygame.Rect(posicao, (largura, altura)) # DESENHA BOTÃO
        pygame.draw.rect(self.tela, self.cor_botao, retangulo) # COR DO BOTÃO
        fonte = pygame.font.Font(None, 20) # TAMANHO FONTE BOTÃO
        texto_renderizado = fonte.render(texto, True, self.cor_texto2) # ESCREVE O TEXTO
        texto_rect = texto_renderizado.get_rect(center=retangulo.center) # CENTRALIZA O TEXTO
        self.tela.blit(texto_renderizado, texto_rect) # RENDERIZA O BOTÃO
    
    # RASTREIA MOUSE NO BOTÃO
    def mouse_sobre_botao(self, posicao, largura, altura):# 
        mouse_x, mouse_y = pygame.mouse.get_pos() # RASTREIA ALTURA E LARGURA DA POSIÇÃO DO MOUSE NA TELA
        return posicao[0] < mouse_x < posicao[0] + largura and posicao[1] < mouse_y < posicao[1] + altura
    
    # RASTREIA JOGADOR
    def obter_jogador(self):
        return self.jogadores[self.rodada % 2] # LOGICA PARA DIVIDIR JOGADOR POR RODADA
    
    # RASTREIA MOVIMENTO
    def obter_movimento(self, x, y):
        return y // self.tamanho_celula, x // self.tamanho_celula # RASTREIA MOUSE PARA INDENTIFICAR MOVIMENTO
    
    # VALIDA MOVIMENTO RASTREADO
    def validar_movimento(self, movimento, jogador):
        self.tabuleiro[movimento[0]][movimento[1]] = jogador # VALIDA SE O MOVIMENTO É VALIDO/POSSIVEL
    
    # RASTREIA VITORIA PARTIDA
    def verificar_vitoria(self, jogador, oponente):
        for i in range(self.dimensao): # VERIFICAR LINHAS
            if all(self.tabuleiro[i][j] == jogador for j in range(self.dimensao)): # VERIFICA SE TODAS AS MARCAÇÕES NA LINHA SÃO DO JOGADOR
                self.vencedor_linha = ((0, i * self.tamanho_celula + self.tamanho_celula // 2), # DEFINE AS COORDENADAS DA LINHA VENCEDORA
                                       (self.largura, i * self.tamanho_celula + self.tamanho_celula // 2))
                return True
            if all(self.tabuleiro[j][i] == jogador for j in range(self.dimensao)): # VERIFICA SE TODAS AS MARCAÇÕES NA COLUNA SÃO DO JOGADOR
                self.vencedor_linha = ((i * self.tamanho_celula + self.tamanho_celula // 2, 0), # DEFINE AS COORDENADAS DA LINHA VENCEDORA
                                       (i * self.tamanho_celula + self.tamanho_celula // 2, self.altura))
                return True

        if all(self.tabuleiro[i][i] == jogador for i in range(self.dimensao)): # VERIFICA SE TODAS AS CÉLULAS NA DIAGONAL PRINCIPAL SÃO DO JOGADOR
            self.vencedor_linha = ((0, 0), (self.largura, self.altura)) # DEFINE AS COORDENADAS DA LINHA VENCEDORA
            return True
        if all(self.tabuleiro[i][self.dimensao - 1 - i] == jogador for i in range(self.dimensao)): # VERIFICA SE TODAS AS CÉLULAS NA DIAGONAL SECUNDÁRIA SÃO DO JOGADOR
            self.vencedor_linha = ((0, self.altura), (self.largura, 0)) # DEFINE AS COORDENADAS DA LINHA VENCEDORA
            return True

        return False
    
    # ATUALIZA GAMEBOARD
    def atualizar_jogo(self):
        self.desenhar_tabuleiro() # ATUALIZA TABULEIRO
        self.desenhar_movimentos() # ATUALIZA MOVIMENTOS
        self.desenhar_informacoes() # ATUALIZA INFORMAÇÕES
        self.verificar_vitoria(self.jogador_atual, self.oponente) # VERIFICA VITORIA
    
    # RESETA GAMEBOARD
    def reiniciar_jogo(self):
        self.rodada = 0 # RESETA RODADA
        self.mensagem_status = "" # RESETA INFORMAÇÕES
        self.tabuleiro = [[" " for _ in range(self.dimensao)] for _ in range(self.dimensao)] # RESETA TABULEIRO
        self.tempo_inicio = time.time() # RESETA TEMPO
        self.tempo_fim = None # RESETA TEMPO DA PARTIDA
        self.jogo_acabou = False # RESETA FLAG JOGO ACABOU
        self.vencedor_linha = None # APAGA LINHA VENCEDOR
        self.jogador_atual = "X" # RESETA JOGADOR PRIMEIRO
        self.oponente = "O" # RESETA OPONENTE
    
    # MENU INICIAL
    def menu_inicial(self):
        while True: # ENQUANTO FOR ATIVO
            self.tela.fill(self.cor_fundo) # COR DO TABULEIRO FUNDO
            fonte_titulo = pygame.font.Font(None, 30) # TAMANHO FONTE TITULO DO MENU

            texto_titulo = fonte_titulo.render("Jogo da Velha", True, self.cor_texto2) # TITULO DO MENU "COR_TEXTO2 SE USAR IMAGEM DO MESTRE"
            texto_titulo_rect = texto_titulo.get_rect(center=(self.largura // 1, self.altura // 8)) # CENTRALIZA TITULO DO MENU
            self.tela.blit(texto_titulo, texto_titulo_rect) # DESENHA TEXTO TITULO MENU

            # Botões centralizados
            botao_largura = 180 # CENTRALIZA NO MEIO HORINZONTAL
            botao_altura = 50 # CENTRALIZA NO MEIO VERTICAL
            centro_x = self.largura # CENTRO DO X
            offset_y = 20 # CENTRO DO Y

            botoes = [
                ("Jogador x CPU", (centro_x - botao_largura // 2, self.altura // 2 - botao_altura - offset_y)), # BOTÃO P1 X CPU
                ("Jogador x Jogador", (centro_x - botao_largura // 2, self.altura // 2)), # BOTÃO P1 X P2
                ("Sair", (centro_x - botao_largura // 2, self.altura // 2 + botao_altura + offset_y)) # BOTÃO SAIR
            ]

            for texto, posicao in botoes: # NO TEXTO E NAS POSIÇÕES DOS BOTÕES
                self.desenhar_botao(texto, posicao, botao_largura, botao_altura) # SE DESENHA O BOTÃO

            for event in pygame.event.get(): # RASTREIA EVENTO DO BOTÃO
                if event.type == pygame.QUIT: # BOTÃO SAIR
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: # RASTREIA BOTÃO
                    pygame.mixer.music.stop()
                    if self.mouse_sobre_botao((centro_x - botao_largura // 2, self.altura // 2 - botao_altura - offset_y), botao_largura, botao_altura): # BOTÃO P1 X CPU
                        self.modo_jogo = "CPU" # SETA P1 X CPU
                        return
                    if self.mouse_sobre_botao((centro_x - botao_largura // 2, self.altura // 2), botao_largura, botao_altura): # BOTÃO P1 X P2
                        self.modo_jogo = "JOGADOR" # SETA P1 X P2
                        return
                    if self.mouse_sobre_botao((centro_x - botao_largura // 2, self.altura // 2 + botao_altura + offset_y), botao_largura, botao_altura): # BOTÃO SAIR
                        pygame.quit()
                        sys.exit()

            pygame.display.flip() # ATUALIZA TELA
    
    ### CPU LOGIC ###
    
    # RASTREIA VITORIA DO JOGADOR NA PROXIMA RODADA
    def verificar_vitoria_iminente(self, jogador):
        # VERIFICA POR LINHA NA DIMENSÃO
        for i in range(self.dimensao):
            linha = [self.tabuleiro[i][j] for j in range(self.dimensao)] # VERIFICA LINHA
            coluna = [self.tabuleiro[j][i] for j in range(self.dimensao)] # VERIFICA COLUNA
            if linha.count(jogador) == self.dimensao - 1 and " " in linha: # SE NA LINHA O JOGADOR FALTA 1 CASA PARA VENCER
                index = linha.index(" ") # RASTREIA LINHA DA POSIÇÃO DO BLOQUEIO
                return i, index 
            if coluna.count(jogador) == self.dimensao - 1 and " " in coluna: # SE NA COLUNA O JOGADOR FALTA 1 CASA PARA VENCER
                index = coluna.index(" ") # RASTREIA COLUNA DA POSIÇÃO DO BLOQUEIO
                return index, i

        # VERIFICAR DIAGONAL PRINCIPAL
        diagonal_principal = [self.tabuleiro[i][i] for i in range(self.dimensao)] # DEFINE DIAGONAL PRINCIPAL
        if diagonal_principal.count(jogador) == self.dimensao - 1 and " " in diagonal_principal:  # SE NA DIAGONAL PRINCIPAL O JOGADOR FALTA 1 CASA PARA VENCER
            index = diagonal_principal.index(" ")  # RASTREIA POSIÇÃO DO BLOQUEIO
            return index, index

        # VERIFICAR DIAGONAL SECUNDÁRIA
        diagonal_secundaria = [self.tabuleiro[i][self.dimensao - 1 - i] for i in range(self.dimensao)] # DEFINE DIAGONAL SECUNDÁRIA
        if diagonal_secundaria.count(jogador) == self.dimensao - 1 and " " in diagonal_secundaria: # SE NA DIAGONAL SECUNDÁRIA O JOGADOR FALTA 1 CASA PARA VENCER
            index = diagonal_secundaria.index(" ")  # RASTREIA POSIÇÃO DO BLOQUEIO
            return index, self.dimensao - 1 - index

        return None

    # JOGA NA POSIÇÃO DA VITORIA DO JOGADOR BLOQUEANDO
    def jogar_em_posicao_vitoria(self, jogador):
        posicao_vitoria = self.verificar_vitoria_iminente(jogador) # SE NA LINHA/COLUNA O JOGADOR FALTAR 1 CASA PARA VENCER
        if posicao_vitoria: # NA POSIÇÃO DA VITORIA DO JOGADOR
            linha, coluna = posicao_vitoria # RASTREIA LINHA/COLUNA
            self.tabuleiro[linha][coluna] = self.oponente # FAZ A JOGADA (CPU) BLOQUEANDO
            return True
        return False

    # JOGA EM UM POSIÇÃO ALEATORIA LIVRE
    def fazer_jogada_aleatoria(self):
        posicoes_disponiveis = [(i, j) for i in range(self.dimensao) for j in range(self.dimensao) if self.tabuleiro[i][j] == " "] # VERIFICA POSIÇÃO LIVRE
        if posicoes_disponiveis: # NAS POSIÇÕES LIVRES
            posicao = random.choice(posicoes_disponiveis) # SORTEIA UMA POSIÇÃO LIVRE
            self.tabuleiro[posicao[0]][posicao[1]] = self.oponente  # FAZ A JOGADA (CPU)

    # ETAPAS DA LOGICA DA JOGADA
    def jogada_computador(self):
        # VERIFICA SE O CPU PODE VENCER NA PRÓXIMA JOGADA
        if self.jogar_em_posicao_vitoria(self.oponente): # FUNÇÃO VITORIA RECEBENDO OPONENTE COMO PARAMETRO
            return

        # VERIFICA SE O JOGADOR PODE VENCER NA PRÓXIMA JOGADA E BLOQUEAR ESSA VITÓRIA
        if self.jogar_em_posicao_vitoria(self.jogador_atual): # FUNÇÃO VITORIA RECEBENDO JOGADOR ATUAL QUE É "O" COMO PARAMETRO
            return

        # FAZER UMA JOGADA ALEATÓRIA
        self.fazer_jogada_aleatoria() # CASO AS DUAS CONDIÇÕES ACIMA NÃO SEJAM VALIDADAS FAZ UMA JOGADA ALEATORIA

    # GAME LOOP PRINCIPAL
    def main(self):
        self.menu_inicial() #INICIA NO MENU
        self.tempo_inicio = time.time() # RESETA TEMPO
        while True: # LOOP PRINCIPAL
            for event in pygame.event.get(): # RASTREIA O EVENTO 
                if event.type == pygame.QUIT: # SELECIONOU BOTÃO SAIR
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: # SELECIONOU BOTÃO JOGAR
                    x, y = pygame.mouse.get_pos() # RASTREIA O MOUSE NO BOTÃO
                    if not self.jogo_acabou: # SE O JOGO NÃO ACABOU
                        if x < self.largura: # SE CLICOU DENTRO DO TABULEIRO
                            linha, coluna = self.obter_movimento(x, y) # OBTEM A JOGADA SELECIONADA
                            if self.tabuleiro[linha][coluna] == " ": # SE ESTIVER VAZIO
                                self.validar_movimento((linha, coluna), self.jogador_atual) # RASTREIA VALIDAÇÃO
                                self.atualizar_jogo() # ATUALIZA GAMEBOARD
                                self.rodada += 1 # SOMA RODADA
                                if self.verificar_vitoria(self.jogador_atual, self.oponente): # VERIFICA VITORIA
                                    self.mensagem_status = f"Jogador {self.jogador_atual} venceu!" # JOGADOR VENCEU
                                    self.jogo_acabou = True # FLAG FIM JOGO
                                    self.tempo_fim = time.time() # PAUSA TEMPO
                                if not self.jogo_acabou and all(all(celula != " " for celula in linha) for linha in self.tabuleiro): # SE NÃO VENCEU E TODAS AS CASAS ESTÃO OCUPADAS
                                    self.mensagem_status = "Empate!" # EMPATE
                                    self.jogo_acabou = True # FLAG FIM JOGO
                                    self.tempo_fim = time.time() # PAUSA TEMPO
                                if not self.jogo_acabou and self.modo_jogo == "JOGADOR": # SE O JOGO NÃO ACABOU E MODO DE JOGO É P1 X P2
                                    self.jogador_atual, self.oponente = self.oponente, self.jogador_atual # ALTERNA O JOGADOR POR RODADA
                                if not self.jogo_acabou and self.modo_jogo == "CPU": # SE O JOGO NÃO ACABOU E MODO DE JOGO É P1 X CPU
                                    self.jogada_computador() # CPU JOGA
                                    self.rodada += 1 # SOMA RODADA
                                    if self.verificar_vitoria(self.oponente, self.jogador_atual): # RASTREIA VITORIA CPU
                                        self.mensagem_status = "CPU venceu!" # CPU VENCEU
                                        self.jogo_acabou = True # FLAG FIM DE JOGO
                                        self.tempo_fim = time.time() # PAUSA TEMPO
                                        
                    else: # SE O JOGO ACABOU
                        if self.mouse_sobre_botao((self.largura + 50, self.altura // 2 - 25), 180, 50): # RASTREIA MOUSE BOTÃO JOGAR NOVAMENTE
                            self.reiniciar_jogo() # FLAG REINICIA TABULEIRO
                        if self.mouse_sobre_botao((self.largura + 50, self.altura // 2 + 50), 180, 50): # RASTREIA MOUSE BOTÃO MENU
                            self.reiniciar_jogo() # FLAG REINICIA TABULEIRO
                            self.menu_inicial() # MENU GATILHO

            self.desenhar_tabuleiro() # ENQUANTO LOOP FOR ATIVO
            self.desenhar_movimentos() # ENQUANTO LOOP FOR ATIVO
            self.desenhar_informacoes() # ENQUANTO LOOP FOR ATIVO
            if self.jogo_acabou: # SE O JOGO ACABOU
                self.desenhar_botao("Jogar Novamente", (self.largura + 50, self.altura // 2 - 25), 180, 50) # BOTÃO JOGAR NOVAMENTE
                self.desenhar_botao("Menu", (self.largura + 50, self.altura // 2 + 50), 180, 50) # BOTÃO MENU
            pygame.display.flip() # ATUALIZA DISPLAY

# MÓDULO PARA IMPORTAÇÃO
if __name__ == "__main__":
    JogoDaVelha().main()


import pygame, random, datetime

#bola - 30 x 30 - 22.5 x 22.5
#paddle - 10 x 140

#! Classes
class Bola(pygame.sprite.Sprite):
    def __init__(self, dir_x, dir_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Ping_pong/Ball.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.75)
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.mask = pygame.mask.from_surface(self.image)
        self.dir_x = 1
        self.dir_y = 1
        self.vel_x = dir_x * 4
        self.vel_y = dir_y * random.randint(2, 5)
        self.som_ponto = pygame.mixer.Sound('Ping_pong/score.ogg')
        self.som_batida = pygame.mixer.Sound('Ping_pong/pong.ogg')
        
    def rebater_jogador(self):
        colisao = pygame.sprite.spritecollide(self, grupo_jogador, False, pygame.sprite.collide_mask)
        if colisao:
            self.som_batida.play()
            self.vel_x *= 1.1
            self.vel_x *= -self.dir_x
            self.vel_y *= 1.05
            
    def ponto(self):
        global pontos_j1, pontos_j2, dir_bola_x, rodada_ativa, fim_de_jogo,jogo_ativo
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - 22.5:
            if self.rect.x <= 0:
                pontos_j2 += 1
                dir_bola_x = -1
            elif self.rect.x >= SCREEN_WIDTH - 22.5:
                pontos_j1 +=1
                dir_bola_x = 1
            self.som_ponto.play()
            self.kill()
            rodada_ativa = False
            if pontos_j1 >= 5 or pontos_j2 >= 5:
                fim_de_jogo = True
                rodada_ativa = False
                jogo_ativo = False
        
    def mover(self):
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - 22.5: self.vel_x *= -self.dir_x
        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT - 22.5: self.vel_y *= -self.dir_y
        self.rect.x -= self.vel_x
        self.rect.y -= self.vel_y
        
    def update(self):
        self.mover()
        self.rebater_jogador()
        self.ponto()
     
class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Ping_pong/Paddle.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.75)
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.vel = 5
        self.pos_init = pos_x
        
    def mover(self):
        keys = pygame.key.get_pressed()
        if self.rect.top <= 0: self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT
        
        if self.pos_init == 10:
            if keys[pygame.K_w]: self.rect.y -= self.vel
            if keys[pygame.K_s]: self.rect.y += self.vel
        elif self.pos_init == SCREEN_WIDTH - 10 :
            if keys[pygame.K_UP]: self.rect.y -= self.vel
            if keys[pygame.K_DOWN]: self.rect.y += self.vel
        
    def update(self):
        self.mover()    

def mostrar_mensagem(msg, pos_x, pos_y):
    surface = font.render(f'{msg}', False, cinza_claro)
    
    if pos_x == SCREEN_WIDTH/2:
        surface = pygame.transform.scale(surface, (surface.get_width()*2, surface.get_height()*2))
    rect = surface.get_rect(center = (pos_x, pos_y))
    screen.blit(surface, rect)

#! Variáveis
cinza_claro = (217,215,214)
preto = (19,24,15)
jogo_ativo = False
rodada_ativa = False
fim_de_jogo = False
pontos_j1 = 0
pontos_j2 = 0
dir_bola_y = [-1,1]
dir_bola_x = 1

#! Cronômetro
tempo_atual = 0
tempo_msg = 0

#! General Setup
pygame.init()
clock = pygame.time.Clock()

#! Game Screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
font = pygame.font.SysFont('comicsans', 25, True)

#! Bola
grupo_bola = pygame.sprite.Group()

#! Jogador
grupo_jogador = pygame.sprite.Group()
jogador_1 = Jogador(10, SCREEN_HEIGHT/2)
jogador_2 = Jogador(SCREEN_WIDTH - 10, SCREEN_HEIGHT/2)
grupo_jogador.add(jogador_1)
grupo_jogador.add(jogador_2)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.KEYDOWN:
            if fim_de_jogo == False:
                if jogo_ativo == False and event.key == pygame.K_SPACE:
                    tempo_init = datetime.datetime.now()
                    bola = Bola(dir_bola_x, random.choice(dir_bola_y))
                    grupo_bola.add(bola)
                    jogo_ativo = True
                    rodada_ativa = True
                elif rodada_ativa == False and event.key == pygame.K_SPACE:
                    bola = Bola(dir_bola_x, random.choice(dir_bola_y))
                    grupo_bola.add(bola)
                    rodada_ativa = True
            elif event.key == pygame.K_SPACE:
                tempo_init = datetime.datetime.now()
                pontos_j1 = 0
                pontos_j2 = 0
                fim_de_jogo = False
            
    screen.fill(preto)
    mostrar_mensagem(f'{tempo_msg}s', (SCREEN_WIDTH-50), 40)
    pygame.draw.line(screen, cinza_claro, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
    grupo_bola.draw(screen)
    grupo_jogador.draw(screen)
            
    if jogo_ativo:    
        tempo_atual = datetime.datetime.now() - tempo_init
        tempo_msg = tempo_atual.seconds
        mostrar_mensagem(pontos_j1,(SCREEN_WIDTH/2 -20), SCREEN_HEIGHT/2)
        mostrar_mensagem(pontos_j2, (SCREEN_WIDTH/2 +20), SCREEN_HEIGHT/2)
        grupo_bola.update()
        grupo_jogador.update()
    else:
        mostrar_mensagem('Press Space to Start', SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        
    if fim_de_jogo:
        screen.fill(preto)
        if pontos_j1 >= 5: mostrar_mensagem(f'Jogador 1 ganhou de {pontos_j1} à {pontos_j2}', SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        else: mostrar_mensagem(f'Jogador 2 ganhou de {pontos_j2} à {pontos_j1}', SCREEN_WIDTH/2, SCREEN_WIDTH/2)
        
    pygame.display.update()
    
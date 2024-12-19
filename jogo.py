from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController 
from random import uniform 

app = Ursina()

# Criar o chão do jogo
chao = Entity(
    model='plane',                      # Modelo de plano
    texture='grass',                    # Textura de grama
    collider='mesh',                    # Colisor para detectar colisões
    scale=(100, 1, 100)                 # Dimensões do chão
)

# Configuração do jogador
jogador = FirstPersonController(collider='box')  
jogador.cursor.visible = False 

# Elementos do ambiente
caixa = Entity(
    model='cube',                       # Modelo de cubo
    color=color.black,                  # Cor preta
    collider='box',                     # Colisor do tipo caixa
    position=(15, 0.5, 5)               # Posição no mundo
)
bola = Entity(
    model='sphere',                     # Modelo de esfera
    color=color.red,                    # Cor vermelha
    collider='sphere',                  # Colisor do tipo esfera
    position=(5, 0.5, 10)               # Posição no mundo
)

ceu = Sky()
nivel = 1

blocos = []
direcoes = [] 
window.fullscreen = True
for i in range(10):
    r = uniform(-2, 2)
    bloco = Entity(
        position=(r, 1 + i, 3 + i * 5),
        model='cube',
        texture='white_cube',
        color=color.azure,
        scale=(3, 0.5, 3),
        collider='box',
    )
    blocos.append(bloco) 
    direcoes.append(1 if r < 0 else -1)  

meta = Entity(
    color=color.gold,
    model='cube',
    texture='white_cube',
    position=(0, 11, 55),
    scale=(10, 1, 10),
    collider='box'
)
pilar = Entity(
    color=color.green,
    model='cube',
    position=(0, 36, 58),
    scale=(1, 50, 1)
)

# Adicionar sons ao jogo
som_pulo = Audio('assets/jump.mp3', loop=False, autoplay=False)
som_caminhada = Audio('assets/walk.mp3', loop=False, autoplay=False) 

# Configurar uma arma para o jogador
arma = Entity(
    model='assets/AK47.obj',
    scale=0.01,
    position=(0.6, -0.6, 1.5),
    rotation=(0, -70, 5),
    parent=camera.ui,                   # Vincular à câmera
    texture='assets/color.tga',         # Textura colorida
    normal_map='assets/normal.tga',     # Mapa de textura normal
    specular_map='assets/specular.tga'  # Mapa de reflexão especular
)

# Criar alvos para o jogador
alvos = []
for i in range(5): 
    alvo = Entity(
        model='cube',
        color=color.red,
        scale=(1, 1, 1),
        position=(uniform(-20, 20), 1, uniform(10, 40)),  # Posição aleatória
        collider='box'
    )
    alvos.append(alvo)

# Função para disparar
def disparar():
    # Calcular a posição inicial do projétil
    posicao_inicial = camera.ui.get_position(relative_to=scene) + Vec3(0.9, -0.5, 0)
    
    # Direção do disparo (sempre para frente)
    direcao_disparo = camera.forward.normalized()

    # Criar o projétil
    projétil = Entity(
        model='sphere',
        color=color.yellow,
        scale=1,
        position=posicao_inicial,
        collider='box',
        always_on_top=True
    )

    # Animar o movimento do projétil
    projétil.animate_position(
        projétil.position + direcao_disparo * 50,
        duration=0.2,
        curve=curve.linear
    )

    # Destruir o projétil após 1 segundo
    destroy(projétil, delay=1)

    # Verificar colisões com os alvos
    for alvo in alvos:
        if projétil.intersects(alvo).hit: 
            destroy(alvo)
            alvos.remove(alvo)

# Função de atualização contínua do jogo
def update():
    global nivel
    for i, bloco in enumerate(blocos):
        bloco.x -= direcoes[i] * time.dt
        if abs(bloco.x) > 5: 
            direcoes[i] *= -1
        if bloco.intersects().hit:
            jogador.x -= direcoes[i] * time.dt
    
    # Atualizar o nível do jogo
    if jogador.z > 56 and nivel == 1:
        nivel = 2
        ceu.texture = 'sky_sunset'  # Alterar o céu para um pôr do sol

    # Reproduzir som de caminhada
    caminhando = held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']
    if caminhando and jogador.grounded:
        if not som_caminhada.playing:
            som_caminhada.play()
    else:
        if som_caminhada.playing:
            som_caminhada.stop()

# Função para lidar com entradas do jogador
def input(tecla):
    if tecla == 'q':  # Pressionar 'q' para sair
        quit()
    if tecla == 'space':  # Pressionar 'espaço' para pular
        if not som_pulo.playing:
            som_pulo.play()
    if tecla == 'left mouse down':  # Pressionar botão esquerdo do mouse para disparar
        disparar()

# Iniciar o jogo
app.run()

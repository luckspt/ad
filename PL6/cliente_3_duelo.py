from kazoo.client import KazooClient
from kazoo.recipe.barrier import DoubleBarrier
from time import sleep

# Criar um ZooKeeper handler
zh = KazooClient()
zh.start()

barrier = DoubleBarrier(zh, '/DUELO', 2)
print('Vou iniciar o jogo')

barrier.enter()
print('O jogo vai começar')

while True:
    try:
        print('A jogar')
        sleep(1)
    except KeyboardInterrupt:
        break

print('Vou encerrar a minha participação no jogo')
barrier.leave()

print('O jogo foi encerrado.\nA sua pontuação foi X.')

# restante do programa
zh.stop()
zh.close()

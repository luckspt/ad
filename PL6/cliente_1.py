from kazoo.client import KazooClient
from time import sleep


def critical_zone():
    print('Comecei a executar a zona crítica')
    sleep(10)
    print('Terminei a execução da zona crítica')


# Criar um ZooKeeper handler
zh = KazooClient()
zh.start()

zh.ensure_path('/LOCKS')
zid = zh.create('/LOCKS/L-', ephemeral=True, sequence=True)
print('My id:', zid)

while True:
    children = zh.get_children('/LOCKS')
    min_id = f'/LOCKS/{min(children)}'

    if zid == min_id:
        critical_zone()
        zh.delete(zid)
        break
    else:
        print('Children:', children)
        sleep(1)

# restante do programa
zh.stop()
zh.close()

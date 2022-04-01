from kazoo.client import KazooClient

# Criar um ZooKeeper handler
zh = KazooClient()
zh.start()

zh.ensure_path('/PAI')


@zh.DataWatch('/NORMAL')
def watch_node(data, stat):
    print("Stat: %s\nData: %s\n" % (stat, data))


@zh.ChildrenWatch('/PAI')
def watch_children(children):
    print("Children are now: %s" % children)


while True:
    pass

# restante do programa
zh.stop()
zh.close()

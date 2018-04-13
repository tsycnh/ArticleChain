import hashlib

'''
区块结构：区块头（前一个区块的hash + nonce）+ 数据
区块规则：区块哈希值以666开头
'''

class Block():
    def __init__(self,data='',previous_block_hash=''):
        self.data = data
        self.previous_block_hash = previous_block_hash
        self.nonce = None
        self._hash = ''

    # 计算当前块的哈希值
    def hash(self):
        m = hashlib.sha256()
        m.update(str(self.previous_block_hash).encode('utf-8'))
        m.update(str(self.nonce).encode('utf-8'))
        m.update(str(self.data).encode('utf-8'))
        self._hash = m.hexdigest()
        return self._hash

    # 挖矿！规则是当前区块的哈希值以666开头
    def mine(self):
        current_nonce = 0
        while not self._hash.startswith('666'):
            current_nonce += 1
            self.nonce = current_nonce
            self.hash()
        print('挖到矿啦！hash:%sd nonce:%d'%(self._hash,self.nonce))

# 区块类
class BlockChain():
    def __init__(self):
        self.blocks=[]

    # 新增一个区块到当前链
    def add_block(self,block):
        if block.hash().startswith('666'):
            if len(self.blocks)<=0:
                self.blocks.append(block)# 创世块
            else:
                if block.previous_block_hash == self.get_last_block_hash():
                    self.blocks.append(block)
                else:
                    print('父块哈希值错误！')

    def get_last_block_hash(self):
        return self.blocks[-1].hash()

    def check_status(self):
        print('区块链长度：%d,最新区块哈希值：%s'%(len(self.blocks),self.get_last_block_hash()))

if __name__ =='__main__':
    god_block = Block(data='Hey there')
    god_block.mine()
    mini_chain = BlockChain()
    mini_chain.add_block(god_block)

    for i in range(10):
        father_hash = mini_chain.get_last_block_hash()
        b = Block(data='test',previous_block_hash=father_hash)
        b.mine()
        mini_chain.add_block(b)
    mini_chain.check_status()
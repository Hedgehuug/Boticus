



from pandas import DataFrame as df
import time
import configparser
p = []
l = []
config = configparser.ConfigParser()
config.read(r"OpenOrders.ini")
coinlist = config['coinslist']
tok = config['openOrders']
#tok = dict(tok)
tok = {a:int(b) for a,b in tok.items()}
blok = dict(tok)
zok = list(config['coinslist']['coinlist'].split(','))


for line in zok:
    if(line.lower() in (x for x in tok.keys())):
        print(line)
        l.append(line)
    else:
        p.append(line)
        blok.update({line.lower():0})
        
        
config['openOrders'] = blok
with open('OpenOrders.ini','w') as configfile:
    config.write(configfile)
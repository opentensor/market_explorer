import bittensor
import os
from concurrent.futures import ThreadPoolExecutor

sub = bittensor.subtensor( network = 'local' )
graph = bittensor.metagraph( subtensor = sub )
block = sub.get_current_block()
graph.sync()
graph.save_to_path( path = os.path.expanduser('~/'), filename = 'nakamoto-{}'.format( block ) )
graph.save_to_path( path = os.path.expanduser('~/'), filename = 'nakamoto-latest')

bittensor.logging( debug = True )
wallet = bittensor.wallet( name = 'const', hotkey = 'Nero')
dend = bittensor.dendrite( wallet = wallet )

resps = []
codes = []
times = []

def make_query( end ):
    resp, code, time = dend.forward_text( endpoints = end, inputs = "hello world" )
    resps.append( resp[0] ) 
    codes.append( code.item())
    times.append( time.item() )

with ThreadPoolExecutor(max_workers=100) as executor:
    for end in graph.endpoints:
        executor.submit(make_query, end)

json_data = {}
for e, r, c, t in list(zip( graph.endpoint_objs, resps, codes, times)):
    json_data[e.uid] = {'uid': e.uid, 'code': c, 'time': t}

import json
with open( os.path.expanduser('~/query-latest.json'), 'w') as f:
    json.dump(json_data, f)

with open( os.path.expanduser('~/query-{}.json'.format( block )), 'w') as f:
    json.dump(json_data, f)
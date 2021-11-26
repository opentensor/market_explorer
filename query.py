import bittensor
import os

sub = bittensor.subtensor( network = 'local' )
graph = bittensor.metagraph( subtensor = sub )
graph = bittensor.metagraph().load_from_path( os.path.expanduser('~/nakamoto-latest') )

bittensor.logging( debug = True )
wallet = bittensor.wallet()
dend = bittensor.dendrite( wallet = wallet )
resp, codes, times = dend.forward_text( endpoints = graph.endpoints, inputs = "hello world" )

json_data = {}
for e, r, c, t in list(zip( graph.endpoint_objs, resp, codes.tolist(), times.tolist() )):
    json_data[e.uid] = {'uid': e.uid, 'code': c, 'time': t}

import json
with open( os.path.expanduser('~/query-latest.json'), 'w') as f:
    json.dump(json_data, f)

with open( os.path.expanduser('~/query-{}.json'.format( sub.get_current_block() )), 'w') as f:
    json.dump(json_data, f)
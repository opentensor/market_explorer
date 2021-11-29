import os
import bittensor
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

frames = {}
def load_graph_file( filename ):
    block = int(filename.split('-')[1])
    graph = bittensor.metagraph().load_from_path( os.path.expanduser( '~/data/{}'.format(filename) ) )
    dataframe = pd.DataFrame(columns=['uid', 'active', 'stake','rank','trust', 'consensus', 'incentive', 'dividends', 'emission'], index=graph.uids.tolist())
    for uid in graph.uids.tolist():
        dataframe.loc[uid] = pd.Series({
                'uid':uid, 
                'active': graph.active[uid].item(), 
                'stake':graph.S[uid].item(), 
                'rank':graph.R[uid].item(), 
                'trust':graph.T[uid].item(), 
                'consensus':graph.C[uid].item(), 
                'incentive':graph.I[uid].item(), 
                'dividends':graph.D[uid].item(), 
                'emission':graph.E[uid].item(),
            })
        frames[block] = dataframe


block_step = 1000
sub = bittensor.subtensor()
all_files = os.listdir(os.path.expanduser('~/data'))
block_range = [ block for block in range( 0, sub.get_current_block(), block_step ) ]
with ThreadPoolExecutor(max_workers=100) as executor:
    for block in tqdm( block_range ):
        block_filename = 'nakamoto-{}'.format( block ) 
        if block_filename in all_files:
            executor.submit( load_graph_file, block_filename )

blocks = pd.Series([f for f in frames.values()], index=frames.keys())
blocks.to_pickle(os.path.expanduser('~/data/all_blocks.pd')) 
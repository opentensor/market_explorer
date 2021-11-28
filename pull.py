import os
import bittensor
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

n_processes = 1
n_threads = 1
step_size = 10000

def pull_graph_at_block( block ):
    print ('pulling block: {}'.format( block ))
    while True:
        try:
            sub = bittensor.subtensor( network = 'nakamoto' )
            graph = bittensor.metagraph( subtensor = sub )
            graph.sync( block )
            # 99% pulled
            if sum( [ 1 for hotkey in graph.hotkeys if hotkey != '' ]) / graph.n.item() > 0.99:
                graph.save_to_path( path = os.path.expanduser('~/data/'), filename = 'nakamoto-{}'.format( block ) )
                print ('finished pulling block: {}'.format( block ))
                break
            else:
                print ('restarting pulling block: {}'.format( block ))
                continue
        except:
            print ('restarting pulling block: {}'.format( block ))
            continue

def multithread_pull_range( block_range ):
    with ThreadPoolExecutor( max_workers=10 ) as executor:
        for block in tqdm( block_range ):
            executor.submit( pull_graph_at_block, block )

def run( block_ranges ):
    with ProcessPoolExecutor( max_workers=10 ) as executor:
        for block_range in tqdm( block_ranges ):
            executor.submit( multithread_pull_range, block_range )

def run_linear( blocks ):
    for block in tqdm( blocks) :
        pull_graph_at_block( block )

if __name__ == "__main__":
    # Get already pulled metagraphs.
    all_files = os.listdir(os.path.expanduser('~/data/'))
    already_pulled_blocks = set()
    for file in all_files:
        if file[:4] == 'naka':
            try:
                already_pulled_blocks.add( int(file.split('-')[1]) )
            except:
                pass

    sub = bittensor.subtensor()
    all_ranges = []
    block_range_size = 5
    current_range = []
    for block in range( 0, sub.get_current_block(), step_size ):
        if block not in already_pulled_blocks:
            if len(current_range) == block_range_size:
                all_ranges.append( current_range )
                current_range = []
            current_range.append( block )

    if n_threads == 1 and n_processes == 1:
        run_linear( sum(all_ranges, []) )
    else:
        run( all_ranges )
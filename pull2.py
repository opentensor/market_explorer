

import os
import bittensor
import time
from termcolor import colored
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

n_thread = 10
n_proc = 5
block_range_size = 5
step_size = 10000
neurons = {}

def get_n_for_block( block ):
    while True:
        try:
            sub = bittensor.subtensor( network = 'nakamoto' )
            return sub.get_n()
        except:
            continue

def neuron_for_block_and_uid( block, uid ):
    while True:
        try:
            sub = bittensor.subtensor( network = 'nakamoto' )
            neuron = sub.neuron_for_uid( uid = uid, block = block )
            print (colored('o: {}'.format(uid), 'green'))
            return neuron
        except Exception as e:
            print (colored('x: {}'.format(uid), 'red'))

def pull_neurons_at_block( block ):
    if block not in neurons:
        neurons[ block ] = {}
    for uid in range( get_n_for_block( block ) ):
        neurons[block][uid] = neuron_for_block_and_uid( block, uid )

def multithread_pull_range( block_range ):
    with ThreadPoolExecutor( max_workers=n_thread ) as executor:
        for block in tqdm( block_range ):
            executor.submit( pull_neurons_at_block, block )

def run( block_ranges ):
    with ProcessPoolExecutor( max_workers=n_proc ) as executor:
        for block_range in tqdm( block_ranges ):
            executor.submit( multithread_pull_range, block_range )

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
    current_range = []
    for block in range( 1000, sub.get_current_block(), step_size ):
        if block not in already_pulled_blocks:
            if len(current_range) == block_range_size:
                all_ranges.append( current_range )
                current_range = []
            current_range.append( block )

    run( all_ranges )

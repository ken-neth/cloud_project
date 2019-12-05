import time
from celery import group
from celery.result import ResultSet
from container_app.tasks import run
from container_app.tasks import add
from container_app.tasks import check

import argparse

import numpy as np

parser = argparse.ArgumentParser(
    description="cloud computing CND",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--N",
    default=2,
    type=int,
    help="Number of VMs",
)
parser.add_argument(
    "--D",
    default=32,
    type=int,
    help="Difficulty level"
)

def split_nonce_set(N):

    subsets = []

    base = np.uint32(4294967296 //N)

    for thread_id in range(N):
        minimum = base*thread_id
        maximum = minimum + base
        if (thread_id == N-1):
            maximum = 4294967296
#         print("Thread " + str(thread_id) + (" takes min: %s and max: %s" % (minimum, maximum)))
        subsets.append([thread_id, int(minimum), int(maximum)])

    print("\n done splitting")
    return subsets


def main(args):

    sections = split_nonce_set(args.N)

    start_time = time.time()

    # result = group(add.si(i, args.D, sections[i][1], sections[i][2]) for i in range(args.N))
    # result_output = ResultSet([run.delay(i, args.D, sections[i][1], sections[i][2]) for i in range(args.N)])
    # result_output = result.apply_async()
    # result_output = result_output.wait(timeout=None, interval=0.5)

    # result_output = result_output.get()  # wait for all to finish
    # print(f'Last scheduled task result: {result_output[0]}, {result_output[1]}, {result_output[2]}, {result_output[3]}')
    exit = 0
    golden = 0
    for n in range(args.N):
        if exit:
            break
        for nonce in range(sections[n][1], sections[n][2]):
            result = check.delay("COMSM0010cloud", nonce, args.D)
            result_output = result.get()
            if result_output :
                exit = 1
                golden = nonce
                break
    # result_output = result.wait(timeout=None, interval=0.5)
    print(f'Last scheduled task result: {nonce}')
    elapsed_time = time.time() - start_time
    print(f"elapsed time: {elapsed_time}")


if __name__ == '__main__':
    main(parser.parse_args())

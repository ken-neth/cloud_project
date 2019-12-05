import time
from billiard import current_process
import hashlib
from .sellerie import app

exit_Flag = 0

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string).hexdigest()
    return sha_signature

def is_golden(hash_string, D): # D for difficulty level
    # return not any(bin(int(hash_string,16))[-D:])
    # return not any('{:0256b}'.format(int(hash_string,16))[:D])
    return list('{:0256b}'.format(int(hash_string,16))[:D]) == ['0'] * D

def test_nonces(threadName, block, minimum, maximum, D):

    found = 0
    golden_nonce = 0

    test_range = (maximum-1)-minimum
    percentage = 0

    for nonce in range(minimum, maximum):
        # if exit_Flag:
        #      threadName.exit()

        hash_result = encrypt_string((str(block) + str(nonce)).encode())
        # result = encrypt_string(block + ('0x%08X' % np.uint32(nonce)))
        if(is_golden(hash_result, D)):
            print("nonce = %s \n hash = %s \n bin = %s \n leading = %s" % (nonce, hash_result,'{:0256b}'.format(int(hash_result,16)), '{:0256b}'.format(int(hash_result,16))[:D]))
            found = 1
            golden_nonce = nonce
            exitFlag = 1
            break

        new_percentage = ((nonce - minimum)/test_range) * 100
        if(new_percentage > percentage+1):
            percentage += 1
            print("\n %s is %s percent complete.\n hash = %s \n bin = %s \n leading = %s" % (threadName, percentage, hash_result,'{:0256b}'.format(int(hash_result,16)), '{:0256b}'.format(int(hash_result,16))[:D]))


    return (found, golden_nonce)

@app.task
def run(id_, D, min, max):
    print('-------> parallel task started %s' % id_)
    print('id: %s | D: %s | min: %s | max: %s' %(id_, D, min, max))
    output = test_nonces(id_, "COMSM0010cloud", min, max, D)
    result = 0
    if output[0]:
        print("Golden nonce found: %s" % (output[1]))
        result = output[1]
    print('-------> parallel task complete %s' % id_)
    return result

@app.task
def check(block, nonce, D):
    hash_result = encrypt_string((str(block) + str(nonce)).encode())
    found = 0
    if(is_golden(hash_result, D)):
        print("nonce = %s \n hash = %s \n bin = %s \n leading = %s" % (nonce, hash_result,'{:0256b}'.format(int(hash_result,16)), '{:0256b}'.format(int(hash_result,16))[:D]))
        found = 1
    return found

@app.task
def add(a, b):
    time.sleep(3)
    result = a + b
    print(f"result of {a} + {b} = {result}")
    return result

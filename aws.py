import boto.ec2
import sys
import os
import argparse

# specify AWS keys
auth = {"aws_access_key_id": "ASIAZBT5P24ZH4KRRBMR", "aws_secret_access_key": "NpseTRlm9x6IODkmQNSNOOjTFYd8nESvkK3Q8522"}

# args definitions
parser = argparse.ArgumentParser(
    description="cloud computing CND",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--start",
    default=0,
    type=int,
    help="Just start the vm"
)
parser.add_argument(
    "--stop",
    default=0,
    type=int,
    help="Just stop the vm"
)
parser.add_argument(
    "--N",
    default=1,
    type=int,
    help="Number of VMs",
)
parser.add_argument(
    "--D",
    default=32,
    type=int,
    help="Difficulty level"
)


def main(args):
    if args.start and args.stop:
	       print("Usage: force start OR stop not both\n")
	       sys.exit(0)

    if args.start:
	    startInstance(args.N, args.D)
    if args.stop:
    	stopInstance()




def startInstance(N, D):
    print("Starting the instance...")

    # change "eu-west-1" region if different
    try:
        ec2 = boto.ec2.connect_to_region("us-east-1", **auth, security_token=os.environ.get('AWS_SESSION_TOKEN', None))

    except Exception as e1:
        error1 = "Error1: %s" % str(e1)
        print(error1)
        sys.exit(0)

    # change instance ID appropriately
    try:
         ec2.start_instances(instance_ids="i-078f12dd0854c092e")

    except Exception as e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

    print("Instance starting with %s and %s" % (N, D))

def stopInstance():
    print("Stopping the instance...")

    try:
        ec2 = boto.ec2.connect_to_region("us-east-1", **auth, security_token=os.environ.get('AWS_SESSION_TOKEN', None))

    except Exception as e1:
        error1 = "Error1: %s" % str(e1)
        print(error1)
        sys.exit(0)

    try:
         ec2.stop_instances(instance_ids="i-078f12dd0854c092e")

    except Exception as e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

if __name__ == '__main__':
    main(parser.parse_args())

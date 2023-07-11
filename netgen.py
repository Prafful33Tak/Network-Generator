#!/usr/bin/env python

import sys
import subprocess


# Function to run the iperf command
def run_iperf_command(iperf_command: list) -> None:
    # Check if the command is valid
    if len(iperf_command) < 2 or iperf_command[0] != './netgen.py':
        raise ValueError('Invalid command')

    # Extract the iperf3 command from the input
    iperf_command = iperf_command[1:]

    # Check if the iperf3 command is valid
    if not is_iperf_command_valid(iperf_command):
        raise ValueError('Invalid iperf3 command')

    try:
        # Redirect the output to log.txt
        with open('log_1700_5_30.txt', 'w') as logfile:
            result = subprocess.run(['./iperf3'] + iperf_command, stdout=logfile, stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as e:
        print('An error occurred:', str(e))
        sys.exit(1)
    except OSError as e:
        print('An error occurred while executing the iperf3 command:', str(e))
        sys.exit(1)
    except Exception as e:
        print('An error occurred:', str(e))
        sys.exit(1)



# Function to check if the iperf3 command is valid or not
def is_iperf_command_valid(iperf_command: list) -> bool:
    valid_options = [
        '-c', '-s', '-p', '-u', '-t', '-i', '-f', '-P', '-R', '-w', '-C', '-n', '-b', '-k', '-l', '-L', '-V', '-Z',
        '--bind', '--client', '--server', '--port', '--udp', '--time', '--interval', '--format', '--parallel', '--reverse',
        '--window', '--compatibility', '--bytes', '--blockcount', '--len', '--lenmax', '--lenmin', '--print_mss', '--verbose', '--no-delay',
        '--get-server-output', '--json', '--logfile', '--forceflush', '--title', '--set-version', '--zerocopy',
        '--ipv6-version', '--udp-counters-64bit', '--repeating-payload', '--bidir', '--reverse-direction', '--connect-timeout',
        '--fq-rate', '--fq-udp-rate', '--ipv6-fq-rate', '--ipv6-fq-udp-rate', '--fq-rate-avg-interval', '--fq-rate-interval-top',
        '--fq-rate-interval-hist', '--fq-rate-interval-all', '--no-fq-rate-interval', '--fq-rate-latency', '--fq-rate-loss', '--fq-rate-jitter',
        '--fq-rate-drop', '--fq-rate-pacing', '--fq-rate-loss-correlation', '--fq-rate-loss-interval', '--fq-rate-pacing-interval',
        '--stream-records', '--bidir-unique-streams', '--rxhistogram', '--txhistogram', '--ciphers', '--client-chaining',
        '--server-chaining', '--cipher', '--null-cipher', '--zerocopy-read', '--zerocopy-write', '--version', '--help'
    ]

    for i in range(len(iperf_command)):
        if i == 0 and (iperf_command[i] not in valid_options):
            return False
        elif (iperf_command[i-1] in ['-u', '-s']) and (iperf_command[i] not in valid_options):
            return False
        elif (iperf_command[i-1] not in ['-u', '-s']) and (iperf_command[i-1] not in valid_options) and (iperf_command[i] not in valid_options):
            return False

    return True



if __name__ == '__main__':
    try:
        run_iperf_command(sys.argv[:])
    except ValueError as e:
        print('Error:', str(e))
        sys.exit(1)

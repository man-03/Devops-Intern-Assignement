import os
import time
import signal
import logging
from collections import Counter

# Set up logging
logging.basicConfig(filename='log_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Function to handle Ctrl+C signal
def signal_handler(sig, frame):
    print('\nMonitoring stopped.')
    logging.info('Monitoring stopped.')
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Function to monitor log file
def monitor_log(log_file):
    try:
        with open(log_file, 'r') as f:
            # Move pointer to the end of the file
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line:
                    yield line
                else:
                    time.sleep(0.1)
    except FileNotFoundError:
        print(f'File {log_file} not found. Exiting.')
        logging.error(f'File {log_file} not found.')
        exit(1)
    except Exception as e:
        print(f'An error occurred: {e}')
        logging.error(f'Error: {e}')
        exit(1)

# Function to perform log analysis
def analyze_log(log_file):
    try:
        keywords = ['error', 'exception']  # Add more keywords for analysis if needed
        error_count = Counter()

        for line in monitor_log(log_file):
            for keyword in keywords:
                if keyword in line.lower():
                    error_count[keyword] += 1

            # Log the entry
            logging.info(line.strip())

            # Print summary report
            if len(error_count) > 0:
                print('\nError Summary:')
                for keyword, count in error_count.items():
                    print(f'{keyword.capitalize()}: {count}')
    except KeyboardInterrupt:
        print('\nMonitoring stopped.')
        logging.info('Monitoring stopped.')
        exit(0)

if __name__ == '__main__':
    log_file = 'example.log'  # Change this to your log file
    print(f'Monitoring log file: {log_file}')
    logging.info(f'Monitoring log file: {log_file}')

    # Start log analysis
    analyze_log(log_file)

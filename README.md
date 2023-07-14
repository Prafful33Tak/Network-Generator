# Network Traffic Generator

This project is a `network traffic generator` that uses `iperf3` to execute commands and analyze the throughput data. It includes a script to run iperf3 commands, a script for throughput analysis, and an HTML template for generating a throughput report.


## Prerequisites

- Python 3.x
- iperf3 (installed and accessible from the command line)
- Dependencies: pandas, matplotlib, and Jinja2 (can be installed using pip)


## Installation

1. Clone the repository or download the code files into a directory.

2. Make sure iperf3 is present in the same directory as the other files.
   
3. Make sure log_files folder is present in the same directory
   
4. Install the Python dependencies by running the following command: `pip install pandas matplotlib jinja2`


## Usage

1. Open a terminal or command prompt and navigate to the project directory.

2. Execute the network traffic generator script by running the following command: `python netgen.py <iperf3 command>`.
- Replace `<iperf3 command>` with the desired iperf3 command and its arguments.
- For example: `python netgen.py -c <server_ip> -t 10`.
- This will run the iperf3 command specified and save the output in the `log_files/log.txt` file.

3. Run the throughput analysis script by executing the following command : `python throughput_analysis.py`.
- This script will read the log file, analyze the throughput data, generate graphs, calculate statistical measures, and generate an HTML report.

4. After executing the throughput analysis script, a file named `throughput_report.html` will be generated, containing the final throughput report.

![image](https://github.com/Prafful33Tak/Network-Generator/assets/88709400/c0aa41ef-d95d-46f1-9114-7b48df3683d1)
![image](https://github.com/Prafful33Tak/Network-Generator/assets/88709400/9405770c-545f-4a72-b98e-f6314a265899)
![image](https://github.com/Prafful33Tak/Network-Generator/assets/88709400/14b6e8e6-69f0-4177-9090-6f8cf0f23b9c)
![image](https://github.com/Prafful33Tak/Network-Generator/assets/88709400/e608b14b-bdac-4019-bd84-11142a3024eb)
[Report_Log.pdf](https://github.com/Prafful33Tak/Network-Generator/files/12047297/Report_Log.pdf)


## File Descriptions

- `netgen.py`: The main script for running iperf3 commands and generating network traffic.
- `throughput_analysis.py`: Script for parsing iperf3 log files, generating throughput graphs, calculating statistical measures, and generating a throughput report.
- `throughput_report_template.html`: HTML template used for generating the final throughput report.
- Please refer the below attached structure of the NETGEN before running it.
- ![Structure_of_NETGEN](https://github.com/Prafful33Tak/Network-Generator/assets/88709400/639338d5-fa77-4ae8-8a43-7b0ad137aac2)



## Customization

- You can modify the iperf3 command and arguments in the `netgen.py` script to suit your specific network testing requirements.
- The `throughput_analysis.py` script can be customized to change the graph generation, statistical calculations, or report format as needed.
- Feel free to modify the `throughput_report_template.html` file to adjust the appearance or content of the generated throughput report.










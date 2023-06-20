import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
import numpy as np


def fetch_throughput_data(log_file):
    # Read the contents of the log file
    with open(log_file, 'r') as logfile:
        data = logfile.read()

    # Split the string into lines
    lines = data.split('\n')

    # Initialize an empty list to store the separated data
    data = []

    # Iterate over each line and split it into columns
    for line in lines:
        columns = line.split()
        # Append the separated columns to the data list
        data.append(columns)

    final_data = []
    num_cols = 0

    for row in data:
        if row[0] == '-': 
            break
        elif (len(row) == 8 or len(row) == 9):
            num_cols = len(row)
            final_data.append(row)

    # Create a DataFrame from the final separated data
    if num_cols == 8:
        df = pd.DataFrame(final_data, columns=['ID_temp', 'ID', 'Interval', 'Int_unit', 'Transfer', 'Trans_unit', 'Bandwidth', 'Band_unit'])
    else:
        df = pd.DataFrame(final_data, columns=['ID_temp', 'ID', 'Interval', 'Int_unit', 'Transfer', 'Trans_unit', 'Bandwidth', 'Band_unit', 'Datagrams'])


    # df = df.drop(['ID_temp', 'ID', 'Int_unit', 'Trans_unit', 'Band_unit'], axis=1) 
    df = df.drop(['ID_temp', 'ID'], axis=1) 

    return df



def generate_graph(df):
    # Interval, Transfer rate & Bandwidth columns
    interval = list(range(1, 1+len(df['Interval'])))

    bandwidth = [float(element) for element in df['Bandwidth']]
    band_unit = [str(element) for element in df['Band_unit']]

    transfer_rate = [float(element) for element in df['Transfer']]
    trans_unit = [str(element) for element in df['Trans_unit']]

    # Converting MBytes to KBytes
    transfer_rate = [rate * 1024 if trans_unit[i] == "MBytes" else rate for i, rate in enumerate(transfer_rate)]

    # Create a scatter plot of the 'Interval' and 'Bandwidth' columns
    plt.figure(figsize=(10, 6))
    plt.scatter(interval, bandwidth, label='Bandwidth in '+ band_unit[0])
    plt.scatter(interval, transfer_rate, label='Transfer rate in '+ band_unit[0])

    # Draw a line joining the points
    plt.plot(interval, bandwidth, color='blue', linewidth=1, linestyle='--')
    plt.plot(interval, transfer_rate, color='red', linewidth=1, linestyle='--')

    plt.xlabel('Interval')
    plt.ylabel('Transfer rate and Bandwidth')
    plt.title('Transfer rate and Bandwidth Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig('transfer_bandwidth_graph.png')



def generate_html_report(df):
    # Load the Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('./report_template.html')

    # Convert the DataFrame to an HTML table
    table_html = df.to_html()

    # Render the template with the throughput data
    html = template.render(data=table_html)

    # Save the HTML report to a file
    with open('report.html', 'w') as file:
        file.write(html)



# Specify the path to the log file
log_file = './log.txt'

# Fetch the throughput data
df = fetch_throughput_data(log_file)

# Generate the graph
generate_graph(df)

# Generate the HTML report
generate_html_report(df)
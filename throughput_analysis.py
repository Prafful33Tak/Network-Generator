# Import the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
import numpy as np
import statistics


# Function to fetch the throughput data from the log file 
def parse_iperf_log(log_file: str) -> pd.DataFrame:
    # Read the contents of the log file
    with open(log_file, 'r') as logfile:
        data = logfile.read()

    # Split the string into lines
    lines = data.split('\n')

    # Initialize an empty list to store the separated data
    separated_data = []

    # Iterate over each line and split it into columns
    for line in lines:
        columns = line.split()
        separated_data.append(columns)

    final_data = []
    num_columns = 0
    flag = False

    for row in separated_data:
        if row[0] == '-':
            continue
        elif row[1] == 'ID]' and not flag:
            flag = True
        elif row[1] == 'ID]' and flag:
            break
        elif len(row) in [8, 9] or row[0] == '[SUM]':
            if row[0] == '[SUM]':
                row.insert(0, ' ')
                num_columns = len(row)
                final_data.append(row)
            else:
                num_columns = len(row)
                row[1] = '[' + row[1]
                final_data.append(row)

    # Create a DataFrame from the final separated data
    column_names = ['ID_temp', 'ID', 'Interval', 'Interval_unit', 'Transfer', 'Transfer_unit', 'Bandwidth', 'Bandwidth_unit']
    if num_columns != 8:
        column_names.append('Datagrams')

    df = pd.DataFrame(final_data, columns=column_names)
    df = df.drop(['ID_temp'], axis=1)

    return df



# Function for unit conversion of transfer and bandwidth
def convert_units(df: pd.DataFrame) -> tuple:
    bandwidth = [float(element) for element in df['Bandwidth']]
    bandwidth_unit = [str(element) for element in df['Bandwidth_unit']]

    transfer = [float(element) for element in df['Transfer']]
    transfer_unit = [str(element) for element in df['Transfer_unit']]

    # Converting  MBytes or GBytes to KBytes (to make sure that Transfer & Bandwidth have same units)
    transfer = [rate * 1024 if transfer_unit[i] == "MBytes" else rate * 1024 * 1024 if transfer_unit[i] == "GBytes" else rate for i, rate in enumerate(transfer)]

    return transfer, bandwidth, bandwidth_unit[0]



# Function to generate the plots of Transfer & Bandwidth
def plot_transfer_bandwidth(df: pd.DataFrame, graph_name: str, group: str, cumulative: bool = False) -> None:
    # Interval, Transfer & Bandwidth columns
    interval = list(range(1, 1 + len(df['Interval'])))

    # Convert transfer and bandwidth units
    transfer, bandwidth, bandwidth_unit = convert_units(df)

    # Generate the cumulative graph of Transfer & Bandwidth
    if cumulative:
        transfer = list(pd.Series(transfer).cumsum())
        bandwidth = list(pd.Series(bandwidth).cumsum())

    plt.figure(figsize=(10, 6))

    # Draw a line joining the points
    plt.plot(interval, bandwidth, label='Bandwidth in ' + bandwidth_unit, color='blue', linewidth=1, linestyle='--')
    plt.plot(interval, transfer, label='Transfer in ' + bandwidth_unit, color='red', linewidth=1, linestyle='--')

    plt.xlabel('Interval')
    plt.ylabel('Transfer and Bandwidth')
    plt.title('Transfer and Bandwidth over Time for ' + group)
    plt.legend()
    plt.grid(True)

    # Save the graph
    plt.savefig(graph_name)



# Function to generate Segregated graphs based on the ID's
def generate_segregated_graphs(df: pd.DataFrame) -> tuple:
    # Segregate the dataframe based on ID
    grouped = df.groupby('ID')

    # Create dictionaries to store the graph names
    graphs = {}
    cumulative_graphs = {}

    # Create a dictionary to store the segregated dataframes
    segregated_dataframes = {group: data for group, data in grouped}

    # Generate graphs and cumulative graphs for each segregated dataframe
    for group, dataframe in segregated_dataframes.items():
        graph_name = f"{group}_transfer_bandwidth_graph"
        cumulative_graph_name = f"{group}_cumulative_transfer_bandwidth_graph"

        # Generate regular graph
        plot_transfer_bandwidth(dataframe, graph_name, group)
        graphs[group] = graph_name

        # Generate cumulative graph
        plot_transfer_bandwidth(dataframe, cumulative_graph_name, group, True)
        cumulative_graphs[group] = cumulative_graph_name

    return graphs, cumulative_graphs



# Function to calculate statistical measures of the throughput data
def calculate_statistics(data: list) -> tuple:
    if not data:
        return None, None, None, None

    # Calculate statistical measures (mean, median, standard deviation, 90th percentile)
    mean = round(statistics.mean(data), 2)
    median = round(statistics.median(data), 2)
    std_dev = round(statistics.stdev(data), 2)
    percentile_90 = round(np.percentile(data, 90), 2)

    return mean, median, std_dev, percentile_90



# Function to generate the throughput report
def generate_throughput_report(df: pd.DataFrame, graphs: list, cumulative_graphs: list, transfer: list, bandwidth: list) -> None:
    # Calculate statistical measures
    mean_transfer, median_transfer, std_dev_transfer, percentile_90_transfer = calculate_statistics(transfer)
    mean_bandwidth, median_bandwidth, std_dev_bandwidth, percentile_90_bandwidth = calculate_statistics(bandwidth)

    # Render the HTML template with the data, graphs, and statistical measures
    env = Environment(loader=FileSystemLoader('.'))     # Set the path to the directory containing templates
    template = env.get_template('throughput_report_template.html')
    rendered_html = template.render(
        data=df.to_html(),
        graphs=graphs,
        cumulative_graphs=cumulative_graphs,
        mean_transfer=mean_transfer,
        mean_bandwidth=mean_bandwidth,
        median_transfer=median_transfer,
        median_bandwidth=median_bandwidth,
        std_dev_transfer=std_dev_transfer,
        std_dev_bandwidth=std_dev_bandwidth,
        percentile_90_transfer=percentile_90_transfer,
        percentile_90_bandwidth=percentile_90_bandwidth
    )

    # Save the rendered HTML to a file
    with open('throughput_report.html', 'w') as file:
        file.write(rendered_html)



# Specify the path to the log file
log_file = './log_P.txt'

# Fetch the throughput data
df = parse_iperf_log(log_file)

# Generate Segregated graphs based on the ID's
graphs, cumulative_graphs = generate_segregated_graphs(df)

# Generate the throughput report
transfer, bandwidth, bandwidth_unit = convert_units(df)
generate_throughput_report(df, graphs, cumulative_graphs, transfer, bandwidth)

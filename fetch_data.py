import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
import numpy as np
import statistics




# function to fetch the throughput data from the log file 
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
    flag = False


    for row in data:
        if row[0] == '-': 
            continue
        elif row[1] == 'ID]' and flag == False:
            flag = True 
        elif row[1] == 'ID]' and flag:
            break
        elif (len(row) == 8 or len(row) == 9 or row[0] == '[SUM]'):
            if row[0] == '[SUM]':
                row.insert(0, ' ')
                num_cols = len(row)
                final_data.append(row)
            else:
                num_cols = len(row)
                row[1] = '[' + row[1] 
                final_data.append(row)


    # Create a DataFrame from the final separated data
    if num_cols == 8:
        df = pd.DataFrame(final_data, columns=['ID_temp', 'ID', 'Interval', 'Int_unit', 'Transfer', 'Trans_unit', 'Bandwidth', 'Band_unit'])
    else:
        df = pd.DataFrame(final_data, columns=['ID_temp', 'ID', 'Interval', 'Int_unit', 'Transfer', 'Trans_unit', 'Bandwidth', 'Band_unit', 'Datagrams'])


    # df = df.drop(['ID_temp', 'ID', 'Int_unit', 'Trans_unit', 'Band_unit'], axis=1) 
    df = df.drop(['ID_temp'], axis=1) 

    return df



# function to generate the graph of Transfer rate & Bandwidth
def generate_graph(df, graph_name, group):
    # Interval, Transfer rate & Bandwidth columns
    interval = list(range(1, 1+len(df['Interval'])))

    bandwidth = [float(element) for element in df['Bandwidth']]
    band_unit = [str(element) for element in df['Band_unit']]

    transfer_rate = [float(element) for element in df['Transfer']]
    trans_unit = [str(element) for element in df['Trans_unit']]

    # Converting MBytes to KBytes
    transfer_rate = [rate * 1024 if trans_unit[i] == "MBytes" else rate for i, rate in enumerate(transfer_rate)]

    plt.figure(figsize=(10, 6))

    # Draw a line joining the points
    plt.plot(interval, bandwidth, label='Bandwidth in '+ band_unit[0], color='blue', linewidth=1, linestyle='--')
    plt.plot(interval, transfer_rate, label='Transfer rate in '+ band_unit[0], color='red', linewidth=1, linestyle='--')

    plt.xlabel('Interval')
    plt.ylabel('Transfer rate and Bandwidth')
    plt.title('Transfer rate and Bandwidth over Time for ' + group)
    plt.legend()
    plt.grid(True)
    plt.savefig(graph_name)



# function to generate the cummulative graph of Transfer rate & Bandwidth
def generate_cummulative_graph(df, cummulative_graph_name, group):
    # Interval, Transfer rate & Bandwidth columns
    interval = list(range(1, 1+len(df['Interval'])))

    bandwidth = [float(element) for element in df['Bandwidth']]
    band_unit = [str(element) for element in df['Band_unit']]

    transfer_rate = [float(element) for element in df['Transfer']]
    trans_unit = [str(element) for element in df['Trans_unit']]

    # Converting MBytes to KBytes
    transfer_rate = [rate * 1024 if trans_unit[i] == "MBytes" else rate for i, rate in enumerate(transfer_rate)]

    # modifying transfer_rate & bandwidth s.t they contains the cummulative sum of transfer_rate & bandwidth
    currTotalTransfer = 0
    currTotalBandwidth = 0

    for i in range(len(df['Interval'])):
        currTotalTransfer += transfer_rate[i]
        transfer_rate[i] = currTotalTransfer

        currTotalBandwidth += bandwidth[i]
        bandwidth[i] = currTotalBandwidth

    plt.figure(figsize=(10, 6))

    # Draw a line joining the points
    plt.plot(interval, bandwidth, label='Bandwidth in '+ band_unit[0], color='blue', linewidth=1, linestyle='--')
    plt.plot(interval, transfer_rate, label='Transfer rate in '+ band_unit[0], color='red', linewidth=1, linestyle='--')

    plt.xlabel('Interval')
    plt.ylabel('Transfer rate and Bandwidth')
    plt.title('Cummulative Transfer rate and Bandwidth over Time for ' + group)
    plt.legend()
    plt.grid(True)
    plt.savefig(cummulative_graph_name)



# function to generate the html report
def generate_html_report(df, graphs, cummulative_graphs, transfer_rate, bandwidth):
    # Calculate statistical measures
    mean_transfer_rate, median_transfer_rate, std_dev_transfer_rate, percentile_90_transfer_rate = calculate_statistics(transfer_rate)
    mean_bandwidth, median_bandwidth, std_dev_bandwidth, percentile_90_bandwidth = calculate_statistics(bandwidth)

    # Render the HTML template with the data, graphs, and statistical measures
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')
    rendered_html = template.render(
        data=df.to_html(),
        graphs=graphs,
        cummulative_graphs=cummulative_graphs,
        mean_transfer_rate=mean_transfer_rate,
        mean_bandwidth=mean_bandwidth,
        median_transfer_rate=median_transfer_rate,
        median_bandwidth=median_bandwidth,
        std_dev_transfer_rate=std_dev_transfer_rate,
        std_dev_bandwidth=std_dev_bandwidth,
        percentile_90_transfer_rate=percentile_90_transfer_rate,
        percentile_90_bandwidth=percentile_90_bandwidth
    )

    # Save the rendered HTML to a file
    with open('throughput_report.html', 'w') as file:
        file.write(rendered_html)




def segregate_dataframes(df):
    # Segregate the dataframe based on ID
    grouped = df.groupby('ID')

    # Create dictionaries to store the graph names
    graphs = {}
    cummulative_graphs = {}

    # Create a dictionary to store the segregated dataframes
    segregated_dataframes = {}

    # Iterate over the groups and store the segregated dataframes
    for group, data in grouped:
        segregated_dataframes[group] = data

 
    # Iterate over the groups and generate graphs
    for group, dataframe in segregated_dataframes.items():
        graph_name = group + "_transfer_bandwidth_graph"
        cummulative_graph_name = group + "_cummulative_transfer_bandwidth_graph"

        generate_graph(dataframe, graph_name, group)
        generate_cummulative_graph(dataframe, cummulative_graph_name, group)

        graphs[group] = graph_name
        cummulative_graphs[group] = cummulative_graph_name

    return graphs, cummulative_graphs



# function to Calculate statistical measures of the throughput data
def calculate_statistics(data):
    # Calculate statistical measures (mean, median, standard deviation, 90th percentile)
    mean = round(statistics.mean(data), 2)
    median = round(statistics.median(data), 2)
    std_dev = round(statistics.stdev(data), 2)
    percentile_90 = round(np.percentile(data, 90), 2)

    return mean, median, std_dev, percentile_90



# function for unit conversion of transfer rate and bandwidth
def convert_units(df):
    bandwidth = [float(element) for element in df['Bandwidth']]
    band_unit = [str(element) for element in df['Band_unit']]

    transfer_rate = [float(element) for element in df['Transfer']]
    trans_unit = [str(element) for element in df['Trans_unit']]

    # Converting MBytes to KBytes
    transfer_rate = [rate * 1024 if trans_unit[i] == "MBytes" else rate for i, rate in enumerate(transfer_rate)]

    return transfer_rate, bandwidth



# Specify the path to the log file
log_file = './log.txt'

# Fetch the throughput data
df = fetch_throughput_data(log_file)

# unit conversion
transfer_rate, bandwidth = convert_units(df)

# Segregate the dataframes based on ID's and generate report
graphs, cummulative_graphs = segregate_dataframes(df)

# generate html report
generate_html_report(df, graphs, cummulative_graphs, transfer_rate, bandwidth)




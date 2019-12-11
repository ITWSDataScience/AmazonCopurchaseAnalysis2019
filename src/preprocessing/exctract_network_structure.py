# -*- coding: utf-8 -*-
# Author: Gregorios Katsios

# get the filenames from global vars
input_file_path = '../../amazon-meta/amazon-meta.txt'
network_output_file_path = '../../output/preprocessing/product_network.csv'
information_output_file_path = '../../output/preprocessing/product_category.csv'

# use global key dictionary to parse specific information
keys = {'1': 'Id: ',
        '2': 'ASIN: ',
        '3': 'group: ',
        '4': 'reviews: ',
        '5': 'similar: ',
        '6': 'categories: '}

# In[4]: saves product category information into CSV file
def groundTruth2CSV(ground_truth, filename):
    print("5. Saving product category info into file: \n\t", filename, "\n")
    
    # open a file to write network information
    with open(filename, 'w') as csv:
        
        # write title-line
        csv.write('product.index,product.category\n')
        
        # write data
        for tupl in ground_truth:
            csv.write(str(tupl[0]) + ',' + str(tupl[1]) + '\n')

# In[3]: saves network adjacency matrix into CSV file
def network2CSV(network, filename):
    print("4. Saving network into file: \n\t", filename, "\n")
    
    # open a file to write network information
    with open(filename, 'w') as csv:
        
        # write title-line
        csv.write('product.index,product.neighbor.index\n')
        
        # write data
        for edge in network:
            # convert ids to string for writing
            csv.write(str(edge[0]) + ',' + str(edge[1]) + '\n')

# In[2]: re-index network
def reIndexNetwork(network, dataset):
    print("3. Re-indexing network...")
    
    ids = set()    
    reindexed = []
    ground_truth = []
    networkx = dict()
    
    # get all nodes
    for edge in network:
        ids.add(edge[0])
        ids.add(edge[1])
      
    # to subscriptable datastruct
    ids = list(ids)
    
    # create index
    for index in range(len(ids)):
        networkx[ids[index]] = index
        
    # re-index network
    for edge in network:
        reindexed.append((networkx[edge[0]], networkx[edge[1]]))   
        
    # re-index ground truth
    for pid, product in dataset.items():   
        pid = int(pid)
        if pid in networkx:
            ground_truth.append((networkx[pid], product['category']))
    
    # final network info
    print("\t$", len(ids), " nodes in the network.")
    print("\t$", len(reindexed), " edges in the network.\n")
        
    return reindexed, ground_truth
    
# In[2]: process dataset into adjacency matrix
def exctractNetwork(dataset):
    print("2. Extracting network...")
    
    counter = 0
    network = []
    products = dict()
    
    # get all valid asins into a set
    for ids, product in dataset.items():
        products[product['asin']] = ids
    
    # create adjacency matrix
    for ids, product in dataset.items():        
        for neighbor in product['neighbors']:
            if neighbor in products:
                # convert ids to integer for sorting
                network.append((int(ids), int(products[neighbor])))
            else:
                counter += 1
    
    # sort the tuples
    network.sort(key = lambda x: x[0])
    print("\t%", counter, " edges not found, as the dataset does not contain all given neighboring nodes.\n")
    
    return network

# In[1]: loads Amazon Meta dataset into memory 
def loadAmazonMeta(filename):
    print("1. Loading dataset from file: \n\t", filename)
    
    counter = 0
    counter_2 = 0
    data = dict()
    current_id = -1
    
    # open dataset file to read
    with open(filename, 'r') as dataset:
    	for line in dataset:
            
            # this is a comment line
            if line.startswith('#'):
                continue
            
            # if line is blank, then new product will in next line
            elif len(line) == 0:
                current_id = -1
                
            else:
                
                # when line starts with id, then its a new product
                if line.startswith(keys['1']):
                    current_id = line.strip().split()[1]
                    data[current_id] = dict()
                    
                # this line has ASIN
                elif line.startswith(keys['2']):
                    data[current_id]['asin'] = line.strip().split()[1]
                    
                # this line has group
                elif keys['3'] in line:
                    data[current_id]['category'] = line.strip().split()[1]
                    
                # this line has adjacency list
                elif keys['5'] in line:
                    data[current_id]['neighbors'] = line.strip().split()[2:]
            
    # process discontinued products    
    for ids, product in data.items():
        if 'neighbors' in product and 'category' in product:
            continue
        else:
            data[ids]['neighbors'] = []
            data[ids]['category'] = 'discontinued product'
            counter += 1
    
    # remove items that are not in one of the 4 valid categories
    clean_data = dict()
    for ids, product in data.items():
        if product['category'] in ['Book', 'Music', 'Video', 'DVD']:
            clean_data[ids] = product
        else:
            counter_2 += 1
            continue
            
    # discontinued product information - it will be removed by the network extraction if necessary
    print("\t*", counter, " products had null descriptors for \'neighbors\' or \'category\' keys.")
    print("\t*", counter_2, " products were not in one of the 4 valid categories.\n")
    
    return clean_data

# In[0]: main function
def main():
    
    # load dataset and extract network
    dataset = loadAmazonMeta(input_file_path)
    network = exctractNetwork(dataset)
    
    # re-index the nodes of the network to be consecutive integers
    network, ground_truth = reIndexNetwork(network, dataset)
    
    # save two new datasets
    network2CSV(network, network_output_file_path)
    groundTruth2CSV(ground_truth, information_output_file_path)
    
if __name__ == "__main__":
    main()
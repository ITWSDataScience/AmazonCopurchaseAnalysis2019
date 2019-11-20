# -*- coding: utf-8 -*-
# Author: Gregorios Katsios

# get the filenames from global vars
input_file_path = '../amazon-meta/amazon-meta.txt'
network_output_file_path = '../output/product_network.csv'
information_output_file_path = '../output/product_category.csv'

# use global key dictionary to parse specific information
keys = {'1': 'Id',
        '2': 'ASIN',
        '3': 'group',
        '4': 'reviews',
        '5': 'similar',
        '6': 'categories'}

# In[4]: saves product category information into CSV file
def product2Category(dataset, filename):
    print("4. Saving product category info into file: \n\t", filename)
    
    # open a file to write network information
    with open(filename, 'w') as csv:
        
        # write title-line
        csv.write('product.id,product.category\n')
        
        # write data
        for ids, product in dataset.items():
            csv.write(ids + ',' + product['category'] + '\n')

# In[3]: saves network adjacency matrix into CSV file
def network2CSV(network, filename):
    print("3. Saving network into file: \n\t", filename)
    
    # open a file to write network information
    with open(filename, 'w') as csv:
        
        # write title-line
        csv.write('product.id,product.neighbor.id\n')
        
        # write data
        for edge in network:
            # convert ids to string for writing
            csv.write(str(edge[0]) + ',' + str(edge[1]) + '\n')
            
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
    print("\t$", len(products), " nodes in the network.")
    print("\t$", len(network), " edges in the network.")
    print("\t$", counter, " edges not found, as the network does not contain all given neighboring nodes.")
    
    return network

# In[1]: loads Amazon Meta dataset into memory 
def loadAmazonMeta(filename):
    print("1. Loading dataset from file: \n\t", filename)
    
    counter = 0
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
            
    print("\t*", counter, " products had null descriptors for \'neighbors\' or \'category\' keys (discontinued products).")
    
    return data

# In[0]: main function
def main():
    
    # load dataset and extract network
    dataset = loadAmazonMeta(input_file_path)
    network = exctractNetwork(dataset)
    
    # save two new datasets
    network2CSV(network, network_output_file_path)
    product2Category(dataset, information_output_file_path)
    
if __name__ == "__main__":
    main()
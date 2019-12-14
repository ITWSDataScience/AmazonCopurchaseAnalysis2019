# -*- coding: utf-8 -*-
# Author(s): Gregorios Katsios & <>

import json
from sklearn import metrics

# In[]: load embeddings from file into memory
def loadEmbeddings(filename):
    print("X. Loading embeddings from file: \n\t", filename)
    
    # embedding dict (index -> vector)
    embeddings = dict()
    with open(filename, 'r') as gemsec:
       lines = gemsec.readlines()
       for i in range(len(lines)):
            
            # skip title line
            if i == 0:
                continue
            else:
                # a single vector
                embeddings[i - 1] = [float(i) for i in lines[i].split(',')] 
                
    return embeddings

#    embeddings =          
#        {0: [1.3017, 0.132],
#         1: [-0.94, 1.4989],
#         2: [....],
#         3: [...],
#         ....
#         }
    
# In[]: load categoriess from file into memory
def loadCategories(filename):
    print("2. Loading category ground-truth from file: \n\t", filename)
    
    # embedding dict (index -> vector)
    categories = dict()
    with open(filename, 'r') as ground_truth:
        lines = ground_truth.readlines()
        
        for i in range(len(lines)):
            line = lines[i]
               
            # skip title line
            if i == 0:
                continue
            else:
                data = line.split(',')
                categories[int(data[0])] = data[1].strip()
                
    print("\t", len(categories), " categories were loaded.")
                
    return categories

#    categories = 
#        {0: "Book",
#         1: "Book",
#         2: "CD",
#         3: "DVD", 
#         ...}

# In[]: load clustering results from file into memory
def loadClusters(filename):
    print("1. Loading clustering results from file: \n\t", filename)
                
    clusters = dict()
    with open(filename, 'r') as results:
        
        # load entire json as dict
        data = json.load(results)
    
    # re-format keys and values to be integers
    for key, value in data.items():
        clusters[int(key)] = int(value)
        
    print("\t", len(clusters), " labels were loaded.")
        
    return clusters
                
#    clusters = 
#        {0: 0, 
#         1: 0,
#         2: 3,
#         3: 1,
#         ...}

# In[]: evaluate clustering results
def evaluate_clustering(clusters, categories):
    print("3. Evaluating clustering results...")
    labels = []
    categs = []
    counter = 0
    
    # example for loop to assign categories and vectors
    for index, label in clusters.items():
        labels.append(label)
        
        # swap category string with a number
        category = categories[index]
        if category == 'Book':
            category = 0
        elif category == 'Music':
            category = 1
        elif category == 'Video':
            category = 2
        elif category == 'DVD':
            category = 3
        else:
            counter += 1
            continue
        
        # append to the list
        categs.append(category)
        
    print("\t*", counter, " products were not in one of the 4 valid categories.\n")
    
    # compute clustering quality metrics
    ari = metrics.adjusted_rand_score(categs, labels)
    ami = metrics.adjusted_mutual_info_score(categs, labels)
    homogeneity = metrics.homogeneity_score(categs, labels)
    completeness = metrics.completeness_score(categs, labels)
    v = metrics.v_measure_score(categs, labels)
    
    # print the results
    print("\tThe results are:")
    print("\tAdjusted Rand Index: ", round(ari, 3))
    print("\tAdjusted Mutual Information: ", round(ami, 3))
    print("\tHomogeneity: ", round(homogeneity, 3))
    print("\tCompleteness: ", round(completeness, 3))
    print("\tV-Measure: ", round(v, 3))
    
# In[]: the main function
def main():
    clusters = loadClusters('../../output/deep_walk/clusters/product_cluster_assignments.json')
    categories = loadCategories('../../output/preprocessing/product_category.csv')
    evaluate_clustering(clusters, categories)
    
if __name__ == '__main__':
    main()
    
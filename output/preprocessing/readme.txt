
Description for file product_category.csv (created on November 13, 2019)
	This comma separated formatted file has two columns titled "product.index" and "product.category"
		The "product.index" column contains the index number of the product, which is an incrementing integer value.
 		The "product.category" column contains the category of the product, which can take one of the following values:
	 			"discontinued product": for products that were removed from the amazon market,
	 			"Book": for products that are books,
	 			"Music": for products that are music CDs,
	 			"DVD": for products that are DVDs, and
	 			"Video": for products that are VHS tapes.

Description for file product_network.csv (created on November 13, 2019)
	This comma separated formatted file has two columns titled "product.id" and "product.neighbor.id"
		The "product.index" column contains the index number of the product, which is an incrementing integer value.
 		The "product.neighbor.index" column contains the index number of the product that has a neighborOf relationship with the product identified in the first collumn. This is also an integer value.
 			product.neighbor.index = neighborOf(product.index)

Both files described above are products of the exctract_network_structure.py script. Input to this script is the amazon-meta.txt file, which was downloaded from https://snap.stanford.edu/data/bigdata/amazon/amazon-meta.txt.gz on November 13, 2019.

TODO: turn this description into a proper metadata format.
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 18:53:40 2023

@author: Özkan
"""




import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Veri seti
file_path = 'data_10k.csv'
data = pd.read_excel(file_path)
original_data= data.copy()


# User-item interaction matrix
item_interaction_matrix = pd.pivot_table(data, index='MALZEME_ADI', columns='CARIKART_ID', values='MIKTAR', fill_value=0)



# Scaling - MinMax
scaler = MinMaxScaler()
item_interaction_matrix_scaled = pd.DataFrame(scaler.fit_transform(item_interaction_matrix), index=item_interaction_matrix.index, columns=item_interaction_matrix.columns)


# Cosine Similarity calculation
item_similarity = pd.DataFrame(cosine_similarity(item_interaction_matrix_scaled), index=item_interaction_matrix.index, columns=item_interaction_matrix.index)



# Recommendation function
def recommend_similar_products(product_id, item_similarity, top_n=5):
  
    # Most similar product to the current product
    similar_products = item_similarity[product_id].sort_values(ascending=False).index.tolist()
    similar_products.remove(product_id)  # Remove the product itself
    return similar_products[:top_n]


# Take an input
example_product_id = input("Please enter a product name: ")







  #Calculates the similarity ratio between two products.
def calculate_similarity(product1, product2, item_similarity):

    return item_similarity.loc[product1, product2]








#Calculates the similarity rates between the input product and the recommended products.

def calculate_similarity_ratios(input_product, recommended_similar_products, item_similarity):
    
    similarity_ratios = {}
    
    for recommended_product in recommended_similar_products:
        similarity_score = calculate_similarity(input_product, recommended_product, item_similarity)
        similarity_ratios[recommended_product] = similarity_score
    
    return similarity_ratios
input_product = example_product_id
recommended_products = recommend_similar_products(input_product, item_similarity)
similarity_ratios = calculate_similarity_ratios(input_product, recommended_products, item_similarity)

# Yazdırma
print(f"Recommended Products and Similarity Rates with {input_product}:")
for recommended_product, similarity_ratio in similarity_ratios.items():
    print(f"{recommended_product}: {similarity_ratio}")







import matplotlib.pyplot as plt

# Visualizes similarity ratios on a bar chart.
def plot_similarity_ratios(similarity_ratios):
   
    products = list(similarity_ratios.keys())
    scores = list(similarity_ratios.values())

    plt.barh(products, scores, color='skyblue')
    plt.xlabel('Similarity ratios')
    plt.title( 'Recommended Products and Similarity Rates with' + example_product_id )
    plt.show()

plot_similarity_ratios(similarity_ratios)
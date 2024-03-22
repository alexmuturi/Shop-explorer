import streamlit as st
import pandas as pd
from itertools import permutations
import json



# Load data
# shop_list = pd.read_csv("List of Shops.csv")
# shop_list.head()

products_df = pd.DataFrame()
for i in range (1,6):    
    df = pd.read_csv(f"Shop {i}.csv")
    df['Shop Name'] = f"Shop {i}"
    products_df = pd.concat([products_df, df])

#convert to Json
json_things = (products_df.groupby('Shop Name').apply(lambda x: x.to_json(orient='values')))


def search_products (json_things, products):
    
    for i, shop in enumerate(json_things):
        results = []
        json_object = json.loads(shop)
        # print(f"{len(json_object)} Items found in Shop {i}. Matches with query:")
        for item in json_object:
            
            for thing in item:               
                if thing in products:                            
                    #    print (thing, "\n") 
                       results.append(thing)
        difference = len(list(set(products)-(set(results))))
        if difference < 1:
             
             st.success(f"Found match for all products in Shop {i+1}")
        else:
            st.warning(f"Not all products found in Shop {i+1}")


# Streamlit UI
st.title("Coffee Shop Product Search")

# Input for products
product_input = st.text_area("Enter the products separated by commas (e.g., Iced coffee, soy milk, agave nectar, honeycomb, protein powder):")

if st.button("Search"):
    products_input = [product.strip() for product in product_input.split(",")]
   
    search_products(json_things, products_input)
    
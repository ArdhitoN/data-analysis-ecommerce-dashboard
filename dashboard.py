import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Fungsi untuk mengambil data
def load_data():
    seller_sales_by_city = pd.read_csv('seller_sales_by_city.csv')  
    reviews_per_category = pd.read_csv('reviews_per_category.csv')
    return seller_sales_by_city, reviews_per_category

# Fungsi untuk memvisualisasikan sales berdasarkan kota yang dipilih
def plot_seller_sales_by_city(data, selected_cities):
    # Filter data berdasarkan kota terpilih
    filtered_data = data[data['seller_city'].isin(selected_cities)]
    
    # Sort dan mengambil top 10 
    filtered_data = filtered_data.sort_values(by='total_sales_city', ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=filtered_data, x='total_sales_city', y='seller_city', palette='viridis')
    plt.xlabel('Total Sales')
    plt.ylabel('Seller City')
    plt.title('Sales by Seller City')
    st.pyplot(plt)

def plot_reviews_per_category(data, selected_categories):
    # Filter data berdasarkan kategori terpilih
    filtered_data = data[data['product_category_name'].isin(selected_categories)]
    
    # Sort dan mengambil top 10 
    filtered_data = filtered_data.sort_values(by='average_review_score_category', ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=filtered_data, x='average_review_score_category', y='product_category_name', palette='magma')
    plt.xlabel('Average Review Score')
    plt.ylabel('Category')
    plt.title('Reviews per Product Category')
    st.pyplot(plt)

def main():
    st.title('Brazillian E-commerce Dashboard')
    
    seller_sales_by_city, reviews_per_category = load_data()
    
    st.sidebar.header('Options')
    analysis_type = st.sidebar.selectbox('Analysis type:', ['Sales by Sellers City', 'Reviews per Product Category'])

    # Untuk analisis kota sellers berdasarkan performa sales
    if analysis_type == 'Sales by Sellers City':
        city_list = seller_sales_by_city['seller_city'].unique().tolist()
        city_filter = st.sidebar.multiselect('Filter by City:', city_list, default=city_list[:10])  # Default to top 10 cities by list order
        plot_seller_sales_by_city(seller_sales_by_city, city_filter)
        
        if st.checkbox('Show data table'):
            st.dataframe(seller_sales_by_city[seller_sales_by_city['seller_city'].isin(city_filter)]
                         .sort_values(by='total_sales_city', ascending=False))

    # Untuk analisis review berdasarkan kategori product
    elif analysis_type == 'Reviews per Product Category':
        category_list = reviews_per_category['product_category_name'].unique().tolist()
        category_filter = st.sidebar.multiselect('Filter by Category:', category_list, default=category_list[:10])  # Default to top 10 categories by list order
        plot_reviews_per_category(reviews_per_category, category_filter)
        
        if st.checkbox('Show data table'):
            st.dataframe(reviews_per_category[reviews_per_category['product_category_name'].isin(category_filter)]
                         .sort_values(by='average_review_score_category', ascending=False))

if __name__ == "__main__":
    main()
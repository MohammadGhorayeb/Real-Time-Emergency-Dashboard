from eventregistry import *
import pandas as pd
import time

# Initialize Event Registry with your API key
er = EventRegistry(apiKey="bd905fb5-dfd2-459d-b1e7-199aa2e10855")  # Replace with your actual API key

# List of broad keywords related to Lebanon
broad_keywords = [
    "Lebanon", "Beirut", "Saida", "Tripoli", "South of Lebanon", "North of Lebanon", "Mount of Lebanon", "Bekaa"
   "Resistance Lebanon", "Baalbek", "Nabatieh", "Akkar"
]

# Initialize an empty list to store article data
articles_data = []
keyword_article_count = {} 

# Check if the Excel file already exists
file_path = 'lebanon_news_articles.xlsx'
if os.path.exists(file_path):
    df_existing = pd.read_excel(file_path)
else:
    df_existing = pd.DataFrame()

# Loop through each broad keyword and fetch news articles
for keyword in broad_keywords:
    article_count=0
    try:
        # Create a query for articles with the keyword
        query = QueryArticlesIter(keywords=keyword, lang="eng")  # Use "eng" for English articles
        articles = query.execQuery(er, sortBy="date", maxItems=500)  # Limit to 500 articles per keyword

        # Iterate over articles and add them to articles_data
        for article in articles:
            title = article.get("title", "No Title")
            source = article.get("source", {}).get("title", "Unknown Source")
            link = article.get("url", "No URL")
            snippet = article.get("body", "No Snippet")

            # Append to the articles_data list
            articles_data.append({
                "Keyword": keyword,
                "Title": title,
                "Source": source,
                "Link": link,
                "Snippet": snippet
            })
            article_count+=1

        # Delay between keyword requests to avoid throttling
        time.sleep(1)

    except Exception as e:
        print(f"Error fetching data for keyword '{keyword}': {e}")
        time.sleep(60)  # Wait if there’s an issue, then continue

# Convert the new articles data to a DataFrame
df_new = pd.DataFrame(articles_data)

# Combine the new data with the existing data
df_combined = pd.concat([df_existing, df_new], ignore_index=True)

# Remove duplicates based on 'Title' and 'Link' columns
df_combined.drop_duplicates(subset=['Title', 'Link'], inplace=True)

# Save the combined DataFrame to an Excel file
df_combined.to_excel(file_path, index=False)

print(f"New data added to '{file_path}'. Total unique articles now: {len(df_combined)}")

# Display the count of articles added for each keyword
print("\nNumber of articles added for each keyword:")
for keyword, count in keyword_article_count.items():
    print(f"{keyword}: {count} articles")
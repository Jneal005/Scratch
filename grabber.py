import requests
import time
import pandas as pd

# Create an empty DataFrame to store the Bible data setting the variable in python to the columns in the panda data frame.
columns = ['book', 'chapter', 'verse_number', 'verse_text']
bible_df = pd.DataFrame(columns=columns)

# Function to fetch a specific chapter of a book from the Bible API and store it in a DataFrame
def fetch_and_store_chapter(book, chapter):
    url = f"https://bible-api.com/{book}%20{chapter}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        verse_text = data['text']

        # Split the verse text by individual verses (assuming verses are separated by line breaks)
        verses = verse_text.split("\n")
        
        # Create a temporary DataFrame for the verses in the current chapter
        temp_df = pd.DataFrame({
            'book': [book] * len(verses),
            'chapter': [chapter] * len(verses),
            'verse_number': range(1, len(verses) + 1),
            'verse_text': [verse.strip() for verse in verses]
        })

        # Append the temporary DataFrame to the main DataFrame
        global bible_df
        bible_df = pd.concat([bible_df, temp_df], ignore_index=True)

        print(f"{book} {chapter} inserted successfully.")
    elif response.status_code == 429:
        # If we hit rate limit, wait and retry
        retry_after = int(response.headers.get('Retry-After', 60))  # Default to 60 seconds if no header is present
        print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
        time.sleep(retry_after)
        return fetch_and_store_chapter(book, chapter)  # Retry the request after waiting
    else:
        print(f"Failed to fetch {book} {chapter}. Status Code: {response.status_code}")


# Prompt the user for the book name
book_name = input("Enter the book name (e.g., Genesis, Exodus, Matthew, etc.): ")

# Prompt the user for the number of chapters in the boJObok
number_of_chapters = int(input(f"Enter the number of chapters in {book_name}: "))

# Fetch and store all chapters of the selected book
for chapter in range(1, number_of_chapters + 1):
    fetch_and_store_chapter(book_name, chapter)

# Optionally, save the DataFrame to a CSV file (write headers)

#change mode = w if you want to overwrite the file and change mode = a to append
bible_df.to_csv('bible_data02.csv', mode='a', index=False)  # This writes the file with headers

print(f"{book_name} data saved to bible_data02.csv.")

# Display the first few rows of the DataFrame
print(bible_df.head())
 

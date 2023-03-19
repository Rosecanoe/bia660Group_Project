import requests
import csv
from bs4 import BeautifulSoup
import time

# URL of the movie's reviews page on IMDB sorted by review date
url = 'https://www.imdb.com/title/tt6723592/reviews?sort=submissionDate&dir=desc&ratingFilter=0'

# Send a request to the page and get its content
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the movie title
movie_title = soup.find('h1').text.strip()

# # Find the "Load More" button
# load_more = soup.find('button', class_='ipl-load-more__button')

# # Loop until all reviews are displayed
# while load_more is not None:
#     # Get the AJAX endpoint URL from the "Load More" button
#     endpoint = load_more.get('data-load-more-href')
#     if not endpoint:
#         break

#     # Send an AJAX request to get more reviews
#     response = requests.get(f'https://www.imdb.com{endpoint}')
#     data = response.json()

#     # Append the new reviews to the HTML content
#     html_content += data['load_more_html'].encode()

#     # Wait a few seconds before making the next request
#     time.sleep(2)

#     # Update the BeautifulSoup object with the new HTML content
#     soup = BeautifulSoup(html_content, 'html.parser')

#     # Find the new "Load More" button
#     load_more = soup.find('div', class_='load-more-data')

# Find all the reviews on the page
reviews = soup.find_all('div', class_='imdb-user-review')

# Open a CSV file to write the results
with open(f'{movie_title}_reviews.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row of the CSV file
    writer.writerow(['Title', 'User', 'Stars', 'Date', 'Content'])

    # Loop through each review and write its data to the CSV file
    for review in reviews:
        title = review.find('a', class_='title').text
        user = review.find('span', class_='display-name-link').text
        stars = review.find('span', class_='rating-other-user-rating').find(
            'span').text if review.find('span', class_='rating-other-user-rating') else 'N/A'
        date = review.find('span', class_='review-date').text
        content = review.find(
            'div', class_='text show-more__control').text.strip()
        writer.writerow([title, user, stars, date, content])

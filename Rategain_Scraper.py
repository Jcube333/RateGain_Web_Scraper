# Required Modules bs4,requests,csv
import requests
from bs4 import BeautifulSoup
import csv

import requests
from bs4 import BeautifulSoup
import csv

output_csv = "blog_data.csv"

def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
    }

    with requests.Session() as session:
        session.headers.update(headers)
        response = session.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def extract_data_from_page(post):
    # Extracting data from the page
    link = post.select_one('.content h6 a')['href']
    title = post.select_one('.content h6 a').text.strip()

    # Extracting blog detail information
    date = post.select_one('.content .blog-detail .bd-item span').text.strip()


    # Extracting blog image URL from the style attribute
        
    a_tag = post.select_one('.img a')
    

    if a_tag:
            # Extract the value of the "data-bg" attribute
        image_url = a_tag['data-bg']
    else:
        image_url="Image link not found."

    # Extracting likes count
    likes_count = int(post.select_one('.zilla-likes span').text.strip().split()[0])

    return (title, link, date, image_url, likes_count)

def save_to_csv(data):
    with open(output_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Blog Title", "Blog Link", "Blog Date", "Blog Image URL", "Blog Likes Count"])
        writer.writerows(data)

def main():
    all_data = []

    # Assuming only one page for simplicity
    
    for i in range(1,46):
    
    
        url = f"https://rategain.com/blog/page/{i}/"
        page_content = get_page_content(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        if page_content:
            blog_posts = soup.select('.wrap')  # Assuming '.content' contains each blog post
            for post in blog_posts:
                data = extract_data_from_page(post)
                all_data.append(data)

            save_to_csv(all_data)
            print(f'Page {i} Scraped')
        
    print("Scraping Completed for https://rategain.com/blog")

if __name__ == "__main__":
    main()

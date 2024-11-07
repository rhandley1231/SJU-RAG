import requests
from bs4 import BeautifulSoup
import urllib.parse

def crawl_and_save_urls(base_url, output_file, exclude_url):
    visited_urls = set()
    urls_to_visit = [base_url]
    
    # Open the file in append mode
    with open(output_file, 'a') as file:
        while urls_to_visit:
            url = urls_to_visit.pop(0)
            
            if url in visited_urls or exclude_url in url:
                continue
            
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses
                soup = BeautifulSoup(response.text, 'html.parser')
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")
                continue
            except Exception as e:
                print(f"Error parsing {url}: {e}")
                continue
            
            visited_urls.add(url)
            
            # Append the found URL to the file
            try:
                file.write(url + '\n')
                print(f"Added {url}")
            except Exception as e:
                print(f"Error writing {url} to file: {e}")
                continue
            
            # Find all anchor tags and extract their href attributes
            for link in soup.find_all('a', href=True):
                try:
                    href = link['href']
                    full_url = urllib.parse.urljoin(base_url, href)  # Construct full URL
                    if full_url.startswith(base_url) and full_url not in visited_urls and exclude_url not in full_url:
                        urls_to_visit.append(full_url)
                except Exception as e:
                    print(f"Error processing link {link}: {e}")
                    continue

if __name__ == "__main__":
    base_url = "https://www.stjohns.edu/"
    output_file = "urls.txt"
    exclude_url = "https://www.givecampus.com/"
    crawl_and_save_urls(base_url, output_file, exclude_url)
    print(f"Crawling completed. URLs saved to {output_file}")

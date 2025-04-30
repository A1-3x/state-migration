import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin
import pandas as pd

def download_migration_flows():
    # Create directory for downloads if it doesn't exist
    output_dir = "migration_flows"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Census.gov URL
    url = "https://www.census.gov/data/tables/time-series/demo/geographic-mobility/state-to-state-migration.html"

    # Get the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access the webpage. Status code: {response.status_code}")
        return

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links that match our pattern
    pattern = r"State-to-State Migration Flows: 20(0[5-9]|1[0-9]|2[0-3])"
    
    # Keep track of downloaded files
    downloaded = 0

    # Find all links
    for link in soup.find_all('a'):
        text = link.get_text().strip()
        if re.search(pattern, text):
            # Extract the year using regex
            year_match = re.search(r'20(0[5-9]|1[0-9]|2[0-3])', text)
            year = year_match.group(0) if year_match else None
            
            if year:
                # Get the href attribute
                href = link.get('href')
                if href:
                    # Construct full URL
                    file_url = urljoin("https://www.census.gov", href)
                    
                    # Construct output filename
                    filename = f"migration_flows_{year}.xlsx"
                    filepath = os.path.join(output_dir, filename)
                    
                    try:
                        # Download the file with updated headers
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                            'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel'
                        }
                        print(f"Downloading {filename}...")
                        file_response = requests.get(file_url, headers=headers, allow_redirects=True)
                        
                        # Print debug info
                        print(f"URL: {file_url}")
                        content_type = file_response.headers.get('Content-Type', 'No content type')
                        print(f"Content-Type: {content_type}")
                        
                        if file_response.status_code == 200:
                            # Determine file extension based on content type
                            if 'application/vnd.ms-excel' in content_type:
                                extension = '.xls'
                            else:
                                extension = '.xlsx'
                            
                            # Update filename with correct extension
                            filename = f"migration_flows_{year}{extension}"
                            filepath = os.path.join(output_dir, filename)
                            
                            # Save the file
                            with open(filepath, 'wb') as f:
                                f.write(file_response.content)
                            
                            # Verify the file is a valid Excel file
                            try:
                                if extension == '.xls':
                                    df = pd.read_excel(filepath, engine='xlrd')
                                else:
                                    df = pd.read_excel(filepath, engine='openpyxl')
                                downloaded += 1
                                print(f"Successfully downloaded and verified {filename}")
                            except Exception as excel_error:
                                print(f"Downloaded file is not a valid Excel file: {str(excel_error)}")
                                # Remove invalid file
                                os.remove(filepath)
                        else:
                            print(f"Failed to download {filename}. Status code: {file_response.status_code}")
                    
                    except Exception as e:
                        print(f"Error downloading {filename}: {str(e)}")

    print(f"\nDownload complete. Successfully downloaded {downloaded} files.")

if __name__ == "__main__":
    download_migration_flows() 
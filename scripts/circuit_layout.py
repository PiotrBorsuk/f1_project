import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.formula1.com/en/racing/2023/netherlands/circuit.html"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the div with the specified class
    div = soup.find('div', class_='col-span-12 desktop:col-span-7')
    
    if div:
        # Find the img tag within the div
        img = div.find('img')
        
        if img and 'src' in img.attrs:
            # Get the src attribute of the img tag
            img_src = img['src']
            print(f"Image source found: {img_src}")
            
            # Optionally, download the image
            img_response = requests.get(img_src)
            if img_response.status_code == 200:
                with open('circuit_image.jpg', 'wb') as file:
                    file.write(img_response.content)
                print("Image downloaded as 'circuit_image.jpg'")
            else:
                print("Failed to download the image")
        else:
            print("No image found in the specified div")
    else:
        print("Div with specified class not found")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
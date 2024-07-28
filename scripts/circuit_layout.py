import requests
from bs4 import BeautifulSoup
import os


def fetch_track_img(year: int, track: str):
    url = f"https://www.formula1.com/en/racing/{year}/{track}/circuit.html"

    # save_directory = "s"

    # os.makedirs(save_directory, exist_ok=True)

    response = requests.get(url)
    print('ok')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        div = soup.find('div', class_='col-span-12 desktop:col-span-7')
        
        if div:
            img = div.find('img')
            
            if img and 'src' in img.attrs:
                img_src = img['src']
                print(f"Image source found: {img_src}")

                img_response = requests.get(img_src)
                if img_response.status_code == 200:
                    file_path = os.path.join('static', 'track_layout.png')
                    with open(file_path, 'wb') as file:
                        file.write(img_response.content)
                    print("Image downloaded as 'track_layout.png'")
                else:
                    print("Failed to download the image")
            else:
                print("No image found in the specified div")
        else:
            print("Div with specified class not found")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
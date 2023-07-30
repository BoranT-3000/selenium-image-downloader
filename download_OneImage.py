import requests

def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded and saved as {filename}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'https://external-content.duckduckgo.com/iu/...' with the actual image URL.
image_url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.themoviedb.org%2Ft%2Fp%2Foriginal%2FnfqXutLdBBo1G36Mt5iHSJFjmLT.jpg&f=1&nofb=1&ipt=500448fe723618816d18783a45e1967d08d9e2201f2ee38df5961aff0851f190&ipo=images'
filename = 'downloaded_image.jpg'  # Specify the filename and extension you want to save the image as.

download_image(image_url, filename)


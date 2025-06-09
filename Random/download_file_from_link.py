from requests import get
from utils import get_all_links_from_website
from pprint import pprint
def download_file_from_link(url: str, file_name=""):
    if not file_name:
        file_name = url.split("/")[-1]
    """
    Downloads a file from the given URL and saves it with the specified file name.
    
    :param url: The URL of the file to download.
    :param file_name: The name to save the downloaded file as.
    """
    response = get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved as {file_name}.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


links = [
    "https://marshallhh.weebly.com/uploads/2/3/0/3/23035522/quiz_14-1_with_answers.pdf",
    "https://marshallhh.weebly.com/uploads/2/3/0/3/23035522/quiz_14-2_with_answers.pdf",
    "https://marshallhh.weebly.com/uploads/2/3/0/3/23035522/quiz_14-3_with_answers.pdf",
    "https://marshallhh.weebly.com/uploads/2/3/0/3/23035522/review_ws_with_answers.pdf",
    "https://marshallhh.weebly.com/uploads/2/3/0/3/23035522/practice_test_b.pdf"
]
pprint(links)

# More pythonic way:
list(map(download_file_from_link, links))

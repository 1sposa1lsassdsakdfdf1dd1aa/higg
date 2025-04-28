import requests
import re

# Function to fetch main domain from iframe
def fetch_main_domain(url):
    response = requests.get(url, verify=False)
    iframe_src = re.search(r'<iframe[^>]+src=["\'](https:\/\/[^"\']+)["\']', response.text)
    if iframe_src:
        iframe_url = iframe_src.group(1)
        domain_with_slash = re.sub(r'\/$', '', iframe_url) + '/'
        domain_without_slash = re.sub(r'\/$', '', iframe_url)
        return domain_with_slash, domain_without_slash
    else:
        raise Exception("No iframe src found starting with https.")

# Function to read the user-agent from a file
def read_user_agent():
    with open('logo/useragent.txt', 'r') as file:
        return file.read().strip()

# Function to process the m3u playlist
def process_playlist(main_domain_with_slash, main_domain_without_slash, user_agent):
    with open('playlist.m3u', 'r') as file:
        playlist_content = file.read()

    updated_playlist = re.sub(
        r'(https?:\/\/[^\s|]+)\|Referer=[^\|]+\|User-Agent=[^\|]+\|Origin=[^\s"\']+',
        lambda match: f"{match.group(1)}|Referer={main_domain_with_slash}|User-Agent={user_agent}|Origin={main_domain_without_slash}",
        playlist_content
    )

    with open('updated_playlist.m3u', 'w') as file:
        file.write(updated_playlist)

    print("Playlist updated successfully!")

if __name__ == '__main__':
    url = "https://miztv.top/total/stream-779.php"
    
    # Fetch domains
    main_domain_with_slash, main_domain_without_slash = fetch_main_domain(url)
    
    # Read user-agent from file
    user_agent = read_user_agent()
    
    # Process the playlist
    process_playlist(main_domain_with_slash, main_domain_without_slash, user_agent)

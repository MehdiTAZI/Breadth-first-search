import requests
from collections import deque

import urllib.parse
from bs4 import BeautifulSoup


def BFS_ALGORITHM(url):
  # queue to store the URLs to be visited
  queue_to_visit = deque([url])
  # set of URLs that have been visited
  visited = set()

  # relation between parent link, child link and depth of the current link
  parent_child_relation = {}
  parent_child_relation[url] = {'parent': None, 'depth': 0}

  while queue_to_visit:
    # retreive the next URL to visit from the queue, it depth and parent url
    current_url = queue_to_visit.popleft()
    current_depth = parent_child_relation[current_url]['depth']
    parent_url = parent_child_relation[current_url]['parent']

    #print the hearchy
    print("[",parent_url,"]","=" * current_depth, ">",current_url)
    
    # add the visited url to the set of visited urls
    visited.add(current_url)

    # get the URL content
    try:
      response = requests.get(current_url)
    except requests.RequestException as e:
      # print the error 
      print("[ERROR] : " , e) 
   
      continue

    # parse the request content
    soup = BeautifulSoup(response.text, "html.parser")

    # retreive all page links (<a>)
    links = soup.find_all("a")

    # add the links to the queue
    for link in links:
      next_url = link.get("href")
      if next_url is None or next_url in visited:
        # Skip the link if it is None or has already been visited
        continue
      # Parse the URL to check if it is valid
      parsed_url = urllib.parse.urlparse(next_url)
      if parsed_url.scheme and parsed_url.netloc:
        # The URL is valid, so add it to the queue
        queue_to_visit.append(next_url)
        parent_child_relation[next_url] = {'parent': current_url, 'depth': current_depth+1}
        

  return visited

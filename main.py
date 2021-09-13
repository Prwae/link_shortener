import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import argparse


def is_bitlink(url_link, head):
  url = f"https://api-ssl.bitly.com/v4/bitlinks/{url_link}"
  response = requests.get(url, headers=head)
  return response.ok


def shorten_link(head, url_link):
  body = {
    "long_url": url_link
  }

  url = "https://api-ssl.bitly.com/v4/bitlinks"
  response = requests.post(url, headers=head, json=body)
  response.raise_for_status()
  return response.json()["id"]


def count_clicks(bitlink, head):
  url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
  response = requests.get(url, headers=head)
  response.raise_for_status()
  return response.json()["total_clicks"]


if __name__ == "__main__":
  load_dotenv()

  headers = {
    "Authorization": os.environ["BITLY_TOKEN"]
  }

  parser = argparse.ArgumentParser(
    description="Сокращение ссылок"
  )
  parser.add_argument("link", help="Ссылка для сокращения или битлинк для получения информации о нем")
  link = parser.parse_args().link

  parsed_link = urlparse(link)
  link_without_scheme = f"{parsed_link.netloc}{parsed_link.path}"

  if is_bitlink(link_without_scheme, headers):
    try:
      print("Кликов всего: ", count_clicks(link_without_scheme, headers))
    except requests.exceptions.HTTPError:
      print("Ошибка при подсчете кликов")
  else:
    try:
      print("Битлинк", shorten_link(headers, link))
    except requests.exceptions.HTTPError:
      print("Ошибка при сокращении ссылки")

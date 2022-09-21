"""
Scraping Books Online - Beta Version
Author: Baptiste Hornecker
Date: September 2022
Target: http://books.toscrape.com/

Functions to go through site pages, find categories of books 
and links to corresponding individual product pages
"""

import requests
from bs4 import BeautifulSoup

import product_page
import outputs



def explore_books_on_page(page_url: str, books_infos: list)-> bool:
	"""For a given URL, extract the books and "loop" on them
	
	Takes the URL of a page, and a list of dictionaries to
	append retrieved book informations in
	Returns False in case the page could not be loaded
	"""

	# Let's get the page, if it exists (error message not required here)
	page = requests.get(page_url)
	if page.status_code != 200:
		return False

	# Get all links in the page
	soup = BeautifulSoup(page.content, 'html.parser')
	links = soup.find_all("a")
	
	# Skip links if they don't contain an image whose class is "thumbnail" (= a book)
	for link in links:
		if link.contents[0].find("thumbnail") == -1:
			continue

		# Extracted links are relative, turn them into full URLs
		href = link.get("href")
		book_url = "http://books.toscrape.com/catalogue/"
		book_url += href.replace("../", "")
		
		# DEBUG
		print(book_url)
		
		# Call subroutine to extract this book, and if something is returned store it
		book_dict = product_page.retrieve_book(book_url)
		if book_dict:
			books_infos.append(book_dict)
	
	return True



def scrape_category(category: str, output_name: str)-> bool:
	"""Extract categories and their links form main website page and "scrapes" the given one
	
	If first parameter is empty, we "scrape" all categories of books!
	Each of them will be stored in a separate CSV file.
	Second parameter is a name for the output folder.
	"""
	
	# Get ready with output folders
	if not outputs.create_folders(output_name):
		print("Error: could not create output folders - quitting")
		quit()
	
	main_url = "http://books.toscrape.com/"
	
	# If site seems to be unavailable, stop immediately
	page = requests.get(main_url)
	if page.status_code != 200:
		print(f"ERROR {page.status_code}, could not retrieve page {page_url}\n")
		return False
	
	# The links we are interested in start with "catalogue/category/"
	soup = BeautifulSoup(page.content, 'html.parser')
	links = soup.find_all("a")
	
	for link in links:
		href = link.get("href")
		
		# Link to a category detected, extract its name inside the link
		if href.startswith("catalogue/category/"):
			category_name = link.contents[0]
			category_name = category_name.replace("\n", "")
			category_name = category_name.strip()
			print(f"Category found: {category_name}")
			
			# Skip the first category, which is just all books
			if category_name == "Books":
				continue

			# We have to scrape this one - pages will be named page-x.html 
			if (category_name == category) or (not category):
				category_url = f"{main_url}{href}"
				category_url = category_url.replace("index.html", "")
				page_nbr = 1
				books_infos = []
				
				# Enumerate pages for a category until one of them does not exist
				while True:
					if page_nbr == 1:
						page_url = f"{category_url}index.html"
					else:
						page_url = f"{category_url}page-{page_nbr}.html"
					
					print(page_url)
					if not explore_books_on_page(page_url, books_infos):
						break
					
					page_nbr += 1
				
				outputs.store_books(output_name, books_infos)
					
	return True

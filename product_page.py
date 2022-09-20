"""
Scraping Books Online - Beta Version
Author: Baptiste Hornecker
Date: September 2022
Target: http://books.toscrape.com/

Function to download informations about a book from its product page.
"""

import requests
from bs4 import BeautifulSoup



def retrieve_book(book_url: str)-> dict:
	"""For a given URL, returns a dictionnary containing book infos
	
	Entries in the dictionary will be:
	book_title, product_page_url, UPC, price_excluding_tax, price_including_tax,
	number_available, review_rating, image_url, product_description, category
	"""

	# Some space between different calls to this functions
	print("")

	# Retrieve page, and give up this book if the returned status is not "HTTP 200"
	page = requests.get(book_url)
	if page.status_code != 200:
		print(f"ERROR {page.status_code}, could not retrieve page {book_url}\n")
		return None

	# book_title: appears in several places, especially inside the only <h1> tag
	soup = BeautifulSoup(page.content, 'html.parser')
	title_tag = soup.find_all('h1')
	book_title = title_tag[0].get_text()

	# Initialize dictionary with book title and URL and inform user
	book_infos = {"book_title":book_title, "product_page_url":book_url}
	print(f"book_title: {book_title}")
	print(f"product_page_url: {book_url}")


	# UPC, both prices and availability share a same table and are located inside the same tags
	tr_tag_table = soup.find_all('tr')

	# The lines we are dealing with typically look like: <th>UPC</th><td>a897fe39b1053632</td>
	for table_element in tr_tag_table:

		# Clean <tr>, </tr> tags and newlines
		string = str(table_element)
		string = string.replace("<tr>", "")
		string = string.replace("</tr>", "")
		string = string.replace("\n", "")

		# Split content in the middle, clean remaining tags
		content_split = string.split("</th>")

		property_name = content_split[0]
		property_name = property_name.replace("<th>", "")

		property_value = content_split[1]
		property_value = property_value.replace("<td>", "")
		property_value = property_value.replace("</td>", "")

		# Retain entries we are interested in
		if property_name=="UPC":
			book_infos["UPC"] = property_value
			print(f"UPC: {property_value}")

		# For prices, extract the value without the unit
		elif property_name=="Price (excl. tax)":
			book_infos["price_excluding_tax"] = property_value[1:]
			print(f"price_excluding_tax: {property_value}")

		elif property_name=="Price (incl. tax)":
			book_infos["price_including_tax"] = property_value[1:]
			print(f"price_including_tax: {property_value}")

		# Default: 0 in stock. If the pattern "In stock" is detected, extract value
		elif property_name=="Availability":
			number_available = 0
			
			if property_value.startswith("In stock"):
				property_value = property_value.replace("In stock (", "")
				property_value = property_value.replace(" available)", "")
				number_available = int(property_value)
			
			book_infos["number_available"] = number_available
			print(f"Availability: {number_available}")

		else:
			continue
	
	# The rating is encoded as class name, refering to a CSS element which renders stars
	# Problem: we first need to filter out those classes in the "recently viewed products"
	# HTML elements, or they will pollute our results
	for product in soup.find_all("article", class_="product_pod"): 
		product.decompose()
    
	if len(soup.find_all("p", class_="star-rating One")):
		rating = "1"
	elif len(soup.find_all("p", class_="star-rating Two")):
		rating = "2"
	elif len(soup.find_all("p", class_="star-rating Three")):
		rating = "3"
	elif len(soup.find_all("p", class_="star-rating Four")):
		rating = "4"
	else:
		rating = "5"

	book_infos["review_rating"] = rating
	print(f"review_rating: {rating}")

	# The URL for the image is straightforward to find, as there is a single image
	img = soup.find("img")
	src = img.get("src")
	
	# Before storing this URL, we need to transform it (it is a relative one)
	src = src.replace("../", "")
	src = f"http://books.toscrape.com/{src}"
	book_infos["image_url"] = src
	print(f"image_url: {src}")

    # Book category, can be isolated in a link starting with "../category/books/"
	links = soup.find_all("a")
    
	for link in links:
		href = link.get("href")
		if href.startswith("../category/books/"):
			book_infos["category"] = link.contents[0]
			break

	print(f"category: {link.contents[0]}")

	# Book description: extract the only paragraph associated to no class
	paragraph = soup.find("p", class_=None)
	paragraph_text = str(paragraph)
	paragraph_text = paragraph_text.replace("<p>", "")
	paragraph_text = paragraph_text.replace("</p>", "")
	paragraph_text = paragraph_text.replace("...more", "")
	book_infos["product_description"] = paragraph_text
	
	# Printing description is a bit too verbose...
	# print(f"product_description: {str(paragraph_text)}")

	# Leave some space in terminal and return extracted informations
	print("")
	return book_infos

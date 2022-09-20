"""
Scraping Books Online - Beta Version
Author: Baptiste Hornecker
Date: September 2022
Target: http://books.toscrape.com/

Main file
"""

import product_page
import outputs



def test_1():
	"""Test 1: Get a single book
	"""
	book_url = "http://books.toscrape.com/catalogue/between-shades-of-gray_128/index.html"
	book_infos = product_page.retrieve_book(book_url)
	print(book_infos)
	
	# Output test
	output_name = "between-shades-of-gray-test-1"
	if not outputs.create_folders(output_name):
		quit()
	books_data = []
	books_data.append(book_infos)
	outputs.store_books(output_name, books_data)



# Script starts here
if __name__ == '__main__':

	test_1()


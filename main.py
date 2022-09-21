"""
Scraping Books Online - Beta Version
Author: Baptiste Hornecker
Date: September 2022
Target: http://books.toscrape.com/

Main file
"""

import explore_categories
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



def test_2():
	"""Test 2: Get links to books in a page and explore all of them
	"""
	book_infos = []
	output_name = "historical-fiction-test-2"
	book_url = "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/page-2.html"
	explore_categories.explore_books_on_page(book_url, book_infos)
	
	# Output...
	if not outputs.create_folders(output_name):
		quit()
	outputs.store_books(output_name, book_infos)



def test_3():
	"""Test 3: Try the whole Religion category (single page)
	"""
	explore_categories.scrape_category("Religion", "religion-test-3")



def test_4():
	"""Test 4: Swallow the whole "Sequential Art" category with four pages
	"""
	explore_categories.scrape_category("Sequential Art", "sequential-art-test-4")



def test_5():
	"""Test 5: Get all categories of books and loop on them
	"""
	explore_categories.scrape_category("", "whole site")
	


# Script starts here
if __name__ == '__main__':

	# test_1()
	# test_2()
	# test_3()
	# test_4()
	test_5()


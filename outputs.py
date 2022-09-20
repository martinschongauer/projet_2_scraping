"""
Scraping Books Online - Beta Version
Author: Baptiste Hornecker
Date: September 2022
Target: http://books.toscrape.com/

Function to export data (CSV format) and download pictures.
Output folders are also created here.
"""

import csv
import requests
import os
import shutil
import re



def create_folders(output_name: str)-> bool:
	"""Create output folders for the data
	
	   output_name if the name of the output directory to create
	"""
	
	# Create a folder in current working directory, overwrite any existing one
	out_dir = os.path.join(".", output_name)
	try:
		shutil.rmtree(output_name)
	except:
		pass
	
	try:
		os.mkdir(output_name)
	except:
		print("Error: could not create output directory")
		return False
	
	# Create a folder inside it for pictures
	output_name = os.path.join(output_name, "Pictures")
	try:
		os.mkdir(output_name)
	except:
		print("Error: could not create Pictures directory")
		return False

	return True


def store_books(output_name: str, books_data: list)-> bool:
	"""Stores books_data list in CSV format + download pictures
	
	   output_name if the name of the output directory to create
	   books_data is a list of dictionnaries, one for each book
	   
	   Recall: books_data fields are book_title, product_page_url,
	   UPC, price_excluding_tax, price_including_tax, number_available,
	   review_rating, image_url, category, product_description.
	"""
	
	# If the list is empty, nothing to do but assume it is OK
	if not books_data:
		return True
	
	# Get category name from first book and "deduce" CSV filename
	book_category = books_data[0]["category"] 
	out_csv = os.path.join(".", output_name)
	out_csv = os.path.join(out_csv, f"{book_category}.csv")
	
	# Create CSV header (first row)
	csv_header = ["book_title", "product_page_url", "UPC", "price_excluding_tax", 
				"price_including_tax", "number_available", "review_rating",
				"image_url", "category", "product_description"]
	
	with open(out_csv, "w") as csv_file:
		# Create writer object and write first row
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow(csv_header)
		
		# Loop on books -> output !
		for book in books_data:
			row = [book["book_title"], book["product_page_url"], book["UPC"], book["price_excluding_tax"], 
				book["price_including_tax"], book["number_available"], book["review_rating"],
				book["image_url"], book["category"], book["product_description"]]
			writer.writerow(row)
			
			# Last but not least, download picture
			response = requests.get(book["image_url"])
			out_pic = os.path.join(".", output_name)
			out_pic = os.path.join(out_pic, "Pictures")
			
			# Some characters can create trouble in filenames, remove non-isalnum ones
			pattern = re.compile('\W')
			filtered_name = re.sub(pattern, '', book["book_title"])
			out_pic = os.path.join(out_pic, filtered_name)
			out_pic += ".jpg"
			
			# Save picture, here errors will just issue warnings
			try:
				with open(out_pic, "wb") as pict:
					pict.write(response.content)
					pict.close()
			except:
				print("WARNING: Could not save picture for: {filtered_name}")

	csv_file.close()
	return True

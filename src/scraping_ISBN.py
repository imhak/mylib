import re
import requests
import json
from src.database_methods import mysql_database, mysql_check_database

def getPage(URI, ISBN):
	try:
		req= requests.get(URI).json()
		print('Succ getting book json page')
	except Exception as e:
		return None
	return req

def parse(json_str, ISBN, json_attribute=None):
	attributes_to_scrape= ['title', 'subtitle', 'authors', 'publisher', 'publishedDate', 'printedPageCount', 'categories']
	attributes_data= []
	if json_attribute == None:
		# do here
		for attribute in attributes_to_scrape:
			try:
				data= json_str['volumeInfo'][attribute]
				attributes_data.append(data)
			except Exception as e:
				print('failed to get', ISBN, attribute)
				attributes_data.append(None)
		return attributes_data
	else:
		try:
			return json_str['items'][0][json_attribute]
		except Exception as e:
			return None

def Crowlies(API_URI, ISBN_list, book_path):
	count=0
	for ISBN in ISBN_list: 
		if ISBN != None:
			check_ISBN= mysql_check_database(book_path[count], ISBN)
			if check_ISBN.check_availability():
				full_URI= API_URI+str(ISBN)
				json_str= getPage(full_URI, ISBN)
				if json_str != None:
					ISBN_selfLink= parse(json_str, ISBN, 'selfLink')
					if ISBN_selfLink != None:
						check_ISBN.input_data()
						json_str= getPage(ISBN_selfLink, ISBN)
						if json_str != None:
							ISBN_attributes = parse(json_str, ISBN)
							ISBN_attributes.insert(0, ISBN)
							Object_database= mysql_database(ISBN_attributes)
							Object_database.input_data()
						else:
							print('Failed API request attributes for', ISBN)
					else:
						print('ISBN not in Google Books API Database', ISBN)
				else:
					print('Failed API request for', ISBN)
			else:
				print('ISBN already in database')	
		count+=1
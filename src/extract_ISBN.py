from pdfminer.high_level import extract_text
from PyPDF2 import PdfFileReader
import re, glob

class ISBN_class(object):
	"""docstring for ISBN_class"""
	def __init__(self, path):
		super(ISBN_class, self).__init__()
		self.path = path
		self.re_ISBN= re.compile('\d\d\d\-?\d\-?\d\d\d\d\-?\d\d\d\d\-?\d')

	def get_all_pdf(self):
		list_pdf_in_dir= glob.glob(str(self.path)+'/*.pdf')
		return list_pdf_in_dir

	def parse_ISBN_pdfminer(self, pdf):
		try:
			extracted_text= extract_text(pdf, page_numbers=range(10))
			ISBN_value= re.search(self.re_ISBN, extracted_text)
		except Exception as e:
			print('Failed parsing ISBN using pdfminer library', e)
			ISBN_value= None
		return ISBN_value

	def parse_ISBN_PyPDF2(self, pdf):
		with open(pdf, 'rb') as f_read:
			try:
				pdf_read= PdfFileReader(f_read)
				for page_number in range(3):
					page= pdf_read.getPage(page_number)
					page_text= page.extractText()
					ISBN_value= re.search(self.re_ISBN, page_text)
					if ISBN_value != None:
						ISBN_value= ISBN_value.group()
			except Exception as e:
				print('Failed parsing ISBN using PyPDF2 library', e)
				ISBN_value= None
		return ISBN_value

	def normalize_ISBN(self, raw_ISBN):
		return_ISBN= raw_ISBN.replace('-', '')
		return return_ISBN
			
	def get_ISBN(self):
		list_returned_ISBN=[]

		if type(self.path) != list:
			returned_ISBN= self.parse_ISBN_PyPDF2(self.path)
			if returned_ISBN == None:
				returned_ISBN= self.parse_ISBN_pdfminer(self.path)
			if returned_ISBN == None:
				print(f'Failed to get ISBN for {self.path} using available libraries')
			else:
				returned_ISBN= self.normalize_ISBN(returned_ISBN)
			list_returned_ISBN.append(returned_ISBN)
		else:
			for pdf in self.path:
				returned_ISBN= self.parse_ISBN_PyPDF2(pdf)
				if returned_ISBN == None:
					returned_ISBN= self.parse_ISBN_pdfminer(pdf)
				if returned_ISBN == None:
					print(f'Failed to get ISBN for {pdf} using available libraries')
				else:
					returned_ISBN= self.normalize_ISBN(returned_ISBN)
				list_returned_ISBN.append(returned_ISBN)

		return list_returned_ISBN
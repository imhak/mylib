from src.monitor_folder import monitor_folder
from src.scraping_ISBN import Crowlies
from src.extract_ISBN import ISBN_class

def main():
	path= 'pdf_folder'
	obj_1= monitor_folder()
	obj_1.getDir()
	pdf_path_list= obj_1.return_pdf_list

	obj_2= ISBN_class(pdf_path_list)
	ISBN_path_list= obj_2.get_ISBN()

	API_URI= "https://www.googleapis.com/books/v1/volumes?q=isbn:"
	Crowlies(API_URI, ISBN_path_list, pdf_path_list)

if __name__ == '__main__':
	main()
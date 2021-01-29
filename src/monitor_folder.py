import os, glob

class monitor_folder(object):
	"""docstring for monitor_folder"""
	def __init__(self):
		super(monitor_folder, self).__init__()
		#self.full_dir_path = full_dir_path
		self.return_pdf_list=[]

	def get_all_pdf(self):
		list_pdfs= glob.glob('scrapped_pdf/*.pdf')
		return list_pdfs

	def move_file(self):
		os.system("mv pdf_folder/*.pdf scrapped_pdf")

	def getDir(self):
		self.move_file()
		self.return_pdf_list= self.get_all_pdf()
		
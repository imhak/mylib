import pymysql
import getpass
import sys

class mysql_database(object):
	"""docstring for mysql_database"""
	def __init__(self, one_list=None, df_list=None):
		super(mysql_database, self).__init__()
		self.one_list = one_list
		self.df_list= df_list

	def normalize_data(self):
		self.TAGS= []
		for attribute in self.one_list[1:]:
			if type(attribute) != list:
				self.TAGS.append(attribute)
				attribute_index= self.one_list.index(attribute)
				self.one_list.pop(attribute_index)
		self.AUTHORS= self.one_list[1]
		self.CATEGORIES= self.one_list[2]

		self.CATEGORIES_v2=[]
		for cat in self.CATEGORIES:
			self.CATEGORIES_v2.append(cat.split(' / '))

		self.CATEGORIES= [i for cat in self.CATEGORIES_v2 for i in cat]

	def database_authentication(self):
		print('Enter Database Credentials:')
		user_username= 'admin_lab'#input('Enter Username: ')
		user_password= 'foo'#getpass.getpass('Enter Password: ')
		sql_host= 'localhost'#input('Enter Host IP/Name: ')
		user_database= 'LAB'#input('Enter Database Name: ')

		parameters= {
			'user' : user_username,
			'password' : user_password,
			'host' : sql_host,
			'database' : user_database
		}
		return parameters

	def database_connection_object(self):
		user_credentials= self.database_authentication()
		while True:
			try:
				connection_object= pymysql.connect(**user_credentials)
				break
			except Exception as e:
				print('Error connecting to database: ', e)
				option= input('Try again? Y/N')
				if option == 'N': sys.exit()
		return connection_object

	def check_availability(self, connection_obj, table_name, column_name, attr):
		cursor_object_dict= connection_obj.cursor(pymysql.cursors.DictCursor)

		sql_query= "SELECT %s FROM %s;"
		cursor_object_dict.execute(sql_query%(column_name, table_name))
		result_set= cursor_object_dict.fetchall()
		x= True
		for row in result_set:
			if attr == row[column_name]: x= False
		return x

	def create_database_table(self):
		connection_obj= self.database_connection_object()
		# input SQL command here

	def input_data(self):
		connection_obj= self.database_connection_object()
		cursor_object= connection_obj.cursor()
		
		self.normalize_data()

		sql_input_query= "INSERT INTO BOOK_TAG VALUES (%s,%s,%s,%s,%s,%s);"

		cursor_object.execute(sql_input_query%(self.one_list[0], self.TAGS[0], self.TAGS[1], self.TAGS[2], self.TAGS[3], self.TAGS[4]))

		for i in self.AUTHORS:
			if self.check_availability(connection_obj, 'AUTHOR', 'Author', i):
				sql_input_query= "INSERT INTO AUTHOR VALUES (%s);"
				cursor_object.execute(sql_input_query%(i))

			sql_input_query= "INSERT INTO BOOK_NAME_AUTHOR VALUES (%s,%s);"
			cursor_object.execute(sql_input_query%(self.one_list[0], i))

		for i in self.CATEGORIES:
			if self.check_availability(connection_obj, 'CATEGORY', 'Category', i):
				sql_input_query= "INSERT INTO CATEGORY VALUES (%s);"
				cursor_object.execute(sql_input_query%(i))
			sql_input_query= "INSERT INTO BOOK_NAME_CATEGORY VALUES (%s,%s);"
			cursor_object.execute(sql_input_query%(self.one_list[0], i))

		connection_obj.commit()
		connection_obj.close()

class mysql_check_database(mysql_database):
	"""docstring for mysql_check_database"""
	def __init__(self, path, ISBN):
		super(mysql_check_database, self).__init__()
		self.path = path
		self.ISBN = ISBN

	def check_availability(self):
		connection_obj= self.database_connection_object()
		cursor_object_dict= connection_obj.cursor(pymysql.cursors.DictCursor)

		table_name= 'BOOK_NAME'
		column_name= 'ISBN'

		sql_query= "SELECT %s FROM %s;"
		cursor_object_dict.execute(sql_query%(column_name, table_name))
		result_set= cursor_object_dict.fetchall()
		x= True
		for row in result_set:
			if self.ISBN == row[column_name]: x= False
		return x
		
	def input_data(self):
		connection_obj= self.database_connection_object()
		cursor_object= connection_obj.cursor()

		sql_input_query= "INSERT INTO BOOK_NAME(Book_Path,ISBN) VALUES (%s,%s);"
		cursor_object.execute(sql_input_query, (self.path, self.ISBN))

		connection_obj.commit()
		connection_obj.close()
		
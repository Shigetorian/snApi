# snApi
universal library for the development of soc. network, based on the yadisk library

Yadisk library: https://yadisk.readthedocs.io/ru/latest/docs.html

Требования:
- Аккаунт Яндекс
- Oauth-приложение с доступом api

Инструкция:
- На диске должны быть созданы папки users и files
- Токен приложения вставить в:

      def __fs_init(self):
        self.server_main = "<token>"
	
- все методы работают коректно только после выполнения метода init()
		
		def init(self):
			self.pbar = True
			self.__constant_init()
			self.__fs_init()
			# self.__thread_init()
			self.s0 = yadisk.YaDisk(token=self.server_main)
			try:
			    file = open('cash/usercash.json', mode='r')
			    rest = json.load(file)
			    self.pbar = False
			    return str(rest)
			except:
			    self.pbar = False
			    return False

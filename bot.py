'''
Titulo: BOT curtir comentários Instagram
Autor: Igor do Espírito Santo
Linguagem: Python
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import FirefoxOptions
import os
import time
import random
import PySimpleGUI as sg
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Util:
    #pega o log do argumento passado
    def getLog(self, e):
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)
        #temos também:
        #logging.INFO
        handler = logging.FileHandler('botCurteCommentLog.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info(e)
    #getLog

    def delay(self):
        time.sleep(random.randint(3, 5))
#Util

class InstagramBot:
    def __init__(self, username, password, rotations):
        self.util = Util()

        self.username           = username
        self.password           = password
        self.rotations          = int(rotations)

        self.driver     = webdriver.Firefox(executable_path=r'geckodriver\geckodriver.exe')
    #FECHA __init__

    def login(self):
        self.driver.get('https://www.instagram.com/')
        self.util.delay()

        user_element = self.driver.find_element_by_xpath("//input[@name='username']")
        user_element.clear()
        user_element.send_keys(self.username)

        pass_element = self.driver.find_element_by_xpath("//input[@name='password']")
        pass_element.clear()
        pass_element.send_keys(self.password)

        pass_element.send_keys(Keys.RETURN)
        self.util.delay()

        self.curtirComments()
    #FECHA login

    def scrollScreen(self, rotations):
        actRotation = 0
        yNow = None
        for i in range(1, rotations):
            try:
                # pega tamanho do scroll do document
                height = self.driver.execute_script("return document.documentElement.scrollHeight;")
                # pega a posY do scroll
                scrollY = self.driver.execute_script("return window.scrollY;")
                if scrollY == yNow:
                    sg.PopupError(f"Page is stoped!{os.linesep}")
                # faz o scroll descer até o final da pag
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.util.delay()
                yNow = scrollY
            except  Exception as e:
                self.util.getLog(e)
                print(f'SCROLL ERROR! - {e} *****')
            #try/except

            actRotation = actRotation + 1
            sg.Print(f"Pag rotação atual: {actRotation}{os.linesep}")
        #for
    #scrollScreen

    def countHrefs(self):
        try:
            # COMANDO PARA PEGAR ALGO PELA TAG_NAME
            jsScriptGet = 'var as = document.getElementsByTagName("a");' \
                          'var arr = Array.prototype.slice.call(as);' \
                          'console.log(arr);' \
                          'return arr;'
            hrefs = self.driver.execute_script(jsScriptGet)

            # EXTRAI APENAS A URL QUE QUEREMOS PARA CURTIR A FOTO
            picHrefs = [elem.get_attribute('href') for elem in hrefs]
            [href for href in picHrefs]
            #[href for href in picHrefs if self.hashtag in href]
            #[href for href in picHrefs]
            return picHrefs
        except Exception as e:
            self.util.getLog(e)
            print(f'SCROLL PAGE ERROR! - {e} *****')
    #countHrefs

    def toLikeFunc(self, picHrefs):
        sg.Print(f"{os.linesep}***************************************"
                 f"{os.linesep}Total: {len(picHrefs)}{os.linesep}"
                 f"***************************************{os.linesep}")
        countAux = 0
        for picHref in picHrefs:
            if 'p/' or 'reel/' in picHref:
                self.driver.get(picHref)
                self.util.delay()

                sg.Print(f"{os.linesep}*********************"
                         f"{os.linesep}Rotação atual: {countAux}{os.linesep}"
                         f"*********************{os.linesep}")

                jsScriptGet = 'var arr = document.getElementsByClassName("wpO6b ZQScA ");' \
                                'for(var i=0;i<arr.length;i++){' \
                                'arr[i].click();' \
                                '}'
                self.driver.execute_script(jsScriptGet)
                countAux = countAux + 1
                time.sleep(1)
        # for
    #toLikeFunc

    #CRIA FUNCAO curtirFotos
    def curtirComments(self):
        try:
            self.driver.get('https://www.instagram.com/explore/')
            self.util.delay()
        except Exception as e:
            self.util.getLog(e)
            print(f'GET EXPLORE PAGE ERROR! - {e} *****')

        self.scrollScreen(self.rotations)
        self.util.delay()
        picHrefs = self.countHrefs()

        sg.Print(f'{os.linesep}***************************************************************************'
                 f'{os.linesep}Total de links a visitar:{len(picHrefs)}'
                 f'{os.linesep}***************************************************************************'
                 f'{os.linesep}')

        self.toLikeFunc(picHrefs)

        # to close the browser
        self.driver.close()
        # to end the driver session
        self.driver.quit()
        sg.PopupOK("Bot process finished!")
        #FECHA for
    #FECHA curtirFotos
#InstagramBot

class TelaPython:
    #CRIA FUNCAO CONSTRUTOR
    def __init__(self):
        #LAYOUT
        layout = [
            #CRIA ELEMENTO NA TELA COM UM INPUT PARA RECEBER DADOS
            [sg.Text('')],
            [sg.Text('Usuário', size=(10, 0)), sg.Input(size=(30, 0), key='username', default_text='igor927482')],
            [sg.Text('Senha', size=(10, 0)), sg.Input(size=(30, 0), key='password', password_char='*', default_text='12131212aA@')],
            [sg.Text('')],
            [sg.Text('Rotações', size=(10, 0)), sg.Input(size=(30, 0), key='rotations', default_text='2')],
            [sg.Text('')],
            [sg.Button('Enviar Dados',size=(30, 0))]
            #CRIA TELA DE OUTPUT PARA MOSTRAR OS DADOS NO LAYOUT
            #[sg.Output(size=(50, 10))]
        ]
        #JANELA
        #CRIA A TELA E COLOCA OS ELEMENTOS DE LAYOUT NELA
        self.janela = sg.Window('Curte comentários em fotos instagram.').layout(layout)
    #FECHA __init__

    def Iniciar(self):
        while True:
            # EXTRAIR DADOS DA TELA
            self.button, self.values = self.janela.Read()
            username = self.values['username']
            password = self.values['password']
            rotations = self.values['rotations']

            logBot = InstagramBot(username, password, rotations)
            logBot.login()
        #FECHA while
    # FECHA Iniciar
#TelaPython

#INSTANCIA CLASSE TelaPython EM tela
tela = TelaPython()
tela.Iniciar()
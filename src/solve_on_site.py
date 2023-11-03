'''The connection between solver program and Weaver website.


Author:

    Ronit Samanta

Classes:

    SiteSolver

'''

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class SiteSolver:
    '''A class to fill out a Weaver solution on the website


    Methods:

        solve(solution: list[str])

        click_random()

        delete_all(num_words: int)

        get_incorrect_word() -> str


    Attributes:

        start - starting word of challenge

        end - ending word of challenge

    '''

    def __init__(self) -> None:
        '''Opens Weaver in Chrome and sets up for solving'''

        chrome_driver_path = '/path/to/chrome/driver'
        chr_options = Options()

        # keeps Chrome open after end of program
        chr_options.add_experimental_option('detach', True)
        self.__driver = webdriver.Chrome(options=chr_options,
                                         service=Service(executable_path=chrome_driver_path))

        self.__driver.get('https://wordwormdormdork.com')

        self.__setup()

    def __type_word(self, word: str) -> None:
        '''Types provided word into website

        Helper method
        '''

        for letter in word:
            self.__type_key(letter)
        while True:
            try:
                self.__enter.click()
                break
            except:
                pass

    def __type_key(self, char: str) -> None:
        '''Types a letter into website

        Helper method
        '''

        for key in self.__keys:
            if key.text == char:
                while True:
                    try:
                        key.click()
                        break
                    except:
                        pass

    def solve(self, solution: list[str]) -> None:
        '''Types out solution

        :param solution: list representation of final solution
        '''

        for word in solution:
            self.__type_word(word)

    def __setup(self):
        '''Locates buttons on website page

        Helper method
        '''
        self.__driver.execute_script("window.scrollTo(0, 1080)")
        self.__keys = self.__driver.find_elements(
            By.CLASS_NAME, 'characterButton')
        self.__enter = self.__driver.find_element(By.CLASS_NAME, 'enterButton')
        time.sleep(0.3)
        self.__start = self.__driver.find_element(
            By.CLASS_NAME, 'startWordRow').text.replace('\n', '')
        self.__end = self.__driver.find_element(
            By.CLASS_NAME, 'endWordRow').text.replace('\n', '')

    def click_random(self):
        '''Clicks the Random button on website to go to random
            challenge'''

        try:
            self.__driver.find_element(
                By.CLASS_NAME, 'playRandomGameButton').click()
        except:
            pass
        self.__setup()

    def delete_all(self, num_words: int):
        '''Deletes all words that have been typed

        :param num_words: Preferably the length of the found solution
                regardless of solution success
        '''

        delete = self.__driver.find_element(By.CLASS_NAME, 'deleteButton')
        for _ in range(num_words * 5):
            delete.click()

    def get_incorrect_word(self) -> str:
        '''Return the word that Weaver doesn't accept'''
        return self.__driver.find_elements(
            By.CSS_SELECTOR, 'div.inputRowsContainer div.row')[-1].text.replace('\n', '')

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

import glob
import os

import cv2
from django.core.management.base import BaseCommand

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from webscrapping.models import Resorts


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = r'https://www.skiresort.info/ski-resorts/'

        ratings_list = []

        options = webdriver.ChromeOptions()
        options.headless = True

        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        browser_ski_lifts = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        resort_links = []

        for i in range(1, 10):
            p_url = url + 'page' + '/' + str(i) + '/'
            browser.get(p_url)

            all_resort_per_page = browser.find_element(By.ID, 'resortList')

            links = all_resort_per_page.find_elements(By.CSS_SELECTOR, 'div.h3 > a')
            for el in links:
                resort_links.append(el.get_attribute('href'))

        slope_difficulty = []
        slope_length = [[] for el in resort_links]
        altitude = []

        price_adults = []
        price_youth = []
        price_children = []
        resort_names = []
        resort_lift_numbers = []

        for i in range(len(resort_links)):  # SKI-LIFT DETAILS

            browser_ski_lifts.get(resort_links[i] + 'ski-lifts')
            browser.get(resort_links[i])

            index = resort_links[i].find('t/')
            name = resort_links[i][index + 2:len(resort_links[i]) - 1]
            resort_names.append(name)

            slope_altitude_web_elements = browser.find_elements(By.ID, 'selAlti')

            if len(slope_altitude_web_elements) == 0:
                x = '0 m - 0 m (Difference 0 m)'
                altitude.append(x)
            else:
                altitude.append(slope_altitude_web_elements[0].text)

            slope_difficulty_web_elements = browser.find_elements(By.CLASS_NAME, 'desc')
            slope_difficulty = [el.text for el in slope_difficulty_web_elements for i in range(1)]

            slope_length_web_elements = browser.find_elements(By.CLASS_NAME, 'distance')
            for k in range(len(slope_length_web_elements)):
                if k != 3:
                    slope_length[i].append(slope_length_web_elements[k].text)

            try:
                adults_curr = browser.find_element(By.ID, 'selTicketA')
                if adults_curr.text.find('€') == -1:
                    adults = browser.find_element(By.ID, 'selTicketEurA')
                    i = adults.text.find(',')
                    euro = adults.text.find('€')
                    a = adults.text[euro + 1:i]
                    price_adults.append(a)
                else:
                    i = adults_curr.text.find(',')
                    euro = adults_curr.text.find('€')
                    a = adults_curr.text[euro + 1:i]
                    price_adults.append(a)

            except NoSuchElementException:
                adults = '0'
                price_adults.append(adults)
            try:
                youth_curr = browser.find_element(By.ID, 'selTicketY')
                if youth_curr.text.find('€') == -1:
                    youth = browser.find_element(By.ID, 'selTicketEurY')
                    i = youth.text.find(',')
                    euro = youth.text.find('€')
                    y = youth.text[euro + 1:i]
                    price_youth.append(y)
                else:
                    i = youth_curr.text.find(',')
                    euro = youth_curr.text.find('€')
                    y = youth_curr.text[euro + 1:i]
                    price_youth.append(y)
            except NoSuchElementException:
                youth = '0'
                price_youth.append(youth)
            try:
                child_curr = browser.find_element(By.ID, 'selTicketC')
                if child_curr.text.find('€') == -1:
                    child = browser.find_element(By.ID, 'selTicketEurC')
                    i = child.text.find(',')
                    euro = child.text.find('€')
                    c = child.text[euro + 1:i]
                    price_children.append(c)
                else:
                    i = child_curr.text.find(',')
                    euro = child_curr.text.find('€')
                    c = child_curr.text[euro + 1:i]
                    price_children.append(c)
            except NoSuchElementException:
                child = '0'
                price_children.append(child)

            try:
                rating = browser.find_element(By.ID, 'selRating')
                ratings_list.append(float(rating.text[:3]))
            except NoSuchElementException:
                no_rating = '0'
                ratings_list.append(float(no_rating))

            try:
                lift_number = browser.find_element(By.ID, 'selLiftstot')
                s = lift_number.text[len(lift_number.text) - 2:].replace(" ", "")
                resort_lift_numbers.append(s)

            except NoSuchElementException:
                resort_lift_numbers.append(None)

        for el in slope_length:
            if len(el) < 3:
                for i in range(3 - len(el)):
                    el.append('0')

        if len(slope_difficulty) == 4:
            slope_difficulty = slope_difficulty[:3]

        slope_altitude_list = [[number for number in el.split() if number.isdigit()] for el in altitude]
        for el in slope_altitude_list:
            print(el)

        # directory = r'C:\Users\tiberiu.ghimbas\Documents\Resorts img5'
        #
        # image_list = [cv2.imread(file) for file in glob.glob(r'C:/Users/tiberiu.ghimbas/Documents/Resorts img5/*.png')]

        # print(len(image_list))
        # print(image_list)

        full_dictionary = {'Name': [el for el in resort_names],
                           'Lift Numbers': [el for el in resort_lift_numbers],
                           'Rating': [el for el in ratings_list],
                           'Lowest point': [el[0] for el in slope_altitude_list],
                           'Highest point': [el[1] for el in slope_altitude_list],
                           'Difference': [el[2] for el in slope_altitude_list]}

        slope_difficulty_dictionary = {}

        for el in slope_difficulty:
            slope_difficulty_dictionary[el] = []

        for i in range(len(slope_difficulty)):
            for j in range(len(slope_length)):
                pos = slope_length[j][i].find(' km')
                slope_length[j][i] = slope_length[j][i][:pos]
                slope_difficulty_dictionary[slope_difficulty[i]].append(slope_length[j][i])

        prices = [[price_adults[i], price_youth[i], price_children[i]] for i in range(len(price_adults))]

        ski_pass_prices_dictionary = {'Adult ticket price': [el[0] for el in prices],
                                      'Youth ticket price': [el[1] for el in prices],
                                      'Children ticket price': [el[2] for el in prices]}

        full_dictionary.update(slope_difficulty_dictionary)
        full_dictionary.update(ski_pass_prices_dictionary)
        full_dictionary.update()

        Resorts.objects.all().delete()

        for i in range(len(full_dictionary['Name'])):
            name = full_dictionary['Name'][i]

            try:
                Resorts.objects.create(
                    name = full_dictionary['Name'][i],
                    rating = full_dictionary['Rating'][i],
                    lowest_point = full_dictionary['Lowest point'][i],
                    highest_point = full_dictionary['Highest point'][i],
                    difference = full_dictionary['Difference'][i],
                    easy = full_dictionary['Easy'][i],
                    intermediate = full_dictionary['Intermediate'][i],
                    difficult = full_dictionary['Difficult'][i],
                    adult_ticket = full_dictionary['Adult ticket price'][i],
                    youth_ticket = full_dictionary['Youth ticket price'][i],
                    children_ticket = full_dictionary['Children ticket price'][i],
                    resort_lift_number = full_dictionary['Lift Numbers'][i],
                    )
                print('%s added' % (name,))
            except :
                print('%s already exists' % (name,))

    print('Finished')




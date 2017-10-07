import os
from selenium import webdriver
from pytesseract import image_to_string
from PIL import Image
import numpy as np
from bs4 import BeautifulSoup

URL = "http://www.csisrmrmp.com/abhi"

class Attack():
	def __init__(self):
		self.driver = webdriver.Chrome(executable_path = os.curdir+'/chromedriver.exe')

	def attack(self,reg=None,dob=None):
		print ("Starting retreival for {} :".format(reg,dob))
		self.driver.get(URL);
		self.driver.find_element_by_id('reg_no').send_keys(reg)
		self.driver.find_element_by_id('dob').send_keys(dob)
		self.driver.find_element_by_id('captcha_code').send_keys("abc")
		self.driver.find_element_by_id('submit').click()
		self.driver.implicitly_wait(3)
		
		#Extraction
		print ("Extracting for {} :".format(reg,dob))
		soup = BeautifulSoup(self.driver.page_source)
		tables = soup.findAll('table')
		data = {}
		data['data'] = []
		c = 0
		t0 = tables[0].find('tbody');
		r = t0.findAll('tr');
		data['name'] = str(r[0].findAll('td')[0].text)
		data['reg'] = str(r[1].findAll('td')[0].text)
		print (data['name'], data['reg'])
		tbody = tables[1].find('tbody')
		for row in tbody.findAll('tr'):
			if c == 0 :
				c = 1
				continue
			cols = row.findAll('td')
			d = {}
			d['subject-code'] = str(cols[0].text)
			d['subject'] = str(cols[1].text)
			d['credits'] = int(cols[2].text)
			d['grade'] = str(cols[3].text)
			data['data'].append(d)
		for d in data['data']:
			print (d)
		return data

	def _get_captcha(self):
		elem = self.driver.find_element_by_id('captchaimg')
		loc = elem.location
		size = elem.size
		x,y = loc['x'],loc['y']
		w,h = size['width'],size['height']
		self.driver.save_screenshot('captcha.png')
		
		# Crop and rgb
		im = Image.open('captcha.png')
		im.crop((x,y,x+w,y+h)).save('captcha.png')
		
		# Cleanup
		im = Image.open('captcha.png')
		data = np.array(im)
		r1, g1, b1 = 60, 60, 60 # Original value
		r2, g2, b2 = 255, 255, 255 # Value that we want to replace it with
		red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
		mask = (red <= r1) & (green <= g1) & (blue <= b1)
		data[:,:,:3][mask] = [r2, g2, b2]
		im = Image.fromarray(data)
		im.save('captcha2.png')
		
		return image_to_string(Image.open('captcha2.png'))
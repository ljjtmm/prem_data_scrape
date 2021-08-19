from nerodia.browser import Browser
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import re
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

#Create browser
browser = Browser('chrome', options = options) 

seasons = ['2021/2022', '2020/2021', '2019/2020','2018/2019', '2017/2018', '2016/2017', '2015/2016', '2014/2015',
		   '2013/2014', '2012/2013', '2011/2012', '2010/2011', '2009/2010', '2008/2009', '2007/2008', '2006/2007',
		   '2005/2006', '2004/2005', '2003/2004', '2002/2003', '2001/2002', '2000/2001', '1999/2000', '1998/1999',
		   '1997/1998', '1996/1997', '1995/1996', '1994/1995', '1993/1994', '1992/1993']

season_id = [418, 363, 274, 210, 79, 54, 42, 27, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10,
			9, 8, 7, 6, 5, 4, 3, 2, 1]

statistics = ['goals', 'goal_assist', 'clean_sheet', 'appearances', 'mins_played' ,'yellow_card', 'red_card', 'total_pass',
			  'touches', 'total_scoring_att', 'hit_woodwork', 'big_chance_missed', 'total_offside', 'total_tackle',
			  'fouls', 'dispossessed', 'own_goals', 'total_clearance', 'clearance_off_line', 'saves', 'penalty_save', 
			  'total_high_claim', 'punches']

def variable_print(list):
	for i in range(len(list)):
		print(list[i])

pair = dict(zip(seasons, season_id))

def scrape(stat, season):
	id = pair[season]

	link = f'https://www.premierleague.com/stats/top/players/{stat}?se={id}'

	print(f"Fetching {stat} data for {season} season, with ID {id} from link {link}")

	browser.goto(link)

	time.sleep(10)

	goals_df = pd.read_html(browser.html)[0]

	while not browser.div(class_name=['paginationBtn', 'paginationNextContainer', 'inactive']).exists:
		#fire onClick event on page next element. If it was a button element (not a div element), we could simply use .click() 
		browser.div(class_name=['paginationBtn', 'paginationNextContainer']).fire_event('onClick')
		#append the table from this page with the existing goals dataframe. 

		goals_df = goals_df.append(pd.read_html(browser.html)[0]) 

	browser.close()
	print("Done! Writing data to csv.")

	goals_df = goals_df[goals_df['Stat'] > 0] 

	goals_df = goals_df.dropna(axis=1, how='all') 

	year = re.sub('[/]', '', season)
	
	goals_df.to_csv(f'data/epl_{stat}_{year}.csv', index=False) 


val_1 = input("Which variable would you like data for?:")

if val_1 not in statistics:
	print("That is not a valid statistic, please choose from the following:", variable_print(statistics))

else:
	val_2 = input("Which season would you like data for?:")

	if val_2 not in seasons:
		print("That is not a valid season, please choose from the following:", variable_print(seasons))

	else:
		scrape(val_1, val_2)





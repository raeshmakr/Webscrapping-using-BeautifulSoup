from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs ={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
row1 = table.find_all('tr', attrs ={'class':''})

row_length = len(row1)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
    date = table.find_all('td')[i*4].text
    
    rate = table.find_all('a')[i*2].text
    temp.append((date,rate)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('Date','Rate'))

#insert data wrangling here
df['Rate'] = df['Rate'].str.replace(",","")
df['Rate'] = df['Rate'].astype('float64')

df['Date'] = df['Date'].astype('datetime64')


#end of data wranggling 
df2 = df.copy()
df2 = df2.reset_index()
df2['month'] = df2['Date'].dt.to_period('M')

@app.route("/")
def index(): 
	
	card_data = f'{round(df.mean()[0],2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (7,7)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
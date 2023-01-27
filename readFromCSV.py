import pandas as pd
import csv

df = pd.read_csv("diamonds.csv")

#1 	מה מחיר היהלום הגבוהה ביותר
max_price = df['price'].max()
print(max_price)
#----------------------------------------------------------------------------------------#

#2.	מה המחיר הממוצע של יהלום?
# df = pd.read_csv("diamonds.csv")
mean_price = df['price'].mean()
print(mean_price)
#----------------------------------------------------------------------------------------#

#3. קיימים Ideal כמה יהלומים מסוג 

#"shape" is a function that give back the tuple contains the number of rows and columns in the DataFrame.
#It can also counts the rows by spesific colum, like the example:
ideal_count = df[df['cut']=='Ideal'].shape[0]
print(ideal_count)

ideal_count = df['cut'].shape[0]
print(ideal_count)
#----------------------------------------------------------------------------------------#

#4.	כמה צבעים שונים יש ליהלומים? מהם?
color_count = len(df['color'].unique())
print(color_count)

# another way
#The csv module reads the CSV file by rows, not by columns. Each row of the CSV file is represented as a list,
#  where each element of the list corresponds to a value in a column of the CSV file.
# the color column is the 3rh column , that in csv it is the 3rd row (list) and it start from index 0.
with open('diamonds.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # skip the header row
    colors = set()
    for row in reader:
        colors.add(row[2])
    print(len(colors))
    print(colors)


color_count = (df['color'].unique())
print(color_count)
#----------------------------------------------------------------------------------------#

#5.	Premium מה החציון קאראט של יהלומים מסוג ?
# premium_carats - contains object that include the name and number of what we need 
premium_carats = df[df['cut'] == 'Premium']['carat']
median_carat = premium_carats.median()
print(median_carat)
#----------------------------------------------------------------------------------------#

#6. cut לכל סוג  Carat צרו ממוצע  
cut_carat_avg = df.groupby('cut')['carat'].mean()
print(cut_carat_avg)
#----------------------------------------------------------------------------------------#

#7.	צרו ממוצע מחיר לכל סוג צבע.
color_price_avg = df.groupby('color')['price'].mean()
print(color_price_avg)


#-----------------------------------------CRUD-----------------------------------------------------------#

from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

@app.route('/avg_price_by_color', methods=['GET'])
def get_avg_price_by_color():
    df = pd.read_csv("diamonds.csv")
    color_price_avg = df.groupby('color')['price'].mean()
    return jsonify(color_price_avg.to_dict())

if __name__ == '__main__':
    app.run()

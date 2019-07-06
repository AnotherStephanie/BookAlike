from flask import render_template
from flask_app import app
from flask import request
from flask_app.a_Model import getReviews, getTitle, recommendBook#getUserIndex,
import pickle
import pandas as pd


@app.route('/')
@app.route('/index')
def recommender_input():
    return render_template("index.html")


#def index():
#    return render_template("index.html",
#       title = 'Home', user = { 'nickname': 'Stephanie' },
#       )
@app.route('/input')
def recommender_input2():
    return render_template("input.html")

@app.route('/output')

def recommender_output():
    myID = request.args.get('myID')
    myBook = request.args.get('myBook')#really book ID from index
    #This next line is the issue.
    recommendResult = getReviews(myID, myBook)
    
    titleResult = getTitle(myBook)
    
    reviewRatings = recommendResult[0]
    reviewTexts=recommendResult[1]
    grUsers = recommendResult[2]
    
    
    return render_template("output.html", 
                           grUser0 = grUsers[0],
                           grUser1 = grUsers[1],
                           grUser2 = grUsers[2],
                           reviewRatings0 = reviewRatings[0],
                           reviewRatings1 = reviewRatings[1],
                           reviewRatings2 = reviewRatings[2],
                           reviewTexts0 = reviewTexts[0], 
                           reviewTexts1 = reviewTexts[1], 
                           reviewTexts2 = reviewTexts[2], 
                           the_title=titleResult)
    
#def bookTitle_output():
#    myBook = request.args.get('myBook')#really book ID from index
#    #titleResult = getTitle(myBook)
#    titleResult = "O HAI!"
#    
#    return render_template("output.html", the_title="Hello!")



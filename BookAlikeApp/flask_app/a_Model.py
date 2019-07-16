import pickle
import pandas as pd
import numpy as np
import implicit
import random




#def getUserIndex (gruser_id):
#    userIndices = pickle.load(open('flask_app/userIndices.pkl', 'rb'))
#    myUserIndex=userIndices[userIndices["user_id_gr"]==gruser_id].index
#    return myUserIndex

def getTitle (myBook):
    bookList = pickle.load(open('flask_app/bookList.pkl', 'rb'))
    
    listy = bookList["book_id"].tolist()
    
    if int(myBook) in listy:
        myRow = bookList[bookList["book_id"]==int(myBook)]
        myTitle = myRow["title"].iloc[0]
    
    else:
        myTitle = "I'm sorry, we do not have enough information about this book."    
    
    return (myTitle)



def getReviews(myID, myBook='11870085'):
    
    #get from input
    model = pickle.load(open('flask_app/model.pkl', 'rb'))
    bookList = pickle.load(open('flask_app/bookList.pkl', 'rb'))
    userIndices = pickle.load(open('flask_app/userIndices.pkl', 'rb'))
    dfRev = pickle.load(open('flask_app/dfRev.pkl', 'rb'))#just coded reviews
    
    mySubtitle = "Here are reviews of this book from readers who are similar to you."
    mySubtitle = userIndices["user_id_gr"].sample()

    
    #Error handling for ids not in model
    booklisty = bookList["book_id"].tolist()
    userlisty = userIndices['user_id_gr'].tolist()
    
    if (int(myBook) not in booklisty) & (int(myID) not in userlisty):
    #    myID = 38974696#userIndices["user_id_gr"].sample(1, axis=1)
        myBook = '530965'
        myUserIndex=userIndices[userIndices['user_id_gr']==random.choice(userIndices['user_id_gr'])].index
        mySubtitle = "Nor do we have sufficient information about you as a user. As an apology gift, please enjoy three random reviews of the 1951 horror classic, The Day of the Triffids."
 
        
    elif int(myID) not in userlisty:
        myUserIndex=userIndices[userIndices['user_id_gr']==random.choice(userIndices['user_id_gr'])].index
        mySubtitle = "Unfortunately, we do not have enough information about you as a user to generate similar reviews. Here are three random reviews instead."
        
    elif int(myBook) not in booklisty:
        myBook = '4671'
        mySubtitle = "Please enjoy some reviews of The Great Gatsby instead, provided by readers who are similar to you."
          
    else:
        mySubtitle = "Here are reviews of this book from readers who are similar to you."
        myUserIndex=userIndices[userIndices['user_id_gr']==int(myID)].index
    
    
    #Convert userID to model index. Note, goodreads id must be recast as int
    #myUserIndex=userIndices[userIndices['user_id_gr']==int(myID)].index
    
    #now get ranked list of similar users, as a data frame;
    #rankings are labeled by in-model indices
    similarU = model.similar_users(myUserIndex[0], N=len(userIndices)) #ranking as list
    
    
    dfSU = pd.DataFrame(similarU, columns=["user_index", "score"])
    dfSU2 = userIndices.iloc[dfSU["user_index"]]
    dfSU2.reset_index(inplace=True, drop=True)
    dfSU3 = pd.concat([dfSU, dfSU2], axis=1)
    dfSU = dfSU3#ranking as data frame
    del([dfSU2, dfSU3])
    
    
    #now leave only reviews for coded readers, for myBook
    dfRevShort = dfRev[dfRev['book_id']==myBook]
    
    #merge onto ranked user data frame dfSU
    dfSU = pd.merge(left = dfSU, right = dfRevShort[["rating", "review_text", "user_code"]], 
                on="user_code", how="left")
    topReviews = dfSU[["user_id_gr", "rating", "review_text"]].dropna()
    topReviews = topReviews.head(3)
  
    
    #return ([topReviews["rating"].iloc[0], topReviews["review_text"].iloc[0], 
    #         topReviews["rating"].iloc[1], topReviews["review_text"].iloc[1],
    #          topReviews["rating"].iloc[2], topReviews["review_text"].iloc[2]])
    return (topReviews["rating"].tolist(), topReviews["review_text"].tolist(),
            topReviews["user_id_gr"].tolist(), mySubtitle)

    
    
    


def recommendBook(myBook):
    
    #get from input
    model = pickle.load(open('flask_app/model.pkl', 'rb'))
    bookList = pickle.load(open('flask_app/bookList.pkl', 'rb'))
    
    #this is the modeling step; different from Mischa's.
    #ok it does not like similar
    similar = model.similar_items(5039, 10) #inputting number rather than var does not throw error
    books = []
    scores = []
    str = "{} <br>"
#  
#    # Print the names of our most similar books
    for item in similar:
#        
        idx, score = item
        books.append(bookList.iloc[idx,0])
#        books.append(str.format(bookList.iloc[idx, 0]))
#        books.append(idx)
        scores.append(score)
        
#    recommendations = pd.DataFrame({'Book': books, 'Score': scores})
    recommendations = books   

    
    return (recommendations)
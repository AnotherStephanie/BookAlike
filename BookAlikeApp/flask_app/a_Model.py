import pickle
import pandas as pd
import numpy as np
import implicit




#def getUserIndex (gruser_id):
#    userIndices = pickle.load(open('flask_app/userIndices.pkl', 'rb'))
#    myUserIndex=userIndices[userIndices["user_id_gr"]==gruser_id].index
#    return myUserIndex

def getTitle (myBook):
    bookList = pickle.load(open('flask_app/bookList.pkl', 'rb'))
    myRow = bookList[bookList["book_id"]==int(myBook)]
    myTitle = myRow["title"].iloc[0]
    
    
    return (myTitle)


def getReviews(myID, myBook='11870085'):
    
    #get from input
    model = pickle.load(open('flask_app/model.pkl', 'rb'))
    bookList = pickle.load(open('flask_app/bookList.pkl', 'rb'))
    userIndices = pickle.load(open('flask_app/userIndices.pkl', 'rb'))
    dfRev = pickle.load(open('flask_app/dfRev.pkl', 'rb'))#just coded reviews
    
    #First, convert userID to model index
    #userIndices=userIndices.reset_index()
    myUserIndex=userIndices[userIndices['user_id_gr']==int(myID)].index#gets 3 but can't pass
    #myUserIndex = myUserIndex[0]#gets it out of index object format, just an integer
    
    #now get ranked list of similar users, as a data frame
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
    topReviews = dfSU[["rating", "review_text"]].dropna()
    topReviews = topReviews.head(3)
    
    #return ([topReviews["rating"].iloc[0], topReviews["review_text"].iloc[0], 
    #         topReviews["rating"].iloc[1], topReviews["review_text"].iloc[1],
    #          topReviews["rating"].iloc[2], topReviews["review_text"].iloc[2]])
    return (topReviews["rating"].tolist(), topReviews["review_text"].tolist() )

    
    
    


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
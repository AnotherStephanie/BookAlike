"""
The product is to build a model to allow users to take a photo of isbn of their children's book and determine a good price to set it at. Would be great to also take into account book quality and user preference for how quickly book should be sold to sell it. Maybe just give them a range of prices? Of low to high effort?

Training data is to start with a list of children's books from goodreads. Then take the isbn for each of those books and get range of used book prices.

Then build a feature list of book attributes to create a model that predicts book price.


"""
# get list of books for dataset
def book_list():
    """
    Access goodreads listopia list of children's books and get all the associated tags and features
    """
    return list

# Access lowest used book price from Amazon
def get_used_price(isbn):

    """
    https://stackoverflow.com/questions/37638066/getting-lowest-used-price-with-amazon-api

    price_response = amazon.ItemLookup(ItemId=isbn, IdType="ISBN", SearchIndex="Books", MerchantID="All", ResponseGroup="Small,OfferSummary")
    desc_soup = BeautifulSoup(price_response) book_price = desc_soup.lowestusedprice.amount.get_text()
    """
    return ()

# Access lowes new used book price from amazon
def get_new_price(isbn):
    """
    This could be useful for sanity check and find weird outliers
    """

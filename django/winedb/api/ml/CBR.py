import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class CBR:
    def __init__(self,represented_items,features,id):

        # Save represented items DataFrame and id for later use
        self.represented_items = represented_items
        self.id = id

        # Create a similiarity matrix
        similarity = pd.DataFrame(cosine_similarity(represented_items[features]))

        # append the wine id
        similarity[id] = represented_items[id]

        self.similarity = similarity

    def predict(self,wine_id):
        # Given a wine return a DataFrame with all the wines ID containing a score of similarity to the given one

        wine_index = self.represented_items[self.represented_items[self.id] == wine_id].index.values[0]
        
        cosine_similarity_df =  self.similarity[[wine_index,self.id]].sort_values(by=wine_index,ascending=False).set_index(self.id) # calculate the scores
        cosine_similarity_df = cosine_similarity_df.rename(columns = {cosine_similarity_df.columns[0]:"CS"}) # rename pandas column
        
        return cosine_similarity_df.iloc[1: , :] # The first row is the wine_id

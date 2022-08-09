import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


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

class CBRDO:
    def __init__(self,represented_items,features):

         self.represented_items = represented_items
         self.features = features
         self.all_wine_data = represented_items[features]
    
    def predict(self,desired_features):

        # Creating wine vector
        wine_vector = np.zeros(len(self.features))

        i=0
        for feature in self.features:
            if feature in desired_features: 
                wine_vector[i] = 1
            
            i += 1

        
        # Calculating cosine similarity
        num_similarity_vector = self.all_wine_data.values @ wine_vector.T
        den_similarity_vector = np.sum(np.linalg.norm(self.all_wine_data.values, axis=1) * np.linalg.norm(wine_vector))
        
        similarity = num_similarity_vector  / den_similarity_vector
        
        # Construct DataFrame for returning data consistency to the front end

        most_similar_wines = pd.DataFrame(index=self.represented_items.id,data=similarity)
        most_similar_wines = most_similar_wines.rename(columns={0:"CS"})
        most_similar_wines = most_similar_wines.sort_values(by="CS",ascending=False)
        return most_similar_wines



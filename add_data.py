from main_database import main_client
import pandas as pd



def addmy_data(name_of_collection, list_of_data, embeddings, ids=None, metadatas=None):
    try:
       collection = main_client.get_collection(name=name_of_collection)
    except ValueError:
        collection = main_client.create_collection(name=name_of_collection)


    collection.add(documents=list_of_data, ids=None, metadatas=None, embeddings=embeddings)
# will save the embeddings to the folder alreadyembedded because I keep losing this data
    the_df = pd.DataFrame({'elements': list_of_data, 'embeddings': embeddings})
    the_df.to_csv('alreadyembbeded', index=False)

    return collection





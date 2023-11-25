from main_database import main_client
import chromadb
from embedd import bert_vector_maker

from add_data import addmy_data

query_text = input('Input something for the database to use similarity search to find: ')

query_embed = bert_vector_maker(query_text)

collection_name = 'maincollection'

how_many_results = 3
try:
    thecollection = main_client.get_collection(collection_name)

    results = main_client.thecollection.query(query_embeddings=query_embed, n_results=how_many_results)
except ValueError:
    print('The collection does not exists yet?? well it should you shouldnt be seeing this error unless our database has no data in it at all :/')

from transformers import BertTokenizer, BertModel
import torch

def bert_vector_maker(text):
  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
  model = BertModel.from_pretrained('bert-base-uncased')


  input_ids = tokenizer.encode(text, return_tensors='pt')

  with torch.no_grad():
      outputs = model(input_ids)

  vector = outputs.last_hidden_state[:, 0, :].squeeze().numpy()

  return vector


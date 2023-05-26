import pickle

model_file = 'similarity_full_features.pkl'

with open(model_file, 'rb') as f:
    model_object = pickle.load(f)

if hasattr(model_object, 'get_similarities'):
    print('Model file loaded successfully')
else:
    print('Error loading model file')
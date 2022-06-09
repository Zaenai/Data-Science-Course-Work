# Import necessary modules
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import pandas as pd
import time 
# Loading data
print("running deep...")

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', "features", "AllFeaturesDroped.csv"))
featureData = pd.read_csv(path)

cleaned_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', "data", "BasicCleaned.csv"))
cleaned_data = pd.read_csv(cleaned_path)
cleaned_data.drop(columns = ["type"], inplace= True)
#print(featureData.head)
#print(cleaned_data.head)

merged = featureData.merge(cleaned_data, on=["id"], how="inner")
merged.drop(columns = ["id"], inplace=True)
merged.dropna(axis=0, subset=["content"], inplace=True)
merged = merged
print(merged.head)

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
start =time.time

train_sentences, test_sentences, train_labels, test_labels = train_test_split(merged["content"], merged["type"], test_size=0.2, random_state=42)
train_sentences = train_sentences.tolist()
test_sentences = test_sentences.tolist()

vocab_size = 5000
embedding_dim = 16
max_length = 1000
trunc_type = 'post'
padding_type = 'post'
oov_tok = '<OOV>'

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
print("fitting tokenizer")
tokenizer.fit_on_texts(train_sentences)
word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(train_sentences)
training_padded = pad_sequences(training_sequences, maxlen=max_length, padding=padding_type)
print("training padded type: ", type(training_padded))

testing_sequences = tokenizer.texts_to_sequences(test_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=1000))
model.add(tf.keras.layers.Bidirectional(
    tf.keras.layers.LSTM(300, dropout=0.3, recurrent_dropout=0.3)
))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

model.summary()

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

cb = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2)
data_model = model.fit(training_padded, train_labels, epochs=50, validation_data=(testing_padded, test_labels), callbacks=[cb])

print("took: ",time.time-start)

plot1 = plt.figure(1)
plt.plot(data_model.history['loss'])
plt.title('Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')

plot2 = plt.figure(2)
plt.plot(data_model.history['val_loss'])
plt.title('Val Loss')
plt.xlabel('Epochs')
plt.ylabel('Val Loss')

plot3 = plt.figure(3)
plt.plot(data_model.history['accuracy'])
plt.title('Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Acuracy')

plot4 = plt.figure(4)
plt.plot(data_model.history['val_accuracy'])
plt.title('Val Acurracy')
plt.xlabel('Epochs')
plt.ylabel('Val Accuracy')
plt.show()
import sqlite3
import os

db_path = 'DataBase/knowledgeBase.db'

# Check if the directory exists, create it if not
directory = os.path.dirname(db_path)
if not os.path.exists(directory):
    os.makedirs(directory)

# Now, connect to the database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Define your word and value pairs (you can replace these with your actual data)
word_value_pairs = [
    ('good', 1),
    ('bad', -1),
    ('tasty', 1),
    ('hate', -1),
    # Add more word-value pairs as needed
]

# Create a table to store word values if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS wordVals
             (word TEXT, value INTEGER)''')

# Insert word-value pairs into the database
for word, value in word_value_pairs:
    c.execute("INSERT INTO wordVals (word, value) VALUES (?, ?)", (word, value))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

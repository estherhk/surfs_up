#!/usr/bin/env python
# coding: utf-8

# In[1]:




# In[2]:


from flask import Flask


# In[3]:


#create new flask app instance
app = Flask(__name__)


# In[4]:
@app.route('/')
def hello_world():
	return 'Hello world'

@app.route('/motivational')
def skill_two():
    return 'I Can Do This'


# In[5]:




# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[18]:


import requests as r


# In[19]:


url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)


# In[20]:


# conferir status da url
resp.status_code


# In[21]:


dados_brutos = resp.json()
dados_brutos[0]


# In[22]:


dados = []
for i in dados_brutos:
    dados.append([i['Confirmed'], i['Deaths'], i['Recovered'], i['Active'], i['Date']])
dados.insert(0, ['Confirmados', 'Obitos', 'Recuperados', 'Ativos', 'Data'])

Confirmados = 0
Obitos = 1
Recuperados = 2
Ativos = 3
Data = 4


# In[23]:


for i in range(1, len(dados)):
    dados[i][Data] = dados[i][Data][:10]


# In[24]:


import datetime as dt


# In[25]:


import csv
with open('brasil-covid19.csv', 'w') as arq:
    writer = csv.writer(arq)
    writer.writerows(dados)
    
for i in range(1, len(dados)):
    dados[i][Data] = dt.datetime.strptime(dados[i][Data], '%Y-%m-%d') # strptime: str para time


# In[26]:


# funções para manipular dados e formatar gráfico
def get_datasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label':labels[i],
                'data':y[i]
            })
        return datasets
    else:
        return [
            {
                'label':labels[0],
                'data':y
            }
        ]

def set_title(title:''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return {
        'title':title,
        'display':display
    }

def create_chart(x, y, labels, kind='bar', title=''):
    
    datasets = get_datasets(y, labels)
    options = set_title(title)
    
    chart = {
        'type': kind,
        'data': {
            'labels': x,
            'datasets': datasets
        },
        'options': options
    }
    
    return chart

def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content

def save_image(path, content):
    with open(path, 'wb') as image: # wb = binário
        image.write(content)
        


# In[27]:


from PIL import Image
from IPython.display import display

def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)


# In[32]:


# estipular dados a serem usados no gráfico

y_data_1 = []
for i in dados[1::30]:
    y_data_1.append(i[Confirmados])

y_data_2 = []
for i in dados[1::30]:
    y_data_2.append(i[Recuperados])
    
labels = ['Confirmados', 'Recuperados']

x = []
for i in dados[1::30]:
    x.append(i[Data].strftime('%d/%m/%Y'))
    
chart = create_chart(x, [y_data_1, y_data_2], labels)
chart_content = get_api_chart(chart)
save_image('covid_br_grafico_cxr.png', chart_content)
display_image('covid_br_grafico_cxr.png')


# In[30]:


y_data_1 = []
for i in dados[1::30]:
    y_data_1.append(i[Obitos])
    
labels = ['Total de Obitos']

x = []
for i in dados[1::30]:
    x.append(i[Data].strftime('%d/%m/%Y'))
    
chart = create_chart(x, [y_data_1], labels)
chart_content = get_api_chart(chart)
save_image('covid_br_grafico_o.png', chart_content)
display_image('covid_br_grafico_o.png')


# In[ ]:





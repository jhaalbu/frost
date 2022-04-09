#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import frost2df # for frost.help
from frost2df import frost2df, obs2df, lightning2df, codetable


# # Observasjonsdata

# In[ ]:


# station metadata
frost2df('sources', {'name': '*haukeliseter*'})


# In[ ]:


frost2df('sources', {'county': 'Vestland'})


# In[ ]:


frost2df('sources', {'municipality': 'Kvam'})


# In[ ]:


# timeseries metadata
frost2df('observations/availableTimeSeries', {'sources': 'SN33951,SN33950'})


# In[ ]:


# observations - simple table
parameters = {
    'sources': 'SN90450',
    'elements': 'sum(precipitation_amount P1D)',
    'timeoffsets': 'PT6H',
    'referencetime': '2018-03-09/2018-05-17',
}
obs2df(parameters=parameters)


# In[ ]:


# observations - recurring
parameters = {
    'sources': 'SN18700',
    'elements': 'mean(air_temperature P1D)',
    'timeoffsets': 'PT0H',
    'referencetime': 'R5/2010-12-28/2011-01-04/P1Y',
}
obs2df(parameters=parameters, verbose=True)


# In[ ]:


# observations - simple toplist
parameters = {
    'sources': 'SN90450',
    'elements': 'sum(precipitation_amount P1D)',
    'timeoffsets': 'PT6H',
    'referencetime': '2018-03-09/2018-05-17',
}
df=frost2df('observations', parameters)
fav_cols = ['sourceId','elementId','referenceTime','value','unit','qualityCode','timeOffset','timeResolution']
df[fav_cols].nlargest(columns='value', n=5)


# In[ ]:


# county records
frost2df('records/countyExtremes', {'counties': 'Oslo'})


# # Elementer

# In[ ]:


# element metadata
frost2df('elements', {'ids': 'over_time(precipitation_type_automatic P1D)'}).T


# In[ ]:


# kodetabell (id, element_id, oldcode)
codetable(oldcode='SLAGWA')


# # IVF-data

# In[ ]:


# IDF data
parameters = {
    'sources': 'SN18701',
    'unit': 'mm',
    'fields': 'values'
}
frost2df('frequencies/rainfall', parameters).T


# In[ ]:


# available IDF series
frost2df('frequencies/rainfall/availableSources')


# # Lyndata

# In[ ]:


# for polygon box, use: https://boundingbox.klokantech.com/
# both functions fail when no data
# can only fetch one day at a time now, which is kind of useless
parameters = {
    'referencetime': '2020-01-24/2020-01-25',
    'geometry': 'POLYGON((8.229474 63.530051, 9.122113 63.530051, 9.122113 63.265625, 8.229474 63.265625, 8.229474 63.530051))'
}
lightning2df(parameters)


# # Klimanormaler

# In[ ]:


# climate normals
parameters = {
    'sources': 'SN36710',
    'elements': 'mean(air_temperature P1Y),sum(precipitation_amount P1Y)',
    'period': '1961/1990'
}
frost2df('climatenormals', parameters)


# In[ ]:


# available climate normals
frost2df('climatenormals/available', {'sources': 'SN36710'})


# # Kvalitetsinfo

# In[ ]:


# quality code table
frost2df('observations/availableQualityCodes')


# In[ ]:


# detailed 5-digit quality code description
frost2df('observations/quality', {'flags':'99999'})


# # Help info

# In[ ]:


params, responses = frost.help('observations')
params
#responses


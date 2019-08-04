def remove_invalid(df):
    '''
    Removes records that have invalid descriptions from the dataframe
    Input: dataframe
    Output: Cleaned up dataframe
    '''
    invalid_desc_idxs=[]
    for i in df.index:
        try:
            a=detect(df.at[i,'book_desc'])
        except:
            invalid_desc_idxs.append(i)
    
    df=df.drop(index=invalid_desc_idxs)
    return df

book_data_train=remove_invalid(book_data_train)
book_data_train['lang']=book_data_train.book_desc.apply(detect)

#Downloading the list of languages to map the two-letter lang code to the language name
lang_lookup=pd.read_html('https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes')[1]
lang_lookup.drop(columns=[0], inplace=True)
lang_lookup.columns=lang_lookup.iloc[0]
lang_lookup=lang_lookup.reindex(lang_lookup.index.drop(0))
lang_lookup.rename(columns={'639-1': 'lang'}, inplace=True)

def get_language(lang):
    if lang in list(lang_lookup['lang']):
        return lang_lookup[lang_lookup['lang']==lang]['ISO language name'].values[0]
    else:
        return 'N/A'

book_data_train['language']=book_data_train['lang'].apply(get_language)
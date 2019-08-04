def genre_binarizer(genres):
    '''
    Analyzes the genres string passed as argument to check if fiction or nonfiction is present and returns a genre appropriately
    Inputs: the genres column data from the book data frame
    Returns:
    - fiction, if fiction is present
    - nonfiction, if nonfiction is present
    - neither, if neither is present
    '''
    genre_list=genres.lower().split('|')
    if 'fiction' in genre_list:
        return 'fiction'
    elif 'nonfiction' in genre_list:
        return 'nonfiction'
    else:
        return 'neither'

def eng_desc(df):
    '''
    Analyzes the book description in the data frame passed, and returns a data frame with non-English records removed using the langdetect package
    Inputs: data frame
    Returns: data frame with non-English description records removed
    '''
    invalid_desc_idxs=[]
    for i in df.index:
        try:
            a=detect(df.at[i,'book_desc'])
        except:
            invalid_desc_idxs.append(i)
    
    if len(invalid_desc_idxs)>0:
        print('Removing these records as the descriptions are invalid:',invalid_desc_idxs)
    df=df.drop(index=invalid_desc_idxs)
    df['lang']=df.book_desc.apply(detect)
    df=df[df.lang=='en']
    return df

def add_space_case(desc):
    '''
    Analyzes the book description passed and inserts spaces where a lowercase letter is followed immediately by an uppercase letter.
    Inputs: book description
    Returns: Modified book description
    '''
    upd_desc=''
    
    for i in range(len(desc)-1):
        upd_desc+=desc[i]
        if desc[i] in string.ascii_lowercase and desc[i+1] in string.ascii_uppercase:
            upd_desc+=' '
    
    upd_desc+=desc[-1]
    return upd_desc  

def remove_punctuation(desc):
    '''
    Modifies the book description passed to 
    - insert spaces in place of punctuations
    - join apostrophe words to their parent words and 
    - insert spaces where lowercase is followed by uppercase
    Inputs: book description
    Returns: modified book description
    '''
    desc=add_space_case(desc)
    apostrophe_words=['m', 're', 've', 'll', 't', 's', 'd']
    
    desc=desc.lower()
        
    desc=''.join([c if c in valid_chars else ' ' for c in desc])
    
    for a in apostrophe_words:
        desc=desc.replace(' '+a+' ', a+' ')

    return desc

        
def df_cleaner(df):
    '''
    Takes in a dataframe and performs the following steps to clean up:
    - Removes records with null genres and descriptions
    - Removes records where genre is neither fiction nor nonfiction
    - Removes records where the description is non-English
    - Removes punctuations from the description
    - Resets the index
    Inputs: dataframe
    Returns: cleaned-up dataframe
    '''
    print("No. of records            :", len(df))
    
    df=df[df.genres.notnull()]
    print("After removing null genres:", len(df))
    
    df=df[df.book_desc.notnull()]
    print("After removing null descs :", len(df))
    
    df=df[df.book_desc.str.strip().apply(len)>0]
    print("After removing zero descs :", len(df))
    
    df['binary_genre']=df.genres.apply(genre_binarizer)
    df=df[df.binary_genre!='neither']
    print("Only fiction or nonfiction:", len(df))
    
    df=eng_desc(df)
    print("After removing non-English:", len(df))
    
    df['clean_desc']=df.book_desc.apply(remove_punctuation)
    
    df.reset_index(drop=True, inplace=True)
    print('---------------------------')
    return df
    
book_data_train=df_cleaner(book_data_train)
book_data_test=df_cleaner(book_data_test)

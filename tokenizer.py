vocabulary=set() #unique list of all words

def add_to_vocab(df, vocabulary):
    for i in df.clean_desc:
        for word in i.split():
            vocabulary.add(word)
    return vocabulary

vocabulary=add_to_vocab(book_data_train, vocabulary)
vocabulary=add_to_vocab(book_data_test, vocabulary)

#This dictionary represents the mapping from word to token. Using token+1 to skip 0, since 0 will be used for padding descriptions with less than 200 words
vocab_dict={word: token+1 for token, word in enumerate(list(vocabulary))}

#This dictionary represents the mapping from token to word
token_dict={token+1: word for token, word in enumerate(list(vocabulary))}

assert token_dict[1]==token_dict[vocab_dict[token_dict[1]]]

def tokenizer(desc, vocab_dict, max_desc_length):
    '''
    Function to tokenize descriptions
    Inputs:
    - desc, description
    - vocab_dict, dictionary mapping words to their corresponding tokens
    - max_desc_length, used for pre-padding the descriptions where the no. of words is less than this number
    Returns:
    List of length max_desc_length, pre-padded with zeroes if the desc length was less than max_desc_length
    '''
    a=[vocab_dict[i] if i in vocab_dict else 0 for i in desc.split()]
    b=[0] * max_desc_length
    if len(a)<max_desc_length:
        return np.asarray(b[:max_desc_length-len(a)]+a).squeeze()
    else:
        return np.asarray(a[:max_desc_length]).squeeze()

book_data_train['desc_tokens']=book_data_train['clean_desc'].apply(tokenizer, args=(vocab_dict, max_desc_length))
book_data_test['desc_tokens']=book_data_test['clean_desc'].apply(tokenizer, args=(vocab_dict, max_desc_length))
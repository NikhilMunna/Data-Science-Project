def stratified_split(df, target, val_percent=0.2):
    '''
    Function to split a dataframe into train and validation sets, while preserving the ratio of the classes in the target variable
    Inputs:
    - df, the dataframe
    - target, the target variable
    - val_percent, the percentage of validation samples, default 0.2
    Returns
    - train_idxs, the indices of the training dataset
    - val_idxs, the indices of the validation dataset
    '''
    classes=list(df[target].unique())
    train_idxs, val_idxs = [], []
    for c in classes:
        idx=list(df[df[target]==c].index)
        np.random.shuffle(idx)
        val_size=int(len(idx)*val_percent)
        val_idxs+=idx[:val_size]
        train_idxs+=idx[val_size:]
    return train_idxs, val_idxs
    
    
    _, sample_idxs = stratified_split(book_data_train, 'binary_genre', 0.1)

train_idxs, val_idxs = stratified_split(book_data_train, 'binary_genre', val_percent=0.2)
sample_train_idxs, sample_val_idxs = stratified_split(book_data_train[book_data_train.index.isin(sample_idxs)], 'binary_genre', val_percent=0.2)
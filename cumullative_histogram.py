#Calculating the no. of words in the book descriptions and storing them in a dataframe - this enables the use of cufflinks
len_df=pd.DataFrame()
desc_lengths=[len(i.split()) for i in book_data_train.clean_desc] + [len(i.split()) for i in book_data_test.clean_desc]
len_df['desc_lengths']=desc_lengths

cf.go_offline()

#This function needs to be called to draw Plotly charts in Colab
configure_plotly_browser_state()


#Binning the lengths (no. of words) and calculating a cumsum to figure the 80% mark
len_df_bins=len_df.desc_lengths.value_counts(bins=100, normalize=True).reset_index().sort_values(by=['index'])
len_df_bins['cumulative']=len_df_bins.desc_lengths.cumsum()
len_df_bins['index']=len_df_bins['index'].astype('str')
len_df_bins.iplot(kind='bar', x='index', y='cumulative')
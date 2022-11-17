from config import *
import psycopg2
import pandas as pd

conn=psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password)

channel_data = pd.read_sql_query('select * from channel_data',con=conn)
# video_data = pd.read_sql_query('select * from video_data',con=conn)
joined_data = pd.read_sql_query('select * from joined_data',con=conn)
binned_data = pd.read_sql_query('select * from clean_binned_data',con=conn)
mega_df = pd.read_sql_query('select * from new_binned_df',con=conn)

category_data = channel_data.groupby('topic_category').sum().reset_index()
sentiment_data = pd.read_csv('Database/ready_for_sql/sentiment_data.csv')
new_length = pd.read_csv('Database/ready_for_sql/video_data_fixed_length.csv')
# join sentiment data videos_data
video_sentiment_data = joined_data.merge(sentiment_data, on='video_id', how='left')

binned_data2 = binned_data.merge(new_length, on='video_id', how='left')

category_data_new = binned_data2.groupby('topic_category').sum().reset_index()
# add the average length_new to the category_data_new
category_data_new['avg_length'] = binned_data2.groupby('topic_category').mean()['new_length'].reset_index()['new_length']

channel_data2 = binned_data2.groupby('channel_id_x').mean().reset_index()
channel_data2 = channel_data2.merge(binned_data2[['channel_id_x', 'custom_url']], on='channel_id_x', how='left')

mega_df2 = mega_df.merge(sentiment_data, on='video_id', how='left')

mega_df3 = mega_df2.groupby('channel_id_x').agg({'subscriber_count': 'mean', 'view_count': 'mean','comment_count': 'mean', 'sentiment': 'mean', 'video_length_seconds': 'mean', 'topic_category': 'first', 'custom_url': 'first'}).reset_index()

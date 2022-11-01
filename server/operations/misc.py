import os

import pandas as pd

from db.database import db_session
from operations.core import remove_links_emojis


def db_to_excel(departmentTable, file: str, sheet_name: str = None,
                original: bool = False) -> None:
    """
    Reads rows from a database table and writes the result to a csv file
    """
    if sheet_name is None:
        sheet_name = 'Sheet1'

    tweet_df = pd.DataFrame()
    
    with db_session() as session:
        rows = session.query(departmentTable).where(
            departmentTable.location != None).limit(100)

    tweet_df['id'] = [row.id for row in rows]
    if original:
        tweet_df['text'] = [row.text for row in rows]
    else:
        tweet_df['text'] = [remove_links_emojis(row.text) for row in rows]
    
    tweet_df['created_at'] = [row.created_at for row in rows]

    mode = 'a' if os.path.exists(file+'.xlsx') else 'w'

    writer = pd.ExcelWriter(file+'.xlsx', mode=mode)
    tweet_df.to_excel(writer, sheet_name)
    writer.save()
    
    
    print('debug point')

    
        
    
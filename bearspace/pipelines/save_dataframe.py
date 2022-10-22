from datetime import datetime
from uuid import uuid4

import pandas as pd


class SaveInDataframe:
    def __init__(self):
        self.items: list[dict] = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        with open(f"bearspace/output/{uuid4()}_{datetime.now()}", "w") as f:
            dfAsString = df.to_string(header=False, index=False)
            f.write(dfAsString)
        f.close()

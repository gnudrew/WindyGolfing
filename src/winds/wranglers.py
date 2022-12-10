import os
import pandas as pd

from django.conf import settings

class BlobWrangler():
    """Interface between the ORM and Blob storage"""

    staging_path = os.path.join(settings.BASE_DIR, '.blob_storage')

    def read_blob(self, obj):
        """Given a model object, return the associated DataFrame"""
        filename = obj.blob_filename
        filepath = os.path.join(self.staging_path, filename)
        return pd.read_feather(filepath,)

    def write_blob(self, df, Model, params):
        """Given a DataFrame and Model, convert and write the DataFrame to blob storage, creating a new Model entry along the way."""
        # model object
        obj = Model(**params)
        # save blob
        filename = obj.id__str__() + '.fthr' # feather file
        filepath = os.path.join(self.staging_path, filename)
        df.to_feather(filepath)
        # save obj after blob saves
        obj.save()
        return obj
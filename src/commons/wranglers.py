import os
import pandas as pd

from django.conf import settings

class BlobWrangler():
    """Interface between the ORM and Blob storage"""

    staging_path = os.path.join(settings.BASE_DIR, '.blob_storage')

    def read_blob(self, obj):
        """Given a model object, load and return the associated DataFrame"""
        filename = obj.blob_filename
        filepath = os.path.join(self.staging_path, filename)
        return pd.read_feather(filepath,)

    def write_blob(self, df, Model, model_params):
        """
        Given a DataFrame, Model class, and model instance parameters, convert and write the DataFrame to blob storage, creating a new Model entry along the way and returning it.
        
        Parameters:
        -------
        df: pd.DataFrame
            The dataset destined for blob storage.
        Model: class
            The model class representing a table in the RDB.
        model_params: dict
            The parameters used to create and save a model instance to the table.

        Returns:
        -------
        obj: Model instance
            The object for the table entry just created.

        """
        # model object
        obj = Model(**model_params)
        # save blob
        ## assume Model's primary key is a uuid object
        filename = obj.id.__str__() + '.fthr' # feather file
        filepath = os.path.join(self.staging_path, filename)
        df.to_feather(filepath)
        # add blob_filename and save obj (after blob successfully stored)
        obj.blob_filename = filename
        obj.save()
        return obj

    def delete_blob(self, obj):
        """Given a model object, delete the associated blob file"""
        filename = obj.blob_filename
        filepath = os.path.join(self.staging_path, filename)
        os.remove(filepath)
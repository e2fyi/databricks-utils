"""
Utility classes to interface with AWS for databricks notebooks.

.. moduleauthor:: eterna2@hotmail.com
"""
import os

class S3Bucket(object):
    """
    Class to wrap around a S3 bucket and mount at databricks fs.
    """
    dbutils = None
    def __init__(self, bucketname, aws_access_key, aws_secret_key, dbutils=None):
        """
        :param bucketname: name of the S3 bucket
        :param aws_access_key: AWS access key
        :param aws_secret_key: AWS secret key
        :param dbutils: databricks `dbutils` (not needed if `S3Bucket.attach_dbutils` has been called)
        """
        self.name = bucketname
        self.mount_at = None
        self._aws_access_key = aws_access_key
        self._aws_secret_key = aws_secret_key
        self._aws_encoded_secret_key = aws_secret_key.replace("/", "%2F")
        if dbutils:
            self.dbutils = dbutils

    @classmethod
    def attach_dbutils(cls, dbutils):
        """
        Attach databricks `dbutils` to S3Bucket. You MUST attach this before
        S3Bucket can be used.

        :param dbutils: databricks `dbutils` (https://docs.databricks.com/user-guide/dev-tools/dbutils.html#dbutils)
        """
        cls.dbutils = dbutils

    def allow_spark(self, spark_context):
        """
        Update spark context hadoop config with AWS access information so that
        databricks spark can access the S3 bucket.

        :param spark_context: databricks spark context
        """
        # pylint: disable=undefined-variable, protected-access
        spark_context._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId",
                                                     self._aws_access_key)
        # pylint: disable=undefined-variable
        spark_context._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey",
                                                     self._aws_secret_key)
        return self

    def mount(self, mount_pt, dbutils=None):
        """
        Mounts the S3 bucket in dbfs.
        environment variables `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` must be set.

        :param mount_pt: Where to mount the S3 bucket in the `dbfs`.
        :param display: Callable to display
        :param dbutils: `dbutils` module
        """
        self.mount_at = os.path.join("/mnt", mount_pt)
        bucket_uri = "s3a://{0}:{1}@{2}".format(self._aws_access_key,
                                                self._aws_encoded_secret_key,
                                                self.name)
        if dbutils:
            self.dbutils = dbutils

        if self.dbutils is None:
            raise RuntimeError("`dbutils` not provided. Please call " +
                               "`S3Bucket.attach_dbutils` or provide " +
                               "`dbutils` in the arguments.")

        try:
            self.dbutils.fs.mount(bucket_uri, self.mount_at)
        except Exception as error: # pylint: disable=broad-except
            if "Directory already mounted" not in str(error):
                raise error
        return self

    def umount(self, dbutils):
        """umount the s3 bucket."""

        if dbutils:
            self.dbutils = dbutils

        if self.dbutils is None:
            raise RuntimeError("`dbutils` not provided. Please call " +
                               "`S3Bucket.attach_dbutils` or provide " +
                               "`dbutils` in the arguments.")

        self.dbutils.fs.unmount(self.mount_at) # pylint: disable=undefined-variable
        return self

    def s3(self, path): # pylint: disable=invalid-name
        """
        Return the path to the corresponding resource in the s3 bucket that is
        interpretable by the databricks spark worker.

        :param path: relative path to a resource in the s3 bucket.
        """
        return os.path.join("s3a://", self.name, path)

    def local(self, path):
        """
        Return the absolute path to the corresponding resource in dbfs.

        :param path: relative path to a resource in the s3 bucket.
        """
        return os.path.join("/dbfs", self.mount_at[1:], path)

    def ls(self, path="", display=None): # pylint: disable=invalid-name
        """
        List the files and folders in s3 bucket mounted in `dbfs`.

        :param path: path relative to the s3 bucket
        :param display: a Callable to render the HTML output. e.g. `displayHTML`
        """
        # pylint: disable=undefined-variable
        files = self.dbutils.fs.ls(os.path.join("dbfs:/", self.mount_at[1:], path))
        if callable(display):
            frag = ""
            for file in files:
                classname = "file" if file.size > 0 else "folder"
                frag += """
                <tr class='{0}'>
                    <td>{1}</td>
                    <td>{2}</td>
                </tr>""".format(classname, file.name, file.size)

            display("""
            <style>
                section {color: #666; font-family: sans-serif; font-size: 11px;}
                .folder {color: #1976d2; font-weight: bold;}
                .file {color: #00897b;}
            </style>
            <section>
                <big>"""+path+"""</big>
                <table>
                  <tr><th>name</th><th>size</th></tr>
                  """+frag+"""
                </table>
            </section>
            """)
        return files

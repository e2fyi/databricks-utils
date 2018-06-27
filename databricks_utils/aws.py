"""
Utility classes to interface with AWS for databricks notebooks.

.. moduleauthor:: eterna2@hotmail.com
"""
import databricks_utils


class S3Bucket(object):
    """
    Class to wrap around a S3 bucket and mount at databricks fs.
    This class is only usable for databricks notebooks.
    """
    def __init__(self, bucketname, aws_access_key, aws_secret_key):
        """
        :param bucketname: name of the S3 bucket
        :param aws_access_key: AWS access key
        :param aws_secret_key: AWS secret key
        """
        self.name = bucketname
        self.mount_at = None
        self._aws_access_key = aws_access_key
        self._aws_secret_key = aws_secret_key
        self._aws_encoded_secret_key = aws_secret_key.replace("/", "%2F")

    def allow_spark(self):
        """
        Update spark context hadoop config with AWS access information so that
        databricks spark can access the S3 bucket.
        """
        # pylint: disable=undefined-variable, protected-access
        sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId",
                                          self._aws_access_key)
        # pylint: disable=undefined-variable
        sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey",
                                          self._aws_secret_key)
        return self

    def mount(self, mount_pt):
        """
        Mounts the S3 bucket in dbfs.
        environment variables `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` must be set.

        :param mount_pt: Where to mount the S3 bucket in the `dbfs`.
        """
        self.mount_at = "/mnt/{0}".format(mount_pt)
        try:
            # pylint: disable=undefined-variable
            dbutils.fs.mount("s3a://%s:%s@%s" % (self._aws_access_key,
                                                 self._aws_encoded_secret_key,
                                                 self.name), self.mount_at)
            display(dbutils.fs.ls("/mnt/%s" % mount_pt))
        except Exception as error: # pylint: disable=broad-except
            if "Directory already mounted" not in str(error):
                raise error
        return self

    def umount(self):
        """umount the s3 bucket."""
        dbutils.fs.unmount(self.mount_at) # pylint: disable=undefined-variable
        return self

    def s3(self, path): # pylint: disable=invalid-name
        """
        Return the path to the corresponding resource in the s3 bucket that is
        interpretable by the databricks spark worker.

        :param path: relative path to a resource in the s3 bucket.
        """
        return "s3a://" + self.name + "/" + path

    def local(self, path):
        """
        Return the absolute path to the corresponding resource in dbfs.

        :param path: relative path to a resource in the s3 bucket.
        """
        return "/dbfs/{0}/{1}".format(self.mount_at, path)

    def ls(self, path): # pylint: disable=invalid-name
        """
        List the files and folders in s3 bucket mounted in `dbfs`.

        :param path: path relative to the s3 bucket
        """
        # pylint: disable=undefined-variable
        files = dbutils.fs.ls(self.local(path))
        html = ""
        for file in files:
            classname = "file" if file.size > 0 else "folder"
            html += """
            <tr class='{0}'>
                <td>{1}</td>
                <td>{2}</td>
            </tr>""".format(classname, file.name, file.size)

        databricks_utils.displayHTML("""
        <style>
            section {color: #666; font-family: sans-serif; font-size: 11px;}
            .folder {color: #1976d2; font-weight: bold;}
            .file {color: #00897b;}
        </style>
        <section>
            <big>"""+path+"""</big>
            <table>
              <tr><th>name</th><th>size</th></tr>
              """+html+"""
            </table>
        </section>
        """)
        return files

# databricks-utils
[![Python version](https://img.shields.io/badge/python-3.6-blue.svg)](https://shields.io/)
[![Pyspark version](https://img.shields.io/badge/pyspark-2.3.1-blue.svg)](https://shields.io/)
[![Build Status](https://travis-ci.org/e2fyi/databricks-utils.svg?branch=master)](https://travis-ci.org/e2fyi/databricks-utils)

`databricks-utils` is a python package that provide several utility classes/func
that improve ease-of-use in databricks notebook.

### Installation
```bash
pip install databricks-utils
```

### Features
- `S3Bucket` class to easily interact with a [S3 bucket](https://aws.amazon.com/s3/) via [`dbfs`](https://docs.databricks.com/user-guide/dbfs-databricks-file-system.html) and databricks spark.

- `vega_embed` to render charts from [Vega](https://vega.github.io/vega/) and [Vega-Lite](https://vega.github.io/vega-lite/) specifications.

### Documentation
API documentation can be found at [https://e2fyi.github.io/databricks-utils/](https://e2fyi.github.io/databricks-utils/).


### Quick start
**S3Bucket**  
```python
import json
from databricks_utils.aws import S3Bucket

# need to attach notebook's dbutils
# before S3Bucket can be used
S3Bucket.attach_dbutils(dbutils)

# create an instance of the s3 bucket
bucket = (S3Bucket("somebucketname", "SOMEACCESSKEY", "SOMESECRETKEY")
          .allow_spark(sc) # local spark context
          .mount("somebucketname")) # mount location name (resolves as `/mnt/somebucketname`)

# show list of files/folders in the bucket "resource" folder
bucket.ls("resource/")

# read in a json file from the bucket
data = json.load(open(bucket.local("resource/somefile.json", "r")))

# read from parquet via spark
dataframe = spark.read.parquet(bucket.s3("resource/somedf.parquet"))

# umount
bucket.umount()
```

**Vega**  
[Vega](https://vega.github.io/vega/) and [Vega-Lite](https://vega.github.io/vega-lite/)
are high-level grammars of interactive graphics. They provide concise JSON
syntax for rapidly generating visualizations to support analysis.

```python
from databricks_utils.vega import vega_embed

# vega-lite spec for a bar chart
spec = {
  "data": {
    "values": [
      {"a": "A","b": 28}, {"a": "B","b": 55}, {"a": "C","b": 43},
      {"a": "D","b": 91}, {"a": "E","b": 81}, {"a": "F","b": 53},
      {"a": "G","b": 19}, {"a": "H","b": 87}, {"a": "I","b": 52}
    ]
  },
  "mark": "bar",
  "encoding": {
    "x": {"field": "a", "type": "ordinal"},
    "y": {"field": "b", "type": "quantitative"}
  }
}

# plot out the vega chart in databricks notebook
displayHTML(vega_embed(spec=spec))
```

### Developer
```bash
# add a version to git tag and publish to pypi
. add_tag.sh <VERSION>
```

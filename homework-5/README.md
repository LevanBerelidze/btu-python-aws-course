# Homework 5

## Steps

-   `create_bucket.py` - Creates a S3 Bucket with specified name.

-   `create_lambda.py` - Creates a Lambda Function with specified name.

-   `configure_trigger` - Grants S3 Bucket the permission to invoke a Lambda Function and creates a trigger which invokes a Lambda when a _.jpeg_ file is uploaded to the bucket.

In order to do all of the above at once run `main.py` script.

`demo.py` script uploads an image to the bucket and then prints the resulting JSON file to the console.

<small>To see the argument list of the scripts run: `py script_name.py --help`</small>

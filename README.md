# fhir-template-creator
The script in this repository aims to facilitate the creation of jinja2 templates from FHIR profile examples.

## How to use
First you will need to download the example json files from simplifier.net. For ZIB, these can be found on the 
[ZIB FHIR profile page](https://simplifier.net/packages/nictiz.fhir.nl.stu3.zib2017/2.0.6/~introduction).
You will need to extract the files into a folder.

Next, you will call `create_templates.py`, specifying the json examples folder as command-line argument as follows:

```shell
./create_templates.py my/path/to/examples
```

If you don't specify the path to the examples directory the script will assume it is located in the current working 
directory and named *examples* .
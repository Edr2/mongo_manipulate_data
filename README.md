# mongo_manipulate_data
Some tools to manipulate mongo data


python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  

docker-compose up -d mongo  

```
python main.py --help  
Usage: main.py [OPTIONS] COMMAND [ARGS]...  

Options:  
  --help  Show this message and exit.  

Commands:  
  clearfield  
  exportdb  
  initdb  
  removefield  
  sortjson  
  upperfield  
```

python main.py initdb  
python main.py exportdb  

python main.py removefield  
python main.py upperfield  
python main.py clearfield #(better name: emptyfield)  
python main.py sortjson  


docker-compose up -d nginx  
http://localhost/data.json  

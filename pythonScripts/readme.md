# Source Code
## Web Mining
### Getting the query from user and searching on imdb
```
query = Season_split[list_Season].rstrip().lstrip().lower()
                message = message+"Tv series name: "+query+"\n"
                # print "Tv series name: "+query
data= {
  'q': query,
  's': 'tt'
}
r = requests.get('https://www.imdb.com/find/', params=data)

```

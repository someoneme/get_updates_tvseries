# Source Code
## Web Mining
### Getting the query from user and searching on imdb
```Python
query = Season_split[list_Season].rstrip().lstrip().lower()
data= {
  'q': query,
  's': 'tt'
}
r = requests.get('https://www.imdb.com/find/', params=data)

```

# Flask-Wiki
## Install
```
git clone git@github.com:zavatskiy/flask-wiki.git
cd flask-wiki/
make init
make run
```

## Methods
### Add new wiki page
```python
request.post('/api/wiki_page', data={"title":"test", "text":"test_text"})
```
### Add new wiki page version
```python
request.post('/api/wiki_page_version', data={"title":"test", "text":"test_text", "wiki_page_id": <int:wiki_page_id>})
```
### Change wiki page status
```python
request.patch('/api/wiki_page_version/<int:wiki_page_version_id>', data={'status': 0})
```
### Get wiki pages list
```python
request.get('/api/wiki_page')
```
### Get wiki page versions
```python
request.get('/api/wiki_page/<int:wiki_page_id>')
```
### Get wiki page version
```python
request.get('/api/wiki_page_version/<int:wiki_page_version_id>')
```
### Get wiki page current
```python
request.get('/api/wiki_page_version?q={"filters":[{"name":"wiki_page_id","op": "eq","val": <int:wiki_page_id>},{"name":"status","op":"eq","val":1}]} ')
```
В принципе, урл можно сделать красивым, если будет поставлена соответсвующая задача...

## Test
```
make create_test_db
make test
```

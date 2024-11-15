 # Main Commands

 ```python
 # to generate .dot model
 python manage.py graph_models -a -o output.dot
 # testing
 coverage run --source='.' manage.py test
 coverage report
 coverage html
 # migrations
 python manage.py makemigrations <app_name> 
 python manage.py migrate
```

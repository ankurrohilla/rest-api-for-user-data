# rest-api-for-user-data
Rest Api for managing user’s data using Django and DRF

* For setup:

    $ git clone https://github.com/ankurrohilla/rest-api-for-user-data.git
    
    $ cd rest-api-for-user-data/
    


* With Docker
    

    $ docker-compose up


* without Docker 


    $ python3 -m venv env
    
    $  source env/bin/activate
    
    $  pip install -r requirements.txt
    
    $  python manage.py migrate
    
    $ python manage.py add_dummy_data
    
    $ python manage.py test
    
    $ python manage.py runserver
    

# Now you can navigate the API url path : 
 [API url](http://127.0.0.1:8000/api/users/)
 
# Also you can see demo ready heroku app :


 [Heroku App API](https://drf-api-users.herokuapp.com/api/users/)


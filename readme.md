# Better WebUntis
This Package is an add-on for the [WebUntis](https://github.com/python-webuntis/python-webuntis) package. It mainly makes it easier to use the WebUntis package.


## Quickstart
1. Download this Directory and put it in your project directory
2. Run `pip install webuntis requests pytz` to install the required libraries

1. Import the package
```python
from BetterWebUntis import WebUntis
```

2. Create a WebUntis object
```python
webuntis = Webuntis(
    username= "Your username",
    password = "Your password",
    url= "url of your schools webuntis login page",
)
```
You can set the `port` attribute if your school uses a different port. The default port is 8080.

3. Get your timetable
```python
timetable = webuntis.get_timetable(
    start_date= "2021-01-01",
    end_date= "2021-01-31",
    klasse= "Your class",
)
```

## Alternitives
### Not use Url
If you don't want to use the url you can give other atributes instead. But it might be hard to get them. 
```python
WebUntis(
    username= "Your username",
    password = "Your password",
    school= "Your school",
    server= "Your school´s server",
    port= "The Port of your school´s server. Propably 8080.",
    school_id= "Your school´s id",
)
```


## Documentation
### WebUntis
#### Attributes
| Attribute | Type | Description |
| --- | --- | --- |
| classes | list | A list of all classes |
| teachers | list | A list of all teachers |
| rooms | list | A list of all rooms |
| holidays | list | A list of all holidays |

Note: Some attributes might be empty if they are not provided.

#### Methods
- `get_timetable(klasse, start_date, end_date)`
    - `klasse`: The class of the timetable (e.g. 5a) should be a string
    - `start_date`: Datetimeobject for the start date of the timetable
    - `end_date`: Datetimeobject for the end date of the timetable
    - Returns: A list of all lessons in the given time frame
- `get_time_table_by_subjects(klasse, start_date, end_date, subjects)`
    - `klasse`: The class of the timetable (e.g. 5a) should be a string
    - `start_date`: Datetimeobject for the start date of the timetable
    - `end_date`: Datetimeobject for the end date of the timetable
    - `subjects`: A list of subject shortnames (e.g. `["PHY", "MAT"]`)
    - Returns: A list of all lessons in the given time frame

### Lesson
#### Attributes
| Attribute | Type | Description                                                                  |
|-----------| --- |------------------------------------------------------------------------------|
| start     | datetime | The start time of the lesson                                                 |
| end       | datetime | The end time of the lesson                                                   |
| name      | string | The name of the lesson                                                       |
| longname  | string | The long name of the lesson                                                  |
| rooms     | list | A list of all rooms for the lesson                                           |
| classes   | list | A list of all classes in the lesson                                          |
|state | string | The state of the lesson (e.g. "cancelled"). If None the lesson is as planed. |
| id | int | The webuntis id of the lesson.                                               |

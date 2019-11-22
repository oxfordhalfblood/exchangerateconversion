# exchangerateconversion
An application that takes messages as inputs, and based on the type of message the application needs to call different API accordingly, and finally transform and write the data to database.

# Steps to execute the program:

1. Use python3
2. ```pip install pymysql```
3. Put all your json formatted messages in msg1.json file delimited with comma
4. From terminal cd to the project folder. Run ```docker-compose up```
5. Execute rateconversion.py
6. lastmonthAUD.py backfills last month’s data for AUD currency and should be run separately as it's assumed to just fill the database once
7. Unit Testing provided on test.py and should be run with ```python3 test.py```
8. DB schema is included inside sql_dump2 folder which contains three tables



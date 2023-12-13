# Area Environmental Monitoring

## Project Description

Our project, Area Environmental Monitoring is a project designed to provide the most recent data on some of the key environmental parameters where we integrated data from multiple data source which are air quality(PM2.5) data, population density, sound levels, and light intensity in a specific location. By addressing these critical aspects, the project aims to contribute significantly to the environment, public health, and safety.

## Set up project

1. Use Python3 environment
   ```
   python3 -m venv env
   ```
2. Activate environment
   ```
   . env/bin/activate
   ```
   note. This for masOS
3. Install requirements
   ```
   pip install -r requirements.txt
   ```
4. Add file `config.py` (sample files in config.py.example)

## Run this project

- For Python API
  ```
  python app.py
  ```
- For GraphQL
  ```
  openapi-to-graphql --cors openapi/environment-api.yaml
  ```

## OPENAPI

- GET ```/latest/{param}```: Return latest average all params from all source

   <u>list of param can use</u>
   | param |
   | --- |
   |pm25|
   |wind|
   |temp|
   |hum|
   |humcount|
   |sound|

   example result
   ```
   {
      "day": 0,
      "month": 0,
      "year": 0,
      "hour": 0,
      "value": 0
   }
   ```

- GET ```/all/avg/{param}```: Return all average params from all source

   <u>list of param can use</u>
   | param |
   | --- |
   |pm25|
   |wind|
   |temp|
   |hum|
   |humcount|
   |sound|

   example result
   ```
   [
      {
         "day": 0,
         "month": 0,
         "year": 0,
         "hour": 0,
         "value": 0
      }
   ]
   ```

- GET ```/separate/{param}/{source}/hour```: Return average value of specific parameters and source

   <u>list of param and source can use</u>
   |param|source|
   |---|---|
   |pm25|apiairvisual|
   |pm25|apiwqi|
   |pm25|dustsensor|
   |wind|apiairvisual|
   |wind|apiopenweather|
   |temp|apiairvisual|
   |temp|apiopenweather|
   |temp|kidbright|
   |hum|apiairvisual|
   |hum|apiopenweather|
   |humcount|infraredsensor|
   |sound|soundsensor|

   example result
   ```
   [
      {
         "source": "string",
         "hour": 0,
         "value": 0
      }
   ]
   ```
- GET ```/compare/humcount/{param}```: Return human in the area compare with other parameters in each hours

   <u>list of param can use</u>
   | param |
   | --- |
   |pm25|
   |temp|

   example result
   ```
   [
      {
         "year": 0,
         "month": 0,
         "day": 0,
         "hour": 0,
         "humcount": 0,
         "comparevalue": 0
      }
   ]
   ```

## GraphQL

- Find latest average hour

   ```
   {
  	   averageValue(param:"param"){
         day
         month
         year
         hour
         value
      }
   }
   ```
- Find average by hour from specific parameter and source

   ```
   {
	   separateHour(param:"param" source:"source"){
         hour
         value
      }
   }
   ```

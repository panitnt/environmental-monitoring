# Area Environmental Monitoring

## Project Overview

The Area Environmental Monitoring project serves as a proof of concepts, designed to provide the most recent data on some of the key environmental parameters where we integrated data from multiple data source which are air quality(PM2.5) data, population density, sound levels, and light intensity in a specific location. By addressing these critical aspects, the project aims to contribute significantly to the environment monitoring and measuring, public health, and safety.

The idea for the Area Environmental Monitoring project started when we were making live ad hoc decision to attending events like Kasetfair, Loy Krathong Festival at Kasetsart University, Live concerts, and etc. We realized there was a lack of real-time information about environment status in these events and specific areas within them. Our motivation start from the desire to make well-informed decisions about whether to attend an event or not. Therefore, we aim to enhance user decision and the overall event experience by offering real-time insights into crucial environmental factors.

Whether you're the area owner or event organizer, our project aims to be the go-to solution for making public spaces and events safer and more enjoyable by collecting and integrating data. Moreover, sharing crucial environmental data to the public in real-time by visualizing each area environmental factor, showing correlation between population and PM2.5, and showing correlation between population and temperature in the area.


## Project overview and features
- Main page shows latest hour average values
   <img width="1437" alt="Screenshot 2566-12-14 at 12 56 17 AM" src="https://github.com/panitnt/environmental-monitoring/assets/92779345/489ca9c0-4a2b-4820-8482-7ff779563949">
- Graph page shows average values in the day by each source
   <img width="1440" alt="Screenshot 2566-12-14 at 12 56 40 AM" src="https://github.com/panitnt/environmental-monitoring/assets/92779345/c7e8ab43-d99d-4096-8fc6-3e5e1053724c">
- Compare page shows correlation between human in the area with PM2.5 and correlation between human in the area with Temperature
   <img width="1440" alt="Screenshot 2566-12-14 at 12 57 22 AM" src="https://github.com/panitnt/environmental-monitoring/assets/92779345/4d5327d8-b9ab-431f-8576-6feb375618cd">

***Because of our data not much, this graph cannot clearly tell the relationship between this😿***

## Requirements, Required libraries, and tools
All requirements are mentioned in requirements.txt file.

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
5. Copy code from `openapi/environment-api.yaml` and paste it into [python flask generator](https://editor.swagger.io/)

   - Paste the code
   - click *Generate Server*
   - click *python-flask*
   - move the folder to this project and rename to *stub*

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

   *list of param can use*
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

   *list of param and source can use*
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

   *list of param can use*
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

## Project Members

- 6410545452 Nichakorn Chanajitpairee
- 6410545592 Zion Keretho
- 6410546181 Panitta Tanyavichitkul
- 6410546246 Ratthicha Parinthip

Software and Knowledge Engineering (SKE19), Kasetsart University 
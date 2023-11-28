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

## Run this project

- For Python API
  ```
  python app.py
  ```
- For GraphQL
  ```
  openapi-to-graphql --cors openapi/environment-api.yaml
  ```

## GraphQL

- Find latest average hour

   ```
   {
  	   averageValue(param: "param"){
         day
         month
         year
         hour
         value
      }
   }
   ```
- Find latest average hour

   ```
   {
	   separateHour(param: "param"){
         source
         hour
         value
      }
   }
   ```

# Area Environmental Monitoring

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
  openapi-to-graphql openapi/environment-api.yaml
  ```

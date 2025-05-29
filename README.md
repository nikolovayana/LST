# Repository overview
`main.ipynb` --> a Jupiter notebook containing the main script, where analyses and data visualization is done 

`helpers.py` --> stores all the functions used in the notebook

`utils.py` --> contains additional utilities, such as global variables and and 'evalscipt' that defines how Sentinel Hub should process and return the data
## 🧪 Jupiter notebook main script `main.ipynb`

This notebook contains the core logic for interacting with the **Sentinel Hub Statisical API** and processing Land Surface Temperature (**LST**T) data into a DataFrame for analysis.

1. **Imports**
     - `geopandas` and `pandas` for geospatial and tabular data handling

2. **Authentication**
    The notebook prompts for secure authentication using **Sentinel Hub OAuth** credentials, enabling API access.

3. **Configuration & Variables**  
    This section defines the parameters required for running an analysis:
    - `data`: Path to a `.geojson` file containing the geographic area(s) or point(s) of interest
   - `start_date` / `end_date`: Date range for analysis in `YYYY-MM-DD` format
   - `day_interval`: Temporal resolution of the data retrieval (e.g., `1` for daily)

4. **Load Input Geometry** 
   The input GeoJSON file is read into a GeoDataFrame, which represents the spatial features with their respective geometry.

5. **Fetch Remote Data**  
   For each geometry in the input data:
   - A structured JSON request is dynamically generated
   - The request is sent to the **Sentinel Hub Statistics API**
   - The resulting LST statistics are collected into a list named `results`

6. **Build Final DataFrame**  
   - The raw JSON responses are parsed and converted into individual DataFrames
   - Each entry is paired with its corresponding `land_type` attribute from the input data
   - All DataFrames are concatenated into a single, analysis-ready dataset

## 🛠️ Functions in `helpers.py`

This module contains helper functions used to modularize the workflow and improve code readability and reusability.

- **`authenticate_sentinel_hub(client_id: str, client_secret: str)`**  
  Handles authentication with the **Sentinel Hub API**.  
  Returns an `OAuth2Session` object with the authentication token for authorized API requests.

- **`build_json_request(geometry, start_date, end_date, day_interval, data_set)`**  
  Constructs a JSON payload for querying the Sentinel Hub Statistical API.  
  Takes in:
  - `geometry`: The spatial feature to query (e.g., from a GeoDataFrame)  
  - `start_date`, `end_date`: Analysis time range in `YYYY-MM-DD` format  
  - `day_interval`: Temporal resolution (e.g., `1` for daily statistics)  
  - `data_set`: The specific dataset to query (e.g., LST)

- **`stats_to_df(response_json)`**  
  Parses a Statistical API JSON response and transforms it into a `pandas.DataFrame`.  
  This function extracts the relevant statistics and structures them for analysis or visualization.

## ⚙️ Utilities in `utils.py`
- Global variables
- **`evalscript`**  
  This script defines how Sentinel Hub should process and return the data. It is written in a JavaScript-like language and is passed with each request to the API.  
  The current `evalscript` performs the following:

  - Filters scenes based on **local solar time**, specifically selecting observations made at **13:30** (can be changed to 01:30 or left open)
  - Extracts the **Land Surface Temperature (LST)** values and applies a **scale factor of 1/100**
  - Filters out invalid pixels using the **dataMask**
  - Returns data in a format compatible with **Statistical API** output for numerical analysis (via `eobrowserStats`)
  
  ### Key Features:
  - Supports custom visualization ranges via `color_min` and `color_max`
  - Selects the best-quality sample using a valid `dataMask`
  - Outputs a single-band float value per pixel for downstream statistical analysis

  This script is optimized for statistical queries (not visual imagery) and ensures clean, valid data by applying masks and selecting a consistent sensing time.
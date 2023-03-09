# Case Farfetch

## Data Extraction and Transformation
The two scripts are created and the files with the content required were also uploaded.
Comments were added to explain what was done in each part


## Data Engineering in Production

**Using typical sales data as an example, how would you ensure that a data pipeline is kept up to date with accurate data? What tools or process might you use so that sales data is updated daily?**

I would create jobs that would check the data from gold tables and compare with the data found in APIs/Software of the sales, 
so that in case a new sales was registered ou altered, 
this new data would be sent to a raw table so that later it could be standardized and oblige with the criteria of the table that it populates, proceeding with the upsert in the table.
It would require an orchestration tool like AWS Glue, Apache Airflow, CTRL-M or something like that for starting the jobs each day and 
start the process of checking and updating any data that was changed or created. For the scripts would use Python and/or also SQL , depending on the performance of the upsert, and also would Delta Tables for the first steps in this pipeline.
Or to keep it in one single workspace, would Databricks for the orchestration and management of jobs and resources.


**Our sales and product data is constantly changing - returns can affect previous sales, pricing changes can affect product data tables, etc. - how would you go about building a data pipeline that is able to add new data while also changing or updating existing data that has changed at the source system?**

I would use Delta tables to make the upsert in the data easier in the bronze and silver layers, so it wouldn't affect the system with constants changes. 
And for the gold layer, I would program so that, from time to time (maybe even trying to keep near real-time), the tables that feed the source system would be updated and replicated through different servers to guarantee that the data is kept safe in more than one place in case of a system crash.
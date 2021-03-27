# Benchmarking PostGIS load and query times on various datasets

## Goals
- Set up container network containing some or all of the following:
  - GUI
    - Vanilla HTML, JS, and CSS to start. No need to get fancy 
  - DB running PostGIS
  - Synthetic data generator (Python 3 container)
  - Real data loader (Python 3 container)
- Record time it takes to load data 
  - Not sure what the best way to do this is
  - Record from querier's perspective?
  - Agent in DB container collecting / reporting metrics?
  - Both?
- Run randomly generated queries bounded by parameters defined by the user in the GUI.
  - Record time it takes for queries to return
  - Parameters User can provide:
    - min,max Lat
    - min,max Lon
    - Limit
  
## Deployment
- docker-compose on a single node to start
- In future scale across multiple machines
  - K8s
  - Docker Swarm?
  - Nomad?

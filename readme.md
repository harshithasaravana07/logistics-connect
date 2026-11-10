# purvottar Setu— Disaster-Resilient Smart Logistics & Geo-Spatial Accessibility Intelligence Platform

> **An AI-powered multimodal logistics and geo-spatial command platform built for disaster-prone, mountainous, and low-connectivity regions—combining real-time GIS hazard overlays, landslide/flood prediction, dynamic convoy rerouting, GPS essential cargo tracking, and two-way offline-first multilingual field reporting.**

## 1. Overview & Problem Context

Disaster-prone and difficult-terrain regions (such as mountain passes, floodplains, and remote border districts) face severe logistics and accessibility disruptions caused by landslides, flash floods, extreme rainfall, bridge load restrictions, and communication blackouts. Delays in transporting essential commodities—such as life-saving medicines, vaccines, food grains, agricultural produce, and emergency construction materials—directly impact public safety and disaster relief operations.

*Purvottar Setu* provides a unified **Officials Web Command Console** and **Field Reporter Communication Hub** that turns fragmented weather, satellite, GPS, and ground reports into real-time operational decisions.

## 2. Core Features

### Central GIS & Accessibility Monitoring

* **Multi-Layer Interactive GIS Map**: Switch seamlessly between **Sentinel-2 Satellite**, **Vector Highway Schematic**, and **IMD Doppler Rainfall & Flood Inundation Radar** views.

* **Live Corridor & Bridge Health**: Color-coded highway and bridge status (*Clear*, *Caution / Single-Lane / Load Restricted*, *Critical / Blocked*) with district-level connectivity metrics and 12-hour historical trend charts.

* **District Supply-Chain Bottleneck Matrix**: Tracks essential stock buffers (in days) across districts and maps active emergency bypass corridors.

### AI Disruption Prediction & Dynamic Route Optimization

* **Hazard Susceptibility Scoring**: Uses ensemble gradient boosting (**XGBoost + LightGBM**) fused with rainfall intensity, slope terrain, and historical incident data to assign real-time risk scores (0–100%) to every monitored highway segment.

* **AI Safe & Fast Alternate Route Engine**: Automatically computes safest alternate routes around blocked or flooded stretches using hazard-weighted **Dijkstra / A\*** graph routing, displaying comparative ETA delays and hours saved.

* **One-Click Fleet Reroute Broadcast**: Dispatches updated turn-by-turn waypoints directly to affected supply convoys.

### GPS Essential Commodity & Fleet Tracking

* **Cargo-Priority Telemetry**: Filter and monitor active supply vehicles by commodity category (**Medicines & Cold-Chain Vaccines**, **Food Supplies & PDS Grains**, **Agricultural Produce**, and **Bailey Bridge / Construction Materials**).

* **Live Convoy Status**: Displays real-time GPS coordinates, transit speed, corridor assignment, and dynamic ETA adjustments (*On Time*, *Delayed*, *AI Rerouted*).

### Two-Way Field Reporter Notification Inbox & Official Response Desk

* **Geo-Tagged Ground Reports**: Receives verified field incident submissions from PWD/BRO engineers, DDMA officers, and ground inspectors complete with GPS coordinates and categorized photo evidence (*Landslide Debris*, *Flash Flood Waterlogging*, *Bridge/Culvert Damage*).

* **Official Command Reply & Directive Composer**: Enables control-room officials to inspect field reporter threads, select official actions (*Approve Reroute & Dispatch Clearance*, *Deploy SDRF / Police Escort*, *Issue Load/Speed Restriction*, *Mark Incident Resolved*), and reply via **App Push + Offline SMS Fallback** or **VHF Radio**.

* **Instant Notification Management**: Includes unread counters, status filters (*All*, *Awaiting Response*, *Responded*), and one-click dismissal (`×`) across banners, alerts, and inbox threads.

### Offline-First Synchronization & Full-Website Multilingual UI

* **Low-Network Offline Sync Queue**: Caches field reports locally in **IndexedDB / Local Storage** when connectivity drops in remote valleys and automatically synchronizes with the central **PostGIS** cloud when network access returns.

* **Full-Website Multilingual Localization**: Instant 1-click translation of the entire console interface, map overlays, and SMS/Push broadcast payloads across **7 languages** (*English, Assamese / অসমীয়া, Hindi / हिन्दी, Khasi, Mizo, Manipuri / মৈতৈলোন্, and Nagamese*).

* **Unified Light & Dark Mode + Dual Independent Scroll Layout**: Features a docked right-side Console menu with its own independent scrollbar and full Light/Dark theme parity across all cards, charts, and tables.

## 3. System Architecture

```
+-----------------------------------------------------------------------------------+
|                           DATA SOURCES & SENSORS                                  |
|  • Satellite Imagery (ISRO Bhuvan / Sentinel-2: Terrain, Land-Use, Flood Extent)  |
|  • Weather Feeds (IMD Doppler Radar, Rainfall Intensity, River Gauge APIs)        |
|  • Fleet Telemetry (GPS Vehicle Trackers, Cargo Manifests, Speed & ETA Logs)      |
|  • Ground Intelligence (Geo-Tagged Field Officer Reports, Photos, Slope Sensors)  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                       BACKEND & AI/ML PROCESSING LAYER                            |
|  • Data Ingestion & Fusion Pipeline (Python, GeoPandas, Spatial Preprocessing)    |
|  • AI Hazard & Disruption Engine (XGBoost / LightGBM / LSTM Rainfall-Slide Model) |
|  • Dynamic Route Optimizer (Hazard-Weighted Graph Routing + Delay Estimator)      |
|  • Spatial Database (PostgreSQL + PostGIS for Road Network Topology & Telemetry)  |
|  • REST & WebSocket API Gateway (FastAPI + Role-Based Access Control)             |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                   FRONTEND COMMAND CONSOLE & FIELD INTERFACES                     |
|  • Officials Web Dashboard (Interactive GIS Map, KPI Console, Fleet Tracker)      |
|  • 2-Way Field Reporter Notification Inbox & Official Directive Dispatcher        |
|  • Offline-First PWA Sync Engine (IndexedDB Queue + Service Worker Auto-Sync)     |
|  • 7-Language Localization Engine + SMS / Push / VHF Alert Broadcaster            |
+-----------------------------------------------------------------------------------+

```

## 4. Tech Stack

| Layer | Technologies Used | 
| ----- | ----- | 
| **Frontend Web Console** | HTML5, Tailwind CSS, Vanilla ES6+ JavaScript / React.js, Chart.js, Interactive SVG & Leaflet/Mapbox GIS Layers | 
| **Offline & Mobile Support** | Progressive Web App (PWA), IndexedDB Local Sync Queue, Responsive Dual-Scroll Layout | 
| **Backend & APIs** | Python 3.11+, FastAPI, Uvicorn, WebSockets (Live GPS & Alert Streaming) | 
| **AI / Machine Learning** | XGBoost, LightGBM, Scikit-learn, LSTM (Antecedent Rainfall Landslide Prediction), NetworkX (Graph Routing) | 
| **Database & GIS Storage** | PostgreSQL 15+, PostGIS, GeoPandas, Shapely | 
| **External Integrations** | IMD Weather APIs, ISRO Bhuvan / Sentinel-2 Tile Feeds, SMS / Push Notification Gateways | 

## 5. Getting Started

### Quick Preview (Standalone Web Console)

The interactive frontend command console (`purvottar_setu_console.html`) is self-contained and runs directly in any modern browser with zero build steps required:

1. Clone this repository:

   ```
   git clone https://github.com/<your-username>/setu-ai-disaster-logistics.git
   cd setu-ai-disaster-logistics
   
   ```

2. Open the console directly in your browser or serve it locally:

   ```
   python3 -m http.server 8080
   
   ```

3. Visit `http://localhost:8080/purvottar_setu_console.html` to explore:

   * **Overview**: District connectivity KPIs, 12-hour connectivity/delay chart, corridor status, and supply-chain bottleneck matrix.

   * **Map & Routes**: Interactive GIS risk overlay (*Satellite / Schematic / Rainfall Radar*) and AI Route Optimizer.

   * **Vehicle Tracking**: Live GPS commodity fleet cards filterable by cargo type.

   * **Notifications & Inbox**: Two-way Field Reporter message threads and Official Response composer.

   * **Field Reports**: Manual control-desk logging and Offline Sync Queue simulator.

## 6. User Roles Supported

* **Central / Regional Disaster & Logistics Operators**: Full visibility across all districts, GIS layers, and AI route optimizations.

* **SDMA Disaster Control Officers**: Focused on incoming field reporter hazard alerts, SDRF/BRO dispatch, and emergency road clearance.

* **Logistics & Supply Commissioners**: Monitors essential commodity stock buffers (medicines, food grains, fuel) and fleet ETA delays.

* **District Nodal Officers (PWD / BRO)**: Coordinates ground inspection teams, bridge load limits, and slope clearance updates.

## 7. Team & Acknowledgments

* **Team Name**: NAVRA

* **Problem Statement Reference**: Government disaster agencies in India lack a unified, real-time predictive routing system to anticipate disaster-induced road blockages, resulting in delayed emergency deployments, disrupted relief supply chains, and isolated communities during floods and landslides.

* **Theme**: Transportation & Logistics / Disaster-Resilient Infrastructure
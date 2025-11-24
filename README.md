# HydraX: AI-Powered Rainwater Harvesting Predictor

HydraX is an AI-driven sustainability tool designed to help the City of London, UK, estimate how much rainwater buildings can collect over the next 10 years. By combining geospatial data, historical weather records, coordinate conversion, and machine learning, HydraX allows users to input any London address and receive a detailed estimate of a building's potential rainwater collection.  

The project directly contributes to two **United Nations Sustainable Development Goals (SDGs)**:

- **SDG 6 — Clean Water & Sanitation**: HydraX promotes efficient water management by identifying potential rainwater harvesting opportunities.  
- **SDG 11 — Sustainable Cities & Communities**: HydraX supports sustainable urban planning by providing data-driven insights on building-level water conservation.

---

## 📌 Project Purpose

London, like many urban areas, experiences significant rainfall but lacks systematic utilization of rooftop rainwater. HydraX addresses this challenge by:

- Calculating the rainfall collection potential of individual buildings  
- Enabling users to assess long-term water savings  
- Supporting sustainable urban development and planning  
- Educating citizens and policymakers on rainwater harvesting opportunities

The system encourages environmentally conscious behavior and provides actionable insights to reduce water waste in cities.

---

## 🧠 How HydraX Works

HydraX integrates multiple datasets, coordinate systems, and machine learning to provide accurate predictions. The workflow is as follows:

### 1. User Address Input
- Users enter any address in London through the frontend interface.  
- The system captures this input for processing.

### 2. Geocoding
- The **Google Maps Geocoding API** is used to:
  - Validate the user-provided address  
  - Convert it to precise **latitude and longitude coordinates** (WGS84 format)

### 3. Coordinate Conversion (WGS84 → British National Grid)
- The London building dataset uses the **British National Grid (BNG)** coordinate system.  
- HydraX converts the Google WGS84 coordinates to BNG eastings and northings to match the building data.

### 4. Matching to the Nearest Building
- After converting coordinates, HydraX searches the building dataset to find the closest building footprint.  
- Each building entry contains:
  - Easting & northing (BNG)  
  - Rooftop area (in square meters)

### 5. Datasets Used
HydraX relies on two primary datasets:

#### **Building Dataset**
- Contains **all buildings in London, UK**  
- Provides **BNG coordinates** for each building  
- Includes **rooftop area**, which is essential for calculating potential water collection

#### **London Weather Dataset**
- Contains **daily precipitation data** for London  
- Covers the years **1979–2020**  
- Used to analyze historical rainfall patterns and train a predictive model for the future

### 6. Machine Learning Prediction
HydraX uses **scikit-learn** to model rainwater collection potential:

- Inputs:
  - Building rooftop area (from building dataset)  
  - Historical daily precipitation (from `london_uweather`)  
- Output:
  - Estimated **total rainwater harvestable over the next 10 years**  
- This allows users to see how much water could be collected if a rainwater harvesting system were installed.

### 7. Frontend Display
- The backend sends the calculated estimate to the frontend  
- Users can view:
  - The predicted water collection in liters  
  - A visualization of potential savings  
  - Interactive options to test multiple addresses

---

## ✨ Key Features

- 🌧️ Predicts **10-year rainwater collection potential** for any London building  
- 🏢 Accepts any valid **London UK address**  
- 📍 Automates **geocoding and coordinate conversion**  
- 🗺️ Matches user input to **nearest building footprint**  
- 🤖 Uses **machine learning** to forecast rainfall and collection potential  
- 🌱 Supports **SDG 6 (Clean Water & Sanitation)** and **SDG 11 (Sustainable Cities & Communities)**  
- 📊 Provides clear, actionable insights for urban planners, building owners, and sustainability teams

---

## 🛠️ Tech Stack

**Frontend**  
- Next.js
- Node.js
- React
- TailwindCSS
- Framer Motion

**Backend**  
- Python  
- Flask
- Scikit-learn library
- Google Maps Geocoding API for address-to-coordinate conversion  
- Coordinate conversion utilities (WGS84 → British National Grid)  

**Data**  
- London building rooftop dataset (eastings, northings, rooftop area)  
- London historical precipitation dataset (`london_uweather`, 1979–2020)

---

## 🚀 How to Use HydraX

1. Open the HydraX frontend interface  
2. Enter any London address  
3. HydraX converts the address to coordinates and matches the nearest building  
4. The ML model predicts rainwater collection potential over the next 10 years  
5. Results are displayed, including estimated liters of water saved

---

## 🌱 Project Impact

HydraX empowers:

- **City planners**: Incorporate rainwater harvesting data into urban planning  
- **Building owners**: Understand potential water savings for rooftops  
- **Sustainability teams**: Identify areas with the highest potential impact  
- **Environmental researchers**: Analyze urban water sustainability trends  

By providing building-specific rainwater predictions, HydraX contributes to reducing water waste, promoting sustainability, and creating more resilient cities.

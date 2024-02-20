# Software Requirements Document (SRD)

## 1. Introduction
This document outlines the software requirements for a web application that integrates the Dublin Bike API provided by JCDecaux, the Open Weather API, and Google Maps. The application will provide real-time and predictive information about bike availability and weather conditions to users on both mobile and PC browsers.

### 1.1 Purpose
The purpose of this document is to provide a detailed description of the functional and non-functional requirements for the web application. It serves as a guideline for developers and stakeholders to understand the functionalities, system integration, and user interactions involved in the application.

### 1.2 Scope
The application will:
- Retrieve bike station data from the Dublin Bike API.
- Fetch weather data from the Open Weather API.
- Use Google Maps for displaying bike stations.
- Accept user input for location and date/time.
- Display real-time bike and stand availability and weather information.
- Predict future bike and stand availability using a machine learning model.

## 2. Overall Description

### 2.1 User Needs
- **Real-Time Information**: Users require immediate information on bike availability and weather conditions.
- **Future Predictions**: Users plan ahead with predictions on bike availability.
- **Availability**: Easy access on both ~~mobile~~ and PC browsers. (Mobile will be least priority to implement)

### 2.2 Assumptions and Dependencies
- Availability of APIs (Dublin Bike API, Open Weather API, and Google Maps).
- Reliable internet connection for users and server.
- Availability of a machine learning model for predictions.

## 3. System Features and Requirements

### 3.1 Functional Requirements
1. **Data Integration**:
   - Integrate with Dublin Bike API to fetch real-time data on bike stations.
   - Integrate with Open Weather API to get current and forecasted weather data.
   - Utilize Google Maps API for displaying bike stations on a map.

2. **User Input**:
   - Allow users to input a specific location and date/time.

3. **Real-Time Data Display** (for present or past input time):
   - Show available bikes and vacant stands at the closest 5 bike stations.
   - Display current weather information at the selected location.

4. **Predictive Analysis** (for future input time):
   - Send user input to the machine learning model for inference.
   - The model should consider date, weekday, weather, and time as features.
   - Display predictions on the top 5 most likely bike stations for availability.

### 3.2 Non-Functional Requirements
1. **Performance**:
   - Response time for data retrieval and display should be within 5 seconds.
   - Predictive analysis results should be provided within 10 seconds.

2. **Usability**:
   - User interface should be intuitive and easy to navigate.
   - Ensure compatibility with major browsers on PC and mobile platforms.

3. **Reliability**:
   - Application should have an uptime of 99.9%.

4. **Security**:
   - Ensure data transmission is secured using HTTPS.
   - Comply with data protection regulations for user data.

5. **Scalability**:
   - System should be scalable to accommodate an increasing number of users.

6. **Maintainability**:
   - Code should be well-documented for easy maintenance.
   - Regular updates for API integration compatibility.

## 4. External Interface Requirements
- **User Interfaces**: Web-based UI compatible with mobile and PC browsers.
- **Hardware Interfaces**: N/A.
- **Software Interfaces**: APIs (Dublin Bike, Open Weather, Google Maps), Machine Learning Model.
- **Communication Interfaces**: HTTPS for secure data transmission.

## 5. Other Nonfunctional Requirements
- **Legal Requirements**: Compliance with GDPR and other relevant data protection laws.
- **Environmental Requirements**: N/A.

## 6. Appendices
- Appendix A: API Documentation Links.
- Appendix B: Machine Learning Model Specifications.
- Appendix C: User Interface Mockups.

---

This document sets a comprehensive framework for the development, deployment, and maintenance of the web application. It ensures that the end product aligns with user needs and technical specifications.


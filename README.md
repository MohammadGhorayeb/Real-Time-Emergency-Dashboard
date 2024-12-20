# **Emergency Response System**

An interactive web application that processes user input, predicts emergency categories using machine learning, and displays relevant sub-locations on a dynamic Mapbox map. The platform supports real-time data visualization and aims to assist emergency responders in critical situations.

---

## **Features**
- **User Authentication**:
  - Login and registration system with secure password handling.
  - Location input for personalization.

- **Emergency Prediction**:
  - Processes user-provided text and predicts the type of emergency (e.g., "Rescue Operations," "Medical Assistance").
  - Utilizes a fine-tuned BERT-based model for classification.

- **Location Mapping**:
  - Identifies sub-locations (cities, villages) mentioned in the text.
  - Dynamically adds pinpoints to a 3D Mapbox map.
  - Re-centers the map to display all extracted locations.

- **User-Friendly Interface**:
  - Professionally styled pages for login, registration, and main functionalities.
  - Real-time interaction with responsive design.

---

## **Technologies Used**
### **Frontend**
- **HTML/CSS/JavaScript**:
  - Styled components for intuitive user experience.
  - Integrated with Mapbox for real-time mapping.

### **Backend**
- **Flask**:
  - Handles routing, authentication, and model integration.
- **Google Maps API**:
  - Retrieves geographical coordinates for sub-locations.
- **Mapbox**:
  - Provides dynamic map visualization.

### **Machine Learning**
- **BERT-based Model**:
  - Fine-tuned for emergency text classification.
- **OpenAI API**:
  - Extracts sub-location data (cities, villages) from user input.
- **Llama API**:
  - Provides a small description of the emergency.

### **Database**
- **SQLite**:
  - Stores user data and location history.

---

## **Setup Instructions**

### **1. Clone the Repository**
Clone the project from GitHub:
```bash
git clone https://github.com/MohammadGhorayeb/490_Project
```

### **2. Navigate to the Project Directory**
Move to the project folder:
```bash
cd 490_Project
```

### **3. Install Dependencies**
Ensure you have Python 3.9+ installed. Install the required libraries using pip:
```bash
pip install -r dependencies.txt
```

### **4.Run the Application**
Navigate to the web folder and start the Flask app:
```bash
cd web
python app.py
```





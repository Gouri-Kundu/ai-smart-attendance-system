
# SnapClass 

### AI-Powered Smart Attendance System using Face & Voice Recognition

---

##  Problem Statement

Traditional attendance systems in classrooms are:

* Time-consuming
* Prone to manual errors
* Easy to proxy or fake
* Difficult to track in real-time analytics

**SnapClass solves this by automating attendance using AI-based Face and Voice Recognition.**

It enables teachers to take attendance automatically from classroom images or audio recordings, and allows students to register and be identified using biometric-like embeddings.

---

## Solution Overview

SnapClass is a full-stack AI-powered attendance system built using **Streamlit + Supabase + Machine Learning pipelines**.

It works in two intelligent modes:

###  Face-Based Attendance

* Classroom images are captured or uploaded
* Faces are detected using **dlib**
* Each face is converted into a **128-d embedding**
* A trained **SVM classifier (Scikit-learn)** matches embeddings to students
* Attendance is marked based on similarity thresholding

###  Voice-Based Attendance

* Classroom audio is recorded
* Audio is split into speech segments using **librosa**
* Each segment is converted into embeddings using **Resemblyzer**
* Speaker identification is performed using embedding similarity (dot product on normalized voice embeddings, equivalent to cosine similarity).
* Attendance is logged for matched students

---

## System Architecture

```
Student / Teacher UI (Streamlit)
        ↓
Preprocessing Layer
   - Face detection (dlib)
   - Audio segmentation (librosa)
        ↓
Embedding Generation
   - Face embeddings (dlib face model)
   - Voice embeddings (Resemblyzer)
        ↓
ML Matching Layer
   - SVM classifier (face)
   - Cosine similarity (voice)
        ↓
Database Layer (Supabase)
   - Students
   - Subjects
   - Attendance logs
        ↓
Dashboard & Analytics UI
```

---

##  Key Features

### Teacher Module

* Create and manage subjects
* Take attendance using:

  * Face recognition from classroom photos
  * Voice recognition from audio recordings
* View attendance analytics
* Share class using QR code or join link
* Attendance history tracking

### Student Module

* Face-based login system
* Optional voice registration
* Enroll using subject code / QR
* View attendance records
* Unenroll from subjects

---

##  Machine Learning Details

### Face Recognition

* Model: `SVM (Linear Kernel)`
* Feature extractor: `dlib face_recognition_model_v1`
* Input: 128-d face embeddings
* Matching: Euclidean distance thresholding

### Voice Recognition

* Model: Embedding similarity matching
* Feature extractor: `Resemblyzer VoiceEncoder`
* Similarity metric: cosine similarity
* Speech segmentation using `librosa.effects.split`

---

##  Tech Stack

* **Frontend:** Streamlit
* **Backend:** Supabase (PostgreSQL)
* **ML Libraries:** dlib, scikit-learn, resemblyzer, librosa
* **Data Processing:** NumPy, Pandas
* **Image Processing:** Pillow
* **QR Generation:** segno

---

##  Workflow Summary

1. Teacher creates a subject
2. Students register using face/voice
3. Embeddings are stored in database
4. Teacher uploads/captures classroom data
5. AI detects students from face/voice
6. Attendance is automatically logged
7. Analytics dashboard displays results

---

##  Project Structure

```
SNAPCLASS/
│
├── app.py
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── secrets.toml
│
├── src/
│   ├── components/        # UI dialogs & reusable widgets
│   ├── database/          # Supabase operations (CRUD)
│   ├── pipelines/         # ML models (face + voice)
│   └── screens/           # Teacher & Student UI logic
```

---

##  Setup Instructions

```bash
git clone https://github.com/your-username/snapclass.git
cd snapclass
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

##  Environment Variables

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "your_url"
SUPABASE_KEY = "your_key"
```

---

##  Key Highlights 

* Real-world AI application 
* Combines **computer vision + speech processing**
* End-to-end full-stack implementation
* Multi-user system (teacher/student roles)
* Practical deployment-ready architecture
* Processes structured data (Supabase relational tables) and unstructured data (images and audio), converting them into embeddings for AI-based recognition and attendance logging.

---

##  Author

**Gouri Kundu**

---

##  Contact

Gouri Kundu  
GitHub: https://github.com/Gouri-Kundu  
Email: gourikundu1808@gmail.com
LinkedIn: https://www.linkedin.com/in/gouri-kundu 
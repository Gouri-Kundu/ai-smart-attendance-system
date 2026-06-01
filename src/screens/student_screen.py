
import streamlit as st
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

def student_dashboard():
    student_data= st.session_state.student_data
    student_id= student_data['student_id']

    c1, c2, c3= st.columns(3, vertical_alignment= 'center', gap= 'xxlarge')
    with c3:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout", type= 'secondary', key= 'loginbackbtn'):
            st.session_state['is_logged_in']= False
            del st.session_state.student_data
            st.rerun()

    st.space()

    c1, c2= st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type= 'primary', width= 'stretch'):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects...'):
        subjects= get_student_subjects(student_id)
        logs= get_student_attendance(student_id)

    stats_map= {}

    for log in logs:
        sid= log['subject_id']   #sid= subject_id

        if sid not in stats_map:
            stats_map[sid]= {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols= st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub= sub_node['subjects']
        sid= sub['subject_id']

        stats= stats_map.get(sid, {"total": 0, "attended": 0})
        def unenroll_button():
            if st.button("Unenroll from this course",  key= f"unenroll_{sid}", type= 'tertiary', width= 'stretch', icon= ':material/delete_forever:'):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f"Unenrolled from {sub['name']} successfully!")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name= sub['name'],
                code= sub['subject_code'],
                section= sub['section'],
                students=stats['attended'],
                classes=stats['total']
            )
            unenroll_button()



def student_screen():
    if "student_data" in st.session_state:
        student_dashboard()
        return
    c1, c2, c3= st.columns(3, vertical_alignment= 'center', gap= 'xxlarge')
    with c3:
        if st.button("Go back to Home", type= 'secondary', key= 'loginbackbtn'):
            st.session_state['login_type']= None
            st.rerun()

    st.header('Login using FaceID', text_alignment= 'center')
    st.space()
    
    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    photo_source= st.camera_input("Position your face in the center")
    if st.button("Register New Student"):
        st.session_state.show_registration = True
    
    if photo_source:
        img= np.array(Image.open(photo_source))

        with st.spinner('AI is scanning...'):
            detected, all_ids, num_faces= predict_attendance(img)

            if num_faces == 0:
                st.warning('Face not found!')
            elif num_faces >1:
                st.warning('Multiple faces found!')
            else:
                if detected:
                    if not st.session_state.show_registration:
                        student_id= list(detected.keys())[0]
                        all_students= get_all_students()
                        student= next((s for s in all_students if s['student_id']== student_id), None)

                        if student:
                            st.session_state.is_logged_in= True
                            st.session_state.user_role= 'student'
                            st.session_state.student_data= student
                            st.toast(f"Welcome Back {student['name']}")
                            time.sleep(1)
                            st.rerun()
                else:
                    st.info('Face not recognized! You might be a new student!')
                    st.session_state.show_registration= True

    if st.session_state.show_registration:
        with st.container(border= True):
            st.header('Register new profile')
            new_name= st.text_input("Enter your name", placeholder= 'e.g. Dipika Sen')

            st.subheader('Optional: Voice Enrollment')
            st.info("Enroll your voice for attendance")

            audio_data= None

            try:
                audio_data= st.audio_input('Record a short phrase like I am present and my name is Dipika Sen.')
            except Exception:
                st.error('Audio data failed!')

            if st.button('Create Account', type= 'primary'):
                if not photo_source:
                    st.error("Please capture a face photo first")

                elif not new_name:
                    st.error("Please enter your name")

                else:
                    with st.spinner('Creating profile...'):
                        img= np.array(Image.open(photo_source))
                        encodings= get_face_embeddings(img)

                        if encodings:
                            face_emb= encodings[0].tolist()

                            voice_emb= None
                            if audio_data:
                                voice_emb= get_voice_embedding(audio_data.read())
                                
                            response_data= create_student(new_name, face_embedding= face_emb, voice_embedding= voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in= True
                                st.session_state.user_role= 'student'
                                st.session_state.student_data= response_data[0]
                                st.session_state.show_registration = False
                                st.toast(f'Profile created! Hi {new_name}')
                                time.sleep(1)
                                st.rerun()



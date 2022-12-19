import streamlit as st
import pandas as pd
import numpy as np
import controller.user as usrc
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
from PIL import Image
import cv2
import torch
import time
#import numpy as np
import av
#import mediapipe as mp
usrc.create_table()
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


def main():
    st.title("COLD DRINKS INVENTORY MANAGEMENT")
    # usrc.create_table()

    menu = ["None","Staff"]
    choice = st.selectbox("Mode", menu)
    
    if choice=="Staff":
        st.subheader("Staff")
        with st.sidebar:
            d=st.date_input("Date")
            val=st.slider('confidence threshold',0.00,1.00)
            @st.cache
            #device = 'cpu'
            #if not hasattr(st, 'classifier'):
            def model():
                #st.model = torch.hub.load('ultralytics/yolov5', 'yolov5s',  _verbose=False)
                return torch.hub.load('ultralytics/yolov5', 'custom', path="b.pt",force_reload=True)
                #st.model.confi=val
            mod=model()
            
            class VideoProcessor:
                def __init__(self):
                    self.results=None
                    self.confidence=0.5
            
                def res(self):
                    return self.results
                def recv(self, frame):

                    img = frame.to_ndarray(format="bgr24")
                    mod.conf=self.confidence
                   
                    # vision processing
                    flipped = img[:, ::-1, :]

                    # model processing
                    im_pil = Image.fromarray(flipped)
                    results = mod(im_pil, size=112)
                    self.results = results
                    bbox_img = np.array(results.render()[0])

                    return av.VideoFrame.from_ndarray(bbox_img, format="bgr24")
            ch=['📽️video','📊data','🖼️image']
            q=st.radio('View Mode',ch)
            if(q=="📊data"):
                d=usrc.read_()
                op=['None','CSV']
                t=st.radio('Download Mode',op)
                df = pd.DataFrame(d)
                if(t=="None"):
                    pass
                #if t=="Excel":
                   # st.download_button(label='download excel',data="abc.xlsx",mime='text/xlsx')
                    #st.write('Data is written successfully to Excel File.')
                if t=="CSV":
                    st.download_button(label='download csv',data=df.to_csv(),mime='text/csv')
                    st.write('Data is written successfully to csv File.')


        if q=="📽️video":
            st.subheader("📽️video")
            webrtc_ctx = webrtc_streamer(
                key="WYH",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=RTC_CONFIGURATION,
                video_processor_factory=VideoProcessor,
                media_stream_constraints={"video": True, "audio": False},
                async_processing=False,
            )
            if webrtc_ctx.state.playing:
                    webrtc_ctx.video_processor.confidence=val
            lab=st.checkbox("Show the detected labels")
            store=st.checkbox("store")
            if (lab):
                empty=st.empty()
                if webrtc_ctx.state.playing:
                    while True:
                        if webrtc_ctx.video_processor:
                            result = webrtc_ctx.video_processor.res()
                            
                            if result!= None:
                                co= result.pandas().xyxy[0]['Name'].value_counts()
                                st.sidebar.table(co)
                                ##empty.write(c)
                                for i in co.index:
                                    if (store):
                                        usrc.create(d,i,int(co[i]))
                                st.write("database has been updated")
                            else:
                                empty.write("No labels detected")  
                            time.sleep(10)
                        else:
                            break
            
            


        if q=="🖼️image":
            st.subheader("🖼️image")
            im=st.file_uploader('upload_image',type=['png','jpg','jpeg'])
            if(im):
                img =np.array(Image.open(im))
                mod.conf=val
                    

                    # model processing
                im_pil = Image.fromarray(img)
                results = mod(im_pil, size=112)
                bbox_img = np.array(results.render()[0])
                st.image(bbox_img,caption="Processed Image",use_column_width=True)

                C = results.pandas().xyxy[0]['Name'].value_counts()
                
                st.sidebar.table(C)
                if(st.checkbox("Store")):
                    for  x in C.index:
                        usrc.create(d, x, int(C[x]))
                        st.write("database has been updated")
            
        if q=="📊data":
                st.subheader("📊data")
                with st.form("f1",clear_on_submit=True):
                    dtime=st.date_input("Date")
                    dname=st.text_input("Name")
                    dcount=st.number_input("Count",min_value=0,step=1)
                    submit=st.form_submit_button("Submit")
                if(submit):
                    
                    usrc.create(dtime,dname,dcount)
                table=usrc.read_()
                st.table(table)
                ctt=usrc.count_()
                st.table(ctt)
                    



    
    if choice=="None":
        pass

            
main()

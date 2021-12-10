# Retrieval_Streamlit_Demo
 Cross-Encoder-with-Bi-Encoder를 활용한 WebPage 데모

## Download
```python
pip install gdown

cd assets # assets 폴더로 이동한 후 다운로드
gdown --id 1kRTaqreKQAgP23qPeNMigScht0Urb__C # c_encoder download
gdown --id 1ItJy8VA9NMah5E81OtwMSz98tvPXar-4 # passage_embedding download
gdown --id 1ObVAiZCm_285Nqeb1lAxW2i_jN08I9Jg # q_encoder download
gdown --id 1O-kxt4DupOibNhkwmg3luTLt07faRgvO # wiki data upload
```

## Install Requirements
```python
bash install_requirements.sh
```

## Demo Implementation
```python
cd .. # clone 폴더로 이동
streamlit run app.py
```

![Web Demo]<img src='https://user-images.githubusercontent.com/53552847/145511056-0fa31347-d113-434c-b4a3-d25bee76bd49.mp4'>


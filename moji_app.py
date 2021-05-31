#ターミナルでの実行　 streamlit run moji_app.py
import os
from google.cloud import speech
import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/nagasawanaokazu/Desktop/cloud speech-to-text/myproject.json'

def transcribe_file(content,lang='日本語'):

    lang_code = {
        '英語':'en-US',
        '日本語':'ja-JP',
        'ベトナム語':'vi-VN'
    }
    
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=content)
    #設定
    config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
    language_code=lang_code[lang] 
    )
    response = client.recognize(config=config, audio=audio)
    
    for result in response.results:
        text = result.alternatives[0].transcript
        st.write('テキスト化が完了しました ： → ',text)
    
    return text
        
st.title('音声をテキストにするアプリ')
st.subheader('①概要(ファイルをアップロード)')
st.write('※こちらはGoole Speech-to-Textを使用したアプリです。下記リンクを参照ください')
st.markdown('<a href="https://cloud.google.com/speech-to-text/docs?hl=ja">Cloud Speech-to-Text</a>',unsafe_allow_html=True)

upload_file = st.file_uploader('ファイルのアップロード' , type=['mp3' , 'wav'])
st.write('※m4a形式の場合は下記リンクよりmp3又はwav形式に変換してくだい')
st.markdown('<a href = "https://online-audio-converter.com/ja/">Audio Converter</a>',unsafe_allow_html=True)



#Noneじゃなければif文を実行
if upload_file is not None:
    content = upload_file.read()
    st.subheader('ファイル詳細')
    file_details = {'FileName' : upload_file.name, 'FileType' : upload_file.type, 'FileSize' : upload_file.size}
    st.write(file_details)
    st.subheader('②音声の再生')
    st.audio(content)
    
    st.subheader('③言語選択')
    option = st.selectbox('翻訳言語の選択',('英語','日本語','ベトナム語'))
    st.write('選択中の言語 : ',option)
    
    st.subheader('④下の開始ボタンを押すと文字起こしがスタートします')
    if st.button('開始'):
        #空のboxを保持
        coment = st.empty()
        coment.write('文字起こしを開始')
        transcribe_file(content,lang=option)
        coment.write('文字起こしが完了しました！')
        
        st.write('ご利用いただきありがとうございました！')
        
        st.sidebar.markdown('テキストを送付する先のアドレスを入力してください')
        st.sidebar.text_input('E-mail')
        st.text_area('memo', value='')    

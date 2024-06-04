import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from openai import OpenAI

def takeInput():
    # Title
    st.title('QnArt🎨 그림 그리기')
    # Ask for the API key
    api_key = st.secrets["api_key"]

    # Ask for the model choice
    model_choice = "dall-e-3"

    howtocreate = st.selectbox(
        "어떤 방식으로 그림을 생성할까요?",
        ("본인의 경험을 기반으로 그리기", "작품에서 바꾸고 싶은 부분 바꾸기", "작품에서 나타나지 않은 부분 상상하기"),
        index=None,
        key="howtocreate",
        placeholder="그림 생성 방식 선택하기",
    )

    # Takes the user prompt

    if howtocreate == "작품에서 바꾸고 싶은 부분 바꾸기":
        newprompt = "빈센트 반 고흐 <The Bedroom> 작품을 기반으로 해서 아래 부분을 바꿔줘"
    elif howtocreate == "작품에서 나타나지 않은 부분 상상하기":
        newprompt = "빈센트 반 고흐 <The Bedroom> 작품을 기반으로 해서 아래 부분을 추가해줘"
    else:
        newprompt = "나는 동양인 초등학생이야."

    prompt = newprompt + st.text_input("생성할 그림 입력:", key="user_prompt_input")

    return model_choice, prompt, api_key


def generateImage(client, model_choice, prompt):
    if st.button("Generate Image"):
        with st.spinner("이미지 생성 중입니다.."):
            # create the image generation request
            response = client.images.generate(
                model=model_choice,
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1  # This can be modified but currently DALL.E 3 only supports 1
            )
            image_url = response.data[0].url
            print("Generated Image URL:", image_url)

            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))

            # Display the image
            st.image(img)


model_choice, prompt, api_key = takeInput()
# Configure the client
client = OpenAI(api_key=api_key)
# generate image and display it
generateImage(client=client, model_choice=model_choice, prompt=prompt)
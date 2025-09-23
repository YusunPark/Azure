import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from PIL import Image, ImageDraw, ImageFont



load_dotenv()

COMPUTER_VISION_ENDPOINT = os.getenv("COMPUTER_VISION_ENDPOINT")
COMPUTER_VISION_KEY = os.getenv("COMPUTER_VISION_KEY")

# 임시 키를 발급 받아 사용
credential = AzureKeyCredential(COMPUTER_VISION_KEY)
client = ImageAnalysisClient(COMPUTER_VISION_ENDPOINT, credential)  


def get_image_info():
    file_path = input("분석할 이미지 파일 경로를 입력하세요: ")

    with open(file_path, "rb") as image_file:
        image_data = image_file.read()

    
    # 읽어온 이미지데이터를 넘겨줌
    result = client.analyze(
        image_data = image_data, 
        visual_features = [ VisualFeatures.CAPTION, 
                    VisualFeatures.TAGS,        # 한줄평 만들어줌
                    VisualFeatures.OBJECTS],    # 이미지 내 객체 인식 (자동)
        model_version="latest" # 모델 버전
    )

    # cation(한줄평) 출력
    if result.caption is not None:
        print("한줄평:", result.caption.text)
        print("신뢰도:", result.caption.confidence)

    # 태그 출력
    if result.tags is not None:
        print("태그:")
        for tag in result.tags.list:
            print("- 이름:", tag.name , "신뢰도:", tag.confidence)

    # Image에 Draw 객체 생성
    image = Image.open(file_path)
    draw = ImageDraw.Draw(image)    


    # 객체 출력
    if result.objects is not None:
        print("객체:")
        for obj in result.objects.list:
            print(f" - {obj.tags[0].name} (신뢰도: {obj.tags[0].confidence}) at location {obj.bounding_box}")
            
            # 객체 위치에 사각형 그리기
            x, y, w, h = obj.bounding_box["x"], obj.bounding_box["y"], obj.bounding_box["w"], obj.bounding_box["h"]
            draw.rectangle([(x, y), (x + w, y + h)], outline="red", width=10)
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 100)  # macOS 경로 예시
            draw.text((x, y - 100), obj.tags[0].name, fill="red", font=font)

    # 결과 이미지 보기
    image.show()

    # 결과 이미지 저장
    result_image_path = "result_image.png"
    image.save(result_image_path)
    print(f"결과 이미지가 {result_image_path}에 저장되었습니다.")



if __name__ == "__main__":
    get_image_info()

    
    






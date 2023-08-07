
import openai
import concurrent.futures
from flask import Flask, request, jsonify, make_response
import json
import concurrent.futures
from functools import lru_cache
import openai
import pandas as pd
from flask_cors import CORS
import numpy as np

# OpenAI GPT API 키
openai.api_key =

app = Flask(__name__)
CORS(app)

travel_data = pd.read_excel('관광지_en.xlsx')
restaurant_data = pd.read_excel('음식점_en.xlsx')
accommodations_data = pd.read_excel('관광숙박업_en.xlsx')

@app.route('/', methods=['GET'])
def test():
    print("test")
    return jsonify(message='Hello from path!')

@app.route('/init/restaurant', methods=['POST'])
def initial_recommend_restaurant():
    age = request.args.get('age')
    choice = request.args.get('choice')
    gender = request.args.get('gender')
    companion = request.args.get('companion')
    requirements = request.args.get('requirements')
    travel_period = request.args.get('travel_period')
    print("Age:", age)
    print("Choice:", choice)
    print("Gender:", gender)
    print("Companion:", companion)
    print("Requirements:", requirements)
    print("Travel Period:", travel_period)
    return initial_recommend_restaurant(age,gender,companion,requirements,travel_period,restaurant_data,0)

# 초기 맛집 추천
def initial_recommend_restaurant(age, gender, companion, requirements, travel_period, restaurant_data, offset=0):
    recommendations, scores = recommend_restaurant(age, gender, companion, requirements, travel_period, restaurant_data, offset)
    return json.dumps(recommendations, ensure_ascii=False)

# 초기 관광지 추천
def initial_recommend_destination(age, gender, companion, requirements, travel_period, travel_data, offset=0):
    recommendations, scores = recommend_destination(age, gender, companion, requirements, travel_period, travel_data, offset)
    print(json.dumps(recommendations, ensure_ascii=False))
    user_input = input("추천된 관광지 중 하나를 선택해주세요 (1, 2, 3). 더 많은 옵션을 원하시면 '###'를 입력해주세요.\nPlease choose one of the recommended destinations (1, 2, 3) or enter '###' for more options: ")
    if user_input == '###':
        offset += 3
        return initial_recommend_destination(age, gender, companion, requirements, travel_period, travel_data, offset)
    selected_index = int(user_input) - 1
    selected_data = recommendations[selected_index]
    return selected_data

# 초기 숙소 추천
def initial_recommend_hotel(age, gender, companion, requirements, travel_period, accommodations_data, offset=0):
    recommendations, scores = recommend_hotel(age, gender, companion, requirements, travel_period, accommodations_data, offset)
    print(json.dumps(recommendations, ensure_ascii=False))
    user_input = input("추천된 호텔 중 하나를 선택해주세요 (1, 2, 3). 더 많은 옵션을 원하시면 '###'를 입력해주세요.\nPlease choose one of the recommended hotels (1, 2, 3) or enter '###' for more options: ")
    if user_input == '###':
        offset += 3
        return initial_recommend_hotel(age, gender, companion, requirements, travel_period, accommodations_data, offset)
    selected_index = int(user_input) - 1
    selected_data = recommendations[selected_index]
    return selected_data

# 행정구별 맛집 추천
def filter_and_recommend_restaurant(selected_data, age, gender, companion, requirements, travel_period, restaurant_data):
    filtered_data = restaurant_data[restaurant_data['행정구'] == selected_data['행정구']]
    if len(filtered_data) < 3:
        filtered_data = restaurant_data
    recommendations, scores = recommend_restaurant(age, gender, companion, requirements, travel_period, filtered_data, offset=0)
    return recommendations

# 행정구별 관광지 추천
def filter_and_recommend_destination(selected_data, age, gender, companion, requirements, travel_period, travel_data):
    filtered_data = travel_data[travel_data['행정구'] == selected_data['행정구']]
    if len(filtered_data) < 3:
        filtered_data = travel_data
    recommendations, scores = recommend_destination(age, gender, companion, requirements, travel_period, filtered_data, offset=0)
    return recommendations

# 행정구별 숙소 추천
def filter_and_recommend_hotel(selected_data, age, gender, companion, requirements, travel_period, accommodations_data):
    filtered_data = accommodations_data[accommodations_data['행정구'] == selected_data['행정구']]
    if len(filtered_data) < 3:
        filtered_data = accommodations_data
    recommendations, scores = recommend_hotel(age, gender, companion, requirements, travel_period, filtered_data, offset=0)
    return recommendations




####################################################################################################################################################


# 맛집 적합도 평가 함수
def get_restaurant_score(age, gender, companion, requirements, travel_period, restaurant_name, Restaurant_Image_Link, sentiment_score, review_counts, restaurant_type, offset=0):
    prompt = f"""
    Customer's age: {age},
    Customer's gender: {gender},
    Customer's Companion: {companion},
    Customer's requirements: {requirements},
    Travel Period: {travel_period},
    Restaurant name: {restaurant_name},
    Restaurant Review Sentiment Score: {sentiment_score},
    Restaurant Review Counts: {review_counts},
    Restaurant Type: {restaurant_type}

    Based on this information, rate the suitability of the customer and Restaurant as an integer from 1 to 10.
    """

    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=10)
    try:
        score = int(response.choices[0].text.strip())
    except ValueError:
        score = 0

    return score, Restaurant_Image_Link, restaurant_name

# 맛집 추천 함수
def recommend_restaurant(age, gender, companion, requirements, travel_period, restaurant_data, offset=0):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Prepare arguments for get_restaurant_score
        args = [(age, gender, companion, requirements, travel_period, row['Restaurant_name'], row['Restaurant_Image_Link'], row['Restaurant_Review_Sentiment_Score'], row['Restaurant_Review_Counts'], row['Restaurant_Type']) for _, row in restaurant_data.iterrows()]
        # Use map function to execute the function in parallel
        restaurant_scores = list(executor.map(lambda x: get_restaurant_score(*x), args))

    # 점수, 이미지 링크, 맛집 이름으로 이루어진 튜플로 리스트를 재구성
    restaurant_scores = [(score, image_link, restaurant_name) for score, image_link, restaurant_name in restaurant_scores]

    # 점수 내림차순으로 정렬
    restaurant_scores.sort(key=lambda x: x[0], reverse=True)

    # 상위 3개 맛집 선택
    top_3_restaurants = restaurant_scores[offset:offset+3]

    # 추천 이유 생성
    recommendation_reasons = []
    for score, image_link, restaurant_name in top_3_restaurants:
        restaurant_name_ko =  restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_name_ko'].values[0]  # 음식점 한국어 이름 추출
        restaurant_description = restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Description'].values[0]  # 음식점 설명 추출
        restaurant_description_ko = restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Description_ko'].values[0]  # 한국어 음식점 설명 추출
        sentiment_score = restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Review_Sentiment_Score'].values[0]  # 감성 점수 추출
        review_counts = restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Review_Counts'].values[0]  # 리뷰 수 추출
        restaurant_type = restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Type'].values[0]  # 맛집 유형 추출
        restaurant_type_ko = restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Type_ko'].values[0]  # 한국어 맛집 유형 추출
        prompt_reason = [
            {
                "role": "system",
                "content": "You are a food expert"
            },
            {
                "role": "user",
                "content": f"Customer's age: {age}, Customer's gender: {gender},  Customer's Companion: {companion}, Customer's requirements: {requirements}, Travel Period: {travel_period}, 가게이름: {restaurant_name_ko}, Restaurant name: {restaurant_name}, Restaurant Review Sentiment Score: {sentiment_score}, Restaurant Review Counts: {review_counts}, Restaurant Type: {restaurant_type}"
            },
            {
                "role": "system",
                "content": f"Based on this information, could you recommend this restaurant to the customer? If the customer's requirements is in Korean, please respond in Korean."
            }
        ]
        reason_response = openai.ChatCompletion.create(model="gpt-4", messages=prompt_reason, max_tokens=150, temperature=0.6)
        reason = reason_response.choices[0].message['content']
        recommendation_reasons.append(reason)

    # 추천 정보 생성
    restaurant_recommendations = []
    for i, (score, image_link, restaurant_name) in enumerate(top_3_restaurants):
        recommendation = {
            'Rank': i + 1,
            'Score(적합도 점수)': score,
            'Recommendation reason(추천 이유)': recommendation_reasons[i],
            '행정구': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, '행정구'].values[0],
            'image_link': image_link,


            'Restaurant': restaurant_name,
            'Restaurant Description': restaurant_description,
            'Restaurant Review Sentiment Score': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Review_Sentiment_Score'].values[0],
            'Restaurant Review Counts': int(restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Review_Counts'].values[0]),
            'Restaurant_Type': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Type'].values[0],
            'Address': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, '주소'].values[0],
            'Detailed_Directions': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Detailed_Directions'].values[0] if 'Restaurant_Detailed_Directions' in restaurant_data.columns else None,

            '레스토랑명': restaurant_name_ko,
            '음식점 설명': restaurant_description_ko,
            '리뷰 감성점수': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Review_Sentiment_Score'].values[0],
            '리뷰 수': int(restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Review_Counts'].values[0]),
            '가게 카테고리': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Type_ko'].values[0],
            '주소': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, '주소_ko'].values[0],
            '찾아오는 길': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Detailed_Directions_ko'].values[0] if 'Restaurant_Detailed_Directions' in restaurant_data.columns else None
        }
        restaurant_recommendations.append(recommendation)

    return restaurant_recommendations, restaurant_scores



####################################################################################################################################################

# 여행지 적합도 평가 함수
def get_destination_score(age, gender, companion, requirements, travel_period, destination_name, destination_description, image_link, sentiment_score, review_counts, destination_type, offset=0):
    prompt = f"""
    Customer's age: {age},
    Customer's gender: {gender},
    Customer's Companion: {companion},
    Customer's requirements: {requirements},
    Travel Period: {travel_period},
    Destination name: {destination_name},
    Destination description: {destination_description},
    Destination sentiment score: {sentiment_score},
    Destination review counts: {review_counts},
    Destination type: {destination_type}

    Based on this information, rate the suitability of the customer and destination as an integer from 1 to 10.
    """

    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=10)
    try:
        score = int(response.choices[0].text.strip())
    except ValueError:
        score = 0

    return score, image_link, destination_name

# 여행지 추천 함수
def recommend_destination(age, gender, companion, requirements, travel_period, travel_data, offset=0):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Prepare arguments for get_destination_score
        args = [(age, gender, companion, requirements, travel_period, row['여행지명'], row['여행지 설명'], row['이미지링크'], row['감성점수'], row['총 리뷰 수'], row['유형']) for _, row in travel_data.iterrows()]
        # Use map function to execute the function in parallel
        destination_scores = list(executor.map(lambda x: get_destination_score(*x), args))

    # 점수 내림차순으로 정렬
    destination_scores.sort(key=lambda x: x[0], reverse=True)

    # 상위 3개 여행지 선택
    top_3_destinations = destination_scores[offset:offset+3]

    # 추천 이유 생성
    recommendation_reasons = []
    for score, image_link, destination_name in top_3_destinations:
        destination_description = travel_data.loc[travel_data['여행지명'] == destination_name, '여행지 설명'].values[0]  # 여행지 설명 추출
        destination_name_ko = travel_data.loc[travel_data['여행지명'] == destination_name, '여행지명_ko'].values[0]  # 한국어 여행지 이름 추출
        sentiment_score = travel_data.loc[travel_data['여행지명'] == destination_name, '감성점수'].values[0]  # 여행지 감성 점수 추출
        review_counts = travel_data.loc[travel_data['여행지명'] == destination_name, '총 리뷰 수'].values[0]  # 여행지 리뷰 수 추출
        destination_type = travel_data.loc[travel_data['여행지명'] == destination_name, '유형'].values[0]  # 여행지 유형 추출
        prompt_reason = [
            {
                "role": "system",
                "content": "You are a travel expert"
            },
            {
                "role": "user",
                "content": f"Customer's age: {age}, Customer's gender: {gender},  Customer's Companion: {companion}, Customer's requirements: {requirements}, Travel Period: {travel_period}, Destination name: {destination_name_ko}, Destination name: {destination_name}, Destination description: {destination_description}, Destination sentiment score: {sentiment_score}, Destination review counts: {review_counts}, Destination type: {destination_type}"
            },
            {
                "role": "system",
                "content": f"Based on this information, could you recommend a tourist attraction to the customer? If the customer's requirements is in Korean, please respond in Korean."
            }
        ]
        reason_response = openai.ChatCompletion.create(model="gpt-4", messages=prompt_reason, max_tokens=150, temperature=0.6)
        reason = reason_response.choices[0].message['content']
        recommendation_reasons.append(reason)

    # 추천 정보 생성
    destination_recommendations = []
    for i, (score, image_link, destination_name) in enumerate(top_3_destinations):
        recommendation = {
            'Rank': i + 1,
            'Score(적합도 점수)': score,
            'Recommendation reason(추천 이유)': recommendation_reasons[i],
            '행정구': travel_data.loc[travel_data['여행지명'] == destination_name, '행정구'].values[0],
            'image link': image_link,

            'Tourist destination': destination_name,
            'Destination description': destination_description,
            'Destination Type': travel_data.loc[travel_data['여행지명'] == destination_name, '유형'].values[0],
            'Destination Sentiment Score': travel_data.loc[travel_data['여행지명'] == destination_name, '감성점수'].values[0],
            'Destination Review Counts': int(travel_data.loc[travel_data['여행지명'] == destination_name, '총 리뷰 수'].values[0]),
            'Address': travel_data.loc[travel_data['여행지명'] == destination_name, '주소'].values[0],
            'Detailed Directions': travel_data.loc[travel_data['여행지명'] == destination_name, '찾아오는 길'].values[0],
            'Opening hours': travel_data.loc[travel_data['여행지명'] == destination_name, '개장시간'].values[0],
            'Days off': travel_data.loc[travel_data['여행지명'] == destination_name, '휴무일'].values[0],
            'Operating hours': travel_data.loc[travel_data['여행지명'] == destination_name, '이용 시간'].values[0],
            'Parking availability': travel_data.loc[travel_data['여행지명'] == destination_name, '주차장 유무_ko'].values[0],
            'Stroller rental': travel_data.loc[travel_data['여행지명'] == destination_name, '유모차 대여'].values[0],
            'Pets allowed': travel_data.loc[travel_data['여행지명'] == destination_name, '애완동물 동반'].values[0],
            'Detailed information': travel_data.loc[travel_data['여행지명'] == destination_name, '상세정보'].values[0],
            'Parking fee': travel_data.loc[travel_data['여행지명'] == destination_name, '주차요금'].values[0],
            'Usage fee': travel_data.loc[travel_data['여행지명'] == destination_name, '이용료'].values[0],
            'Discount information': travel_data.loc[travel_data['여행지명'] == destination_name, '할인정보'].values[0],


            '여행지': travel_data.loc[travel_data['여행지명'] == destination_name, '여행지명_ko'].values[0],
            '여행지 설명': travel_data.loc[travel_data['여행지명'] == destination_name, '여행지 설명_ko'].values[0],
            '카테고리': travel_data.loc[travel_data['여행지명'] == destination_name, '유형_ko'].values[0],
            '여행지 감성 점수': travel_data.loc[travel_data['여행지명'] == destination_name, '감성점수'].values[0],
            '여행지 리뷰 수': int(travel_data.loc[travel_data['여행지명'] == destination_name, '총 리뷰 수'].values[0]),
            '주소': travel_data.loc[travel_data['여행지명'] == destination_name, '주소_ko'].values[0],
            '찾아오는 길': travel_data.loc[travel_data['여행지명'] == destination_name, '찾아오는 길_ko'].values[0],
            '개장시간': travel_data.loc[travel_data['여행지명'] == destination_name, '개장시간_ko'].values[0],
            '휴무일': travel_data.loc[travel_data['여행지명'] == destination_name, '휴무일_ko'].values[0],
            '이용 시간': travel_data.loc[travel_data['여행지명'] == destination_name, '이용 시간_ko'].values[0],
            '주차장 유무': travel_data.loc[travel_data['여행지명'] == destination_name, '주차장 유무_ko'].values[0],
            '유모차 대여': travel_data.loc[travel_data['여행지명'] == destination_name, '유모차 대여_ko'].values[0],
            '애완동물 동반': travel_data.loc[travel_data['여행지명'] == destination_name, '애완동물 동반_ko'].values[0],
            '상세정보': travel_data.loc[travel_data['여행지명'] == destination_name, '상세정보_ko'].values[0],
            '주차요금': travel_data.loc[travel_data['여행지명'] == destination_name, '주차요금_ko'].values[0],
            '이용료': travel_data.loc[travel_data['여행지명'] == destination_name, '이용료_ko'].values[0],
            '할인정보': travel_data.loc[travel_data['여행지명'] == destination_name, '할인정보_ko'].values[0]
        }
        destination_recommendations.append(recommendation)

    return destination_recommendations, destination_scores


####################################################################################################################################################

# 호텔 적합도 평가 함수
def get_hotel_score(age, gender, companion, requirements, travel_period, hotel_name, hotel_description, Hotel_Image_Link, sentiment_score, star_rating, hotel_ratings, review_counts, offset=0):
    prompt = f"""
    Customer's age: {age},
    Customer's gender: {gender},
    Customer's Companion: {companion},
    Customer's requirements: {requirements},
    Travel Period: {travel_period},
    Hotel name: {hotel_name},
    Hotel Description: {hotel_description},
    Hotel Review Sentiment Score: {sentiment_score},
    Hotel Star Rating: {star_rating},
    Hotel Ratings: {hotel_ratings},
    Hotel Review Counts: {review_counts}

    Based on this information, rate the suitability of the customer and Hotel as an integer from 1 to 10.
    """

    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=10)
    try:
        score = int(response.choices[0].text.strip())
    except ValueError:
        score = 0

    return score, Hotel_Image_Link, hotel_name

# 호텔 추천 함수
def recommend_hotel(age, gender, companion, requirements, travel_period, accommodations_data, offset=0):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Prepare arguments for get_hotel_score
        args = [(age, gender, companion, requirements, travel_period, row['Hotel_Name'], row['Hotel_Description'], row['Hotel_Image_Link'], row['Hotel_Sentiment_Score'], row['Star_rating'], row['Hotel_Ratings'], row['Hotel_Review_Counts']) for _, row in accommodations_data.iterrows()]
        # Use map function to execute the function in parallel
        hotel_scores = list(executor.map(lambda x: get_hotel_score(*x), args))

    # 점수 내림차순으로 정렬
    hotel_scores.sort(key=lambda x: x[0], reverse=True)

    # 상위 3개 호텔 선택
    top_3_hotels = hotel_scores[offset:offset+3]

    # 추천 이유 생성
    recommendation_reasons = []
    for score, image_link, hotel_name in top_3_hotels:
        hotel_description = accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Description'].values[0]  # 호텔 설명 추출
        sentiment_score = accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Sentiment_Score'].values[0]  # 호텔 감성 점수 추출
        Hotel_Name_ko = accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Name_ko'].values[0]  # 한국어 호텔명 추출
        star_rating = accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Star_rating'].values[0]  # 호텔 등급 추출
        hotel_ratings = accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Ratings'].values[0]  # 호텔 평점 추출
        review_counts = accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Review_Counts'].values[0]  # 호텔 리뷰 수 추출
        prompt_reason = [
            {
                "role": "system",
                "content": "You are a hotel expert"
            },
            {
                "role": "user",
                "content": f"Customer's age: {age}, Customer's gender: {gender},  Customer's Companion: {companion}, Customer's requirements: {requirements}, Travel Period: {travel_period}, 호텔명: {Hotel_Name_ko}, Hotel name: {hotel_name}, Hotel description: {hotel_description}, Hotel Review Sentiment Score: {sentiment_score}, Hotel Star Rating: {star_rating}, Hotel Ratings: {hotel_ratings}, Hotel Review Counts: {review_counts}"
            },
            {
                "role": "system",
                "content": f"Based on this information, could you recommend a hotel to the customer? If the customer's requirements is in Korean, please respond in Korean."
            }
        ]
        reason_response = openai.ChatCompletion.create(model="gpt-4", messages=prompt_reason, max_tokens=150, temperature=0.6)
        reason = reason_response.choices[0].message['content']
        recommendation_reasons.append(reason)

    # 추천 정보 생성
    hotel_recommendations = []
    for i, (score, image_link, hotel_name) in enumerate(top_3_hotels):
        recommendation = {
            'Rank': i + 1,
            'Score(적합도 점수)': score,
            'Recommendation reason(추천 이유)': recommendation_reasons[i],
            '행정구': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, '행정구'].values[0],
            'image link': image_link,

            'Hotel Name': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Name'].values[0],
            'Hotel Description': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Description'].values[0],
            'Hotel Sentiment Score': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Sentiment_Score'].values[0],
            'Star rating': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Star_rating'].values[0],
            'Hotel Ratings': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Ratings'].values[0],
            'Hotel Review Counts': int(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Review_Counts'].values[0]),
            'Hotel address': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_address'].values[0],
            'Hotel Directions': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Directions'].values[0],

            '호텔명': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Name_ko'].values[0],
            '호텔 소개': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Description_ko'].values[0],
            '호텔 감성 점수': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Sentiment_Score'].values[0],
            '호텔 등급': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Star_rating_ko'].values[0],
            '호텔 점수': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Ratings_ko'].values[0],
            '호텔 리뷰 수': int(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Review_Counts'].values[0]),
            '주소': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_address_ko'].values[0],
            '찾아오는 길': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Directions_ko'].values[0],
        }
        hotel_recommendations.append(recommendation)

    return hotel_recommendations, hotel_scores


if __name__ == '__main__':
    app.run(debug=True)


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
openai.api_key = ""

app = Flask(__name__)
CORS(app)

travel_data = pd.read_excel('관광지_en.xlsx')
restaurant_data = pd.read_excel('음식점_en.xlsx')
accommodations_data = pd.read_excel('관광숙박업_en.xlsx')

@app.route('/', methods=['GET'])
def test():
    print("test")
    return jsonify(message='Hello from path!')

@app.route('/init', methods=['POST'])
def initial_recommend():
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
    if choice == '맛집':
        return initial_recommend_restaurant(age,gender,companion,requirements,travel_period,restaurant_data)
    elif choice == '관광지':
        return initial_recommend_destination(age,gender,companion,requirements,travel_period,travel_data)
    else:
        return initial_recommend_hotel(age,gender,companion,requirements,travel_period,accommodations_data)

@app.route('/filter', methods=['POST'])
def filter_recommend():
    place = request.args.get('place')
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
    if choice == '맛집':
        return filter_and_recommend_restaurant(place,age,gender,companion,requirements,travel_period,restaurant_data)
    elif choice == '관광지':
        return filter_and_recommend_destination(place,age,gender,companion,requirements,travel_period,travel_data)
    else:
        return filter_and_recommend_hotel(place,age,gender,companion,requirements,travel_period,accommodations_data)
# 초기 맛집 추천
def initial_recommend_restaurant(age, gender, companion, requirements, travel_period, restaurant_data):
    print('초기 맛집')
    recommendations, restaurant_scores = recommend_restaurant(age, gender, companion, requirements, travel_period, restaurant_data)

    return json.dumps(recommendations, ensure_ascii=False)
# 행정구별 맛집 추천
def filter_and_recommend_restaurant(place, age, gender, companion, requirements, travel_period, restaurant_data):
    filtered_data = restaurant_data[restaurant_data['행정구'] == place]
    if len(filtered_data) < 3:
        filtered_data = restaurant_data
    recommendations, restaurant_scores = recommend_restaurant(age, gender, companion, requirements, travel_period, filtered_data)
    return json.dumps(recommendations, ensure_ascii=False)

# 초기 숙소 추천
def initial_recommend_hotel(age, gender, companion, requirements, travel_period, accommodations_data):
    recommendations, scores = recommend_hotel(age, gender, companion, requirements, travel_period, accommodations_data)
    print('초기 숙소')
    return json.dumps(recommendations, ensure_ascii=False)

# 행정구별 숙소 추천
def filter_and_recommend_hotel(place, age, gender, companion, requirements, travel_period, accommodations_data):
    filtered_data = accommodations_data[accommodations_data['행정구'] == place]
    if len(filtered_data) < 3:
        filtered_data = accommodations_data
    recommendations, scores = recommend_hotel(age, gender, companion, requirements, travel_period, filtered_data)
    return json.dumps(recommendations, ensure_ascii=False)

# 초기 관광지 추천
def initial_recommend_destination(age, gender, companion, requirements, travel_period, travel_data):
    recommendations, scores = recommend_destination(age, gender, companion, requirements, travel_period, travel_data)
    print("초기 관광지")

    return json.dumps(recommendations, ensure_ascii=False)

# 행정구별 관광지 추천
def filter_and_recommend_destination(place, age, gender, companion, requirements, travel_period, travel_data):
    filtered_data = travel_data[travel_data['행정구'] == place]
    if len(filtered_data) < 3:
        filtered_data = travel_data
    recommendations, scores = recommend_destination(age, gender, companion, requirements, travel_period, filtered_data)
    return json.dumps(recommendations, ensure_ascii=False)

# # 초기 맛집 추천
# def initial_recommend_restaurant(age, gender, companion, requirements, travel_period, restaurant_data):
#     print("초기 맛집 추천")
#     recommendations = recommend_restaurant(age, gender, companion, requirements, travel_period, restaurant_data)
#     return json.dumps(recommendations, ensure_ascii=False)
#
# # 초기 관광지 추천
# def initial_recommend_destination(age, gender, companion, requirements, travel_period, travel_data):
#     print("초기 관광지 추천")
#     recommendations, scores = recommend_destination(age, gender, companion, requirements, travel_period, travel_data)
#     return json.dumps(recommendations, ensure_ascii=False)
#
# # 초기 숙소 추천
# def initial_recommend_hotel(age, gender, companion, requirements, travel_period, accommodations_data):
#     print("초기 숙소 추천")
#     recommendations, scores = recommend_hotel(age, gender, companion, requirements, travel_period, accommodations_data)
#     return json.dumps(recommendations, ensure_ascii=False)
#
# # 행정구별 맛집 추천
# def filter_and_recommend_restaurant(selected_data, age, gender, companion, requirements, travel_period, restaurant_data):
#     filtered_data = restaurant_data[restaurant_data['행정구'] == selected_data['행정구']]
#     if len(filtered_data) < 3:
#         filtered_data = restaurant_data
#     recommendations = recommend_restaurant(age, gender, companion, requirements, travel_period, filtered_data)
#     return recommendations
#
#
# # 행정구별 관광지 추천
# def filter_and_recommend_destination(selected_data, age, gender, companion, requirements, travel_period, travel_data):
#     filtered_data = travel_data[travel_data['행정구'] == selected_data['행정구']]
#     if len(filtered_data) < 3:
#         filtered_data = travel_data
#     recommendations, scores = recommend_destination(age, gender, companion, requirements, travel_period, filtered_data)
#     return recommendations
#
#
# # 행정구별 숙소 추천
# def filter_and_recommend_hotel(selected_data, age, gender, companion, requirements, travel_period, accommodations_data):
#     filtered_data = accommodations_data[accommodations_data['행정구'] == selected_data['행정구']]
#     if len(filtered_data) < 3:
#         filtered_data = accommodations_data
#     recommendations, scores = recommend_hotel(age, gender, companion, requirements, travel_period, filtered_data)
#     return recommendations

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
        print(restaurant_name)
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
        restaurant_description = restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Description'].values[0]  # 음식점 설명 추출
        recommendation = {
            'Rank': i + 1,
            'Score': score,
            'Recommendation_reason': recommendation_reasons[i],
            '행정구': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, '행정구'].values[0],
            'image_link': image_link,


            'Restaurant': restaurant_name,
            # 'Restaurant_Description': restaurant_description,
            'Restaurant_Description': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Description'].values[0],
            'Restaurant_Review_Sentiment_Score': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Review_Sentiment_Score'].values[0],
            'Restaurant_Review_Counts': int(restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Review_Counts'].values[0]),
            'Restaurant_Type': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Type'].values[0],
            'Address': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, '주소'].values[0],
            'Detailed_Directions': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Detailed_Directions'].values[0],

            # '레스토랑명': restaurant_name_ko,
            # '음식점_설명': restaurant_description_ko,
            '레스토랑명': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_name_ko'].values[0],
            '음식점_설명': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Description_ko'].values[0],

            '리뷰_감성점수': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Review_Sentiment_Score'].values[0],
            '리뷰_수': int(restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Review_Counts'].values[0]),
            '가게_카테고리': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Type_ko'].values[0],
            '주소': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, '주소_ko'].values[0],
            '찾아오는_길': restaurant_data.loc[restaurant_data['Restaurant_name'] == restaurant_name, 'Restaurant_Detailed_Directions_ko'].values[0]



        }
        # NaN 제거하는 코드
        if pd.isna(recommendation.get("Detailed_Directions")):
            print(recommendation.get("Detailed_Directions"))
            recommendation['Detailed_Directions'] = ''
        if pd.isna(recommendation.get('찾아오는_길')):
            recommendation['찾아오는_길'] = ''

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
def recommend_destination(age, gender, companion, requirements, travel_period, travel_data):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Prepare arguments for get_destination_score
        args = [(age, gender, companion, requirements, travel_period, row['여행지명'], row['여행지_설명'], row['이미지링크'], row['감성점수'], row['총_리뷰_수'], row['유형']) for _, row in travel_data.iterrows()]
        # Use map function to execute the function in parallel
        destination_scores = list(executor.map(lambda x: get_destination_score(*x), args))

    # 점수 내림차순으로 정렬
    destination_scores.sort(key=lambda x: x[0], reverse=True)

    # 상위 3개 여행지 선택
    top_3_destinations = destination_scores[:3]

    # 추천 이유 생성
    recommendation_reasons = []
    for score, image_link, destination_name in top_3_destinations:
        destination_description = travel_data.loc[travel_data['여행지명'] == destination_name, '여행지_설명'].values[0]  # 여행지_설명 추출
        destination_name_ko = travel_data.loc[travel_data['여행지명'] == destination_name, '여행지명_ko'].values[0]  # 한국어 여행지 이름 추출
        sentiment_score = travel_data.loc[travel_data['여행지명'] == destination_name, '감성점수'].values[0]  # 여행지 감성 점수 추출
        review_counts = travel_data.loc[travel_data['여행지명'] == destination_name, '총_리뷰_수'].values[0]  # 여행지 리뷰 수 추출
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
                "content": f"Based on this information, could you recommend a tourist attraction to the customer? If the customer's requirements are in Korean, please respond in Korean."
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
            'Score': score if pd.notna(score) else None,
            'Recommendation_reason': recommendation_reasons[i],
            '행정구': travel_data.loc[travel_data['여행지명'] == destination_name, '행정구'].values[0],
            'image_link': image_link if pd.notna(image_link) else None,

            'Tourist_destination': destination_name if pd.notna(destination_name) else None,
            'Destination_description': destination_description if pd.notna(destination_description) else None,
            'Destination_Type': travel_data.loc[travel_data['여행지명'] == destination_name, '유형'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '유형'].values[0]) else None,
            'Destination_Sentiment_Score': sentiment_score if pd.notna(sentiment_score) else None,
            'Destination_Review_Counts': int(review_counts) if pd.notna(review_counts) else None,
            'Address': travel_data.loc[travel_data['여행지명'] == destination_name, '주소'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '주소'].values[0]) else None,
            'Detailed_Directions': travel_data.loc[travel_data['여행지명'] == destination_name, '찾아오는_길'].values[0] if '찾아오는_길' in travel_data.columns and pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '찾아오는_길'].values[0]) else None,
            'Opening_hours': travel_data.loc[travel_data['여행지명'] == destination_name, '개장시간'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '개장시간'].values[0]) else None,
            'Days_off': travel_data.loc[travel_data['여행지명'] == destination_name, '휴무일'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '휴무일'].values[0]) else None,
            'Operating_hours': travel_data.loc[travel_data['여행지명'] == destination_name, '이용_시간'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '이용_시간'].values[0]) else None,
            'Parking_availability': travel_data.loc[travel_data['여행지명'] == destination_name, '주차장_유무_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '주차장_유무_ko'].values[0]) else None,
            'Stroller_rental': travel_data.loc[travel_data['여행지명'] == destination_name, '유모차_대여'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '유모차_대여'].values[0]) else None,
            'Pets_allowed': travel_data.loc[travel_data['여행지명'] == destination_name, '애완동물_동반'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '애완동물_동반'].values[0]) else None,
            'Detailed_information': travel_data.loc[travel_data['여행지명'] == destination_name, '상세정보'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '상세정보'].values[0]) else None,
            'Parking_fee': travel_data.loc[travel_data['여행지명'] == destination_name, '주차요금'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '주차요금'].values[0]) else None,
            'Usage_fee': travel_data.loc[travel_data['여행지명'] == destination_name, '이용료'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '이용료'].values[0]) else None,
            'Discount_information': travel_data.loc[travel_data['여행지명'] == destination_name, '할인정보'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '할인정보'].values[0]) else None,


            '여행지': travel_data.loc[travel_data['여행지명'] == destination_name, '여행지명_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '여행지명_ko'].values[0]) else None,
            '여행지_설명': travel_data.loc[travel_data['여행지명'] == destination_name, '여행지_설명_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '여행지_설명_ko'].values[0]) else None,
            '카테고리': travel_data.loc[travel_data['여행지명'] == destination_name, '유형_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '유형_ko'].values[0]) else None,
            '여행지_감성_점수': sentiment_score if pd.notna(sentiment_score) else None,
            '여행지_리뷰_수': int(review_counts) if pd.notna(review_counts) else None,
            '주소': travel_data.loc[travel_data['여행지명'] == destination_name, '주소_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '주소_ko'].values[0]) else None,
            '찾아오는_길': travel_data.loc[travel_data['여행지명'] == destination_name, '찾아오는_길_ko'].values[0] if '찾아오는_길_ko' in travel_data.columns and pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '찾아오는_길_ko'].values[0]) else None,
            '개장시간': travel_data.loc[travel_data['여행지명'] == destination_name, '개장시간_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '개장시간_ko'].values[0]) else None,
            '휴무일': travel_data.loc[travel_data['여행지명'] == destination_name, '휴무일_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '휴무일_ko'].values[0]) else None,
            '이용_시간': travel_data.loc[travel_data['여행지명'] == destination_name, '이용_시간_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '이용_시간_ko'].values[0]) else None,
            '주차장_유무': travel_data.loc[travel_data['여행지명'] == destination_name, '주차장_유무_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '주차장_유무_ko'].values[0]) else None,
            '유모차_대여': travel_data.loc[travel_data['여행지명'] == destination_name, '유모차_대여_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '유모차_대여_ko'].values[0]) else None,
            '애완동물_동반': travel_data.loc[travel_data['여행지명'] == destination_name, '애완동물_동반_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '애완동물_동반_ko'].values[0]) else None,
            '상세정보': travel_data.loc[travel_data['여행지명'] == destination_name, '상세정보_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '상세정보_ko'].values[0]) else None,
            '주차요금': travel_data.loc[travel_data['여행지명'] == destination_name, '주차요금_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '주차요금_ko'].values[0]) else None,
            '이용료': travel_data.loc[travel_data['여행지명'] == destination_name, '이용료_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '이용료_ko'].values[0]) else None,
            '할인정보': travel_data.loc[travel_data['여행지명'] == destination_name, '할인정보_ko'].values[0] if pd.notna(travel_data.loc[travel_data['여행지명'] == destination_name, '할인정보_ko'].values[0]) else None
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
def recommend_hotel(age, gender, companion, requirements, travel_period, accommodations_data):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Prepare arguments for get_hotel_score

        print(accommodations_data.iterrows())
        args = [(age, gender, companion, requirements, travel_period, row['Hotel_Name'], row['Hotel_Description'], row['Hotel_Image_Link'], row['Hotel_Sentiment_Score'], row['Star_rating'], row['Hotel_Ratings'], row['Hotel_Review_Counts']) for _, row in accommodations_data.iterrows()]
        # Use map function to execute the function in parallel
        print("hello2222")
        hotel_scores = list(executor.map(lambda x: get_hotel_score(*x), args))

    # 점수 내림차순으로 정렬
    hotel_scores.sort(key=lambda x: x[0], reverse=True)

    # 상위 3개 호텔 선택
    top_3_hotels = hotel_scores[:3]

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
            'Score': score if pd.notna(score) else None,
            'Recommendation_reason': recommendation_reasons[i] if pd.notna(recommendation_reasons[i]) else None,
            '행정구': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, '행정구'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, '행정구'].values[0]) else None,
            'image_link': image_link if pd.notna(image_link) else None,

            'Hotel_Name': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Name'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Name'].values[0]) else None,
            'Hotel_Description': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Description'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Description'].values[0]) else None,
            'Hotel_Sentiment Score': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Sentiment_Score'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Sentiment_Score'].values[0]) else None,
            'Star_rating': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Star_rating'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Star_rating'].values[0]) else None,
            'Hotel_Ratings': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Ratings'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Ratings'].values[0]) else None,
            'Hotel_Review_Counts': int(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Review_Counts'].values[0]) if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Review_Counts'].values[0]) else None,
            'Hotel_address': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_address'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_address'].values[0]) else None,
            'Hotel_Directions': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Directions'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Directions'].values[0]) else None,

            '호텔명': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Name_ko'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Name_ko'].values[0]) else None,
            '호텔_소개': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Description_ko'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Description_ko'].values[0]) else None,
            '호텔_감성_점수': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Sentiment_Score'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Sentiment_Score'].values[0]) else None,
            '호텔_등급': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Star_rating_ko'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Star_rating_ko'].values[0]) else None,
            '호텔_점수': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Ratings_ko'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Ratings_ko'].values[0]) else None,
            '호텔_리뷰_수': int(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Review_Counts'].values[0]) if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Review_Counts'].values[0]) else None,
            '주소': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_address_ko'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_address_ko'].values[0]) else None,
            '찾아오는_길': accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Directions_ko'].values[0] if pd.notna(accommodations_data.loc[accommodations_data['Hotel_Name'] == hotel_name, 'Hotel_Directions_ko'].values[0]) else None,
        }
        hotel_recommendations.append(recommendation)

    return hotel_recommendations, hotel_scores
if __name__ == '__main__':
    app.run(debug=True)

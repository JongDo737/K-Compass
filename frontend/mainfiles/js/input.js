var questionNum = 0;
var question = '언어를 선택해 주세요.';
var number = document.querySelector('.number');
var output = document.getElementById('output');
typeWriter(question,0)

var nationality = '';
var choice = '';
var age = '';
var gender = '';
var companion = '';
var requirements = '';
var period = '';
var input = '';

const btnContainer = document.querySelector('.btnContainer');
var btnHTML = `
            <button class="btn"><span>🇰🇷</span> 한국어</button>
            <button class="btn"><span>🇺🇸</span> English</button>
        `;
 // Insert the HTML code into the container
 btnContainer.innerHTML = btnHTML;
 var btns = document.querySelectorAll('.btn');
 btnCheck();

function bot() {

    number.innerHTML = questionNum+2;
    if (questionNum == 0) {
        question = '여행에서 가장 중요한게 무엇인가요?';
        var btnHTML = `
            <button class="btn">🍱 맛집</button>
            <button class="btn">🌉 관광지</button>
            <button class="btn">🏨 숙소</button>
        `;
        btnContainer.innerHTML = btnHTML;
        btnCheck();
        timedQuestion();
    } else if (questionNum == 1) {
        question = '나이를 입력해주세요';
        var btnHTML = `
            <button class="btn">🍱 10대</button>
            <button class="btn">🌉 20대</button>
            <button class="btn">🏨 30대</button>
        `;
        btnContainer.innerHTML = btnHTML;
        btnCheck();
        timedQuestion();
    } else if (questionNum == 2) {
        question = '성별을 입력해주세요';
        var btnHTML = `
        <button class="btn">🙋🏼‍♂️ 남자</button>
        <button class="btn">💁🏼‍♀️ 여자</button>
        `;
        btnContainer.innerHTML = btnHTML;
        btnCheck();
        timedQuestion();
    } else if (questionNum == 3) {
        question = '동행자가 있으신가요? (있음, 없음)';
        var btnHTML = `
        <button class="btn">🧍🏻 나홀로여행</button>
        <button class="btn">👫 동행자있음</button>
        `;
        btnContainer.innerHTML = btnHTML;
        btnCheck();
        timedQuestion();
    } else if (questionNum == 4) {
        question = '여행에 필요한 조건이 있으신가요?';
        var btnHTML = `
        <button class="btn">🧖🏻‍♀️ 에어컨주의</button>
        `;
        btnContainer.innerHTML = btnHTML;
        btnCheck();
        timedQuestion();
    } else if (questionNum == 5) {
        question = '마지막으로 여행 기간을 입력해주세요';
        var btnHTML = `
        <button class="btn">🍱 7일</button>
        <button class="btn">🌉 1박2일</button>
        <button class="btn">🏨 4박5일</button>
        `;
        btnContainer.innerHTML = btnHTML;
        btnCheck();
        timedQuestion();
    } else if (questionNum == 6) {
        question = '여행지 추천 결과가 나왔습니다!';
        btnCheck();
    }
}

function typeWriter(text, i) {
    if (i < text.length) {
        output.innerHTML += text.charAt(i);
        i++;
        setTimeout(function () {
            typeWriter(text, i);
        }, 50); 
    }
}

function timedQuestion() {
    output.innerHTML = '';
    typeWriter(question, 0);
}
function print(){
  var message = "Nationality: " + nationality + "\n" +
              "Choice: " + choice + "\n" +
              "Age: " + age + "\n" +
              "Gender: " + gender + "\n" +
              "Companion: " + companion + "\n" +
              "Requirements: " + requirements + "\n" +
              "Period: " + period;

  alert(message);
  restaurantLoad();
  // AJAX request to send data to the Flask route

}


function restaurantLoad() {

  const url = `http://127.0.0.1:5000/init/restaurant?age=${age}&gender=${gender}&companion=${companion}&requirements=${requirements}&travel_period=${period}`;


  $.ajax({
    type: "POST",
    url: `${url}`,
    crossDomain: true,
    dataType: 'text',
    contentType: 'plain',
    async:false,
    success: function (data) {
			let forumsListObj = JSON.parse(data);
      alert(forumsListObj);
    },
    error: function () {
      alert('비동기 처리 오류');
    } 
    });
}

$(document).keypress(function (e) {
    if (e.which == 13) {
        bot();
        questionNum++;
    }
});
function btnCheck() {
  btns = document.querySelectorAll('.btn');

  for(let i=0; i< btns.length;i ++) {
    btns[i].onclick = () => {
      input = btns[i].textContent.split(' ');
      bot();
      questionNum++;
      alert(input[1]+questionNum);
      if(questionNum==1) {
        nationality = input[1];
      }
      else if(questionNum==2) {
        choice=input[1];
      }
      else if(questionNum==3) {
        age=input[1];
      }
      else if(questionNum==4) {
        gender=input[1];
      }
      else if(questionNum==5) {
        companion=input[1];
      }
      else if(questionNum==6) {
        requirements=input[1];
      }
      else if(questionNum==7) {
        period=input[1];
        print();
      }
    }
  } 
}
var questionNum = 0;
var question = '언어를 선택해 주세요.';
var number = document.querySelector('.number');
var output = document.getElementById('output');
const imgElement = document.querySelector('.bot');
const dateContainer = document.querySelector('.dateContainer');
const inputContainer = document.querySelector('.inputContainer');
localStorage.clear();
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
        imgElement.src = './mainfiles/img/ho5.png'; // New image source
        btnCheck();
        timedQuestion();
    } else if (questionNum == 1) {
        question = '나이를 입력해주세요';
        var btnHTML = `
            <button class="btn">😋 10대</button>
            <button class="btn">😎 20대</button>
            <button class="btn">🥳 30대</button>
            <button class="btn">🥸 중년층</button>
            <button class="btn">🤠 노년층</button>
        `;
        btnContainer.innerHTML = btnHTML;
        imgElement.src = './mainfiles/img/ho2.png'; // New image source
        btnCheck();
        timedQuestion();
    } else if (questionNum == 2) {
        question = '성별을 입력해주세요';
        var btnHTML = `
        <button class="btn">🙋🏼‍♂️ 남자</button>
        <button class="btn">💁🏼‍♀️ 여자</button>
        `;
        btnContainer.innerHTML = btnHTML;
        imgElement.src = './mainfiles/img/ho3.png'; // New image source
        btnCheck();
        timedQuestion();
    } else if (questionNum == 3) {
        question = '동행자가 있으신가요?';
        var btnHTML = `
        <button class="btn">🧍🏻 나홀로여행</button>
        <button class="btn">👯‍♂️ 친구와함께</button>
        <button class="btn">👫 애인과함께</button>
        <button class="btn">👨‍👩‍👧‍👦 가족과함께</button>
        `;
        btnContainer.innerHTML = btnHTML;
        imgElement.src = './mainfiles/img/ho4.png'; // New image source
        btnCheck();
        timedQuestion();
    } else if (questionNum == 4) {
        question = '여행에 필요한 조건이 있으신가요?';
        btnContainer.innerHTML = "";
        inputContainer.style.display = 'flex';
        imgElement.src = './mainfiles/img/ho5.png'; // New image source
        btnCheck();
        timedQuestion();
        
    } else if (questionNum == 5) {
        question = '마지막으로 여행 기간을 입력해주세요';
        btnContainer.innerHTML = "";
        inputContainer.style.display = 'none';
        dateContainer.style.display = 'flex';
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
  localStorage.setItem("nationality",nationality);
  localStorage.setItem("choice",choice);
  localStorage.setItem("age",age);
  localStorage.setItem("gender",gender);
  localStorage.setItem("companion",companion);
  localStorage.setItem("requirements",requirements);
  localStorage.setItem("period",period);
  location.href = '../mainfiles/loading2.html';
  // AJAX request to send data to the Flask route

}



function btnCheck() {
  btns = document.querySelectorAll('.btn');

  for(let i=0; i< btns.length;i ++) {
    btns[i].onclick = () => {
      input = btns[i].textContent.split(' ');
      bot();
      questionNum++;
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
        var require = document.querySelector('.requireInput').value;
        requirements=require;
      }
      else if(questionNum==7) {
        var start = document.querySelector('.start').value;
        var end = document.querySelector('.end').value;
        period=start+'~'+end;
        print();
      }
    }
  } 
}
var questionNum = 0;
var question = '언어를 선택해 주세요.';
var output = document.getElementById('output');
typeWriter(question,0)

var nationality = '';
var choice = '';
var age = '';
var gender = '';
var companion = '';
var requirements = '';
var period = '';

function bot() {
    var input = document.getElementById("input").value;
    console.log(input);

    if (questionNum == 0) {
        nationality = input;
        document.getElementById("input").value = "";
        question = '여행에서 가장 중요한게 무엇인가요? 맛집, 관광지, 숙소 중에 선택해 주세요 !';
        timedQuestion();
    } else if (questionNum == 1) {
        choice = input;
        document.getElementById("input").value = "";
        question = '나이를 입력해주세요';
        timedQuestion();
    } else if (questionNum == 2) {
        age = input;
        document.getElementById("input").value = "";
        question = '성별을 입력해주세요';
        timedQuestion();
    } else if (questionNum == 3) {
        gender = input;
        document.getElementById("input").value = "";
        question = '동행자가 있으신가요? (있음, 없음)';
        timedQuestion();
    } else if (questionNum == 4) {
        companion = input;
        document.getElementById("input").value = "";
        question = '여행에 필요한 조건이 있으신가요?';
        timedQuestion();
    } else if (questionNum == 5) {
        requirements = input;
        document.getElementById("input").value = "";
        question = '여행 기간을 입력해주세요';
        timedQuestion();
    } else if (questionNum == 6) {
        period = input;
        document.getElementById("input").value = "";
        question = '여행지 추천 결과가 나왔습니다!';
        print()
    }
}

function typeWriter(text, i) {
    if (i < text.length) {
        output.innerHTML += text.charAt(i);
        i++;
        setTimeout(function () {
            typeWriter(text, i);
        }, 100); 
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
}
$(document).keypress(function (e) {
    if (e.which == 13) {
        bot();
        questionNum++;
    }
});
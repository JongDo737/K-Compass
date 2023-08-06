const dataList = localStorage.getItem("dataList");
const imgList = localStorage.getItem("imgList");
const reasonList = localStorage.getItem("reasonList");
// 전달받은 데이터가 한글일 경우
// console.log(decodeURI(receivedData));
const img = document.querySelectorAll('.tte');
const title = document.querySelector('.loc_container_right_title');
const content = document.querySelector('.loc_container_right_content');

const btn = document.querySelector('.btn-two');

title.textContent = dataList;
content.textContent = reasonList;

for(let i=0; i<img.length; i++) {
    img[i].src = imgList;
}

btn.onclick = () => {
    location.href = `../card.html?${dataList}`
}











$(function () {
    $("body div").fadeIn(500, function () {
        $(this).animate({
            "top": "150px"
        },1000);
    });
    
    $("a").click(function () {
        var url = $(this).attr("href");
        $("body div").animate({
            "opacity": "0",
            "top": "10px"
        },500, function () {
            document.location.href = url;
        });
        
        return false;
    });
  });
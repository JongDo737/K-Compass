const receivedData = location.href.split('?')[1];
const search = decodeURI(receivedData);

const btn = document.querySelector('lastBtn');



const forumsList = document.querySelector('.foodlist');


const url = `http://127.0.0.1:5000/stores?destination=${search}`;


function restaurantLoad() {
  $.ajax({
    type: "POST",
    url: `${url}`,
    crossDomain: true,
    dataType: 'text',
    contentType: 'plain',
    timeout: 200000,
    success: function (data) {
      forumsItem = ``;
			let forumsListObj = JSON.parse(data);
			forumsItem += getForums(forumsListObj);
			forumsList.innerHTML = forumsItem;


    },
    error: function () {
      alert('비동기 처리 오류');
    } 
    });
  // alert(data);
  // let forumsItem = getForums(data);
  // alert(forumsItem);
  // forumsList.innerHTML = forumsItem;
}


function getForums(forumsList) {
  let forumsHtml = '';
  for (let pet of forumsList) {
    if (pet.naver_map_url === null) {
      pet.naver_map_url="#";
    }
    if (pet.Description=== null) {
      pet.Description="";
    }
   
  
    forumsHtml += `
      <div class="item" style="background-image: url(${pet.Image_Links});">
        <div class="item-desc">
          <div class="item-desc_title">
            <h3>${pet.name}</h3>
            <p>🍀 ${pet.Sentiment}/5</p>
            <label><input data-store='${JSON.stringify(pet)}' class="cb pristine" type="checkbox"> <span>저장하기</span></label>
            <a class="review" href="${pet.naver_map_url}">리뷰 ${pet.Review_Counts}개</a>
          </div>
          <p>${pet.Description}</p>
        </div>
      </div>
    `;
  }
  return forumsHtml;
}

restaurantLoad()

$(".custom-carousel").owlCarousel({
  autoWidth: true,
  loop: true
});
$(document).ready(function () {
  $(".custom-carousel .item").click(function () {

    $(".custom-carousel .item").not($(this)).removeClass("active");
    $(this).toggleClass("active");
  });
});
var id = 0;
var result = "";
$('input[type=checkbox].cb').on('change', function () {
  // 선택된 체크박스의 개수를 세어 3개 이상인지 확인합니다.
  if ($('input[type=checkbox].cb:checked').length > 3) {
    // 선택된 체크박스가 3개 이상인 경우 현재 선택한 체크박스를 해제하고 경고 메시지를 표시합니다.
    $(this).prop('checked', false);
    alert("최대 3개까지 선택할 수 있습니다.");
  } else {

    // 선택한 상점 데이터를 local storage에 저장하거나 제거합니다.
    var storeData = JSON.parse($(this).attr('data-store'));
    var storeId = "#"+storeData.name;
    
    
    if ($(this).is(':checked')) { // 체크박스가 선택되면 데이터를 저장합니다.
      localStorage.setItem(storeId, encodeURIComponent(JSON.stringify(storeData)));
    } else { // 체크박스가 해제되면 데이터를 삭제합니다.
      localStorage.removeItem(storeId);
    }
      result = newStr;
      alert(result);
    }
  
});

function btnClick() {
  localStorage.setItem("result", result);
  location.href = `../loading.html`
}
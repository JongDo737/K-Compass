
const decodedData = JSON.parse(decodeURIComponent(localStorage.getItem('encodedData')));
const test = document.querySelector('.text'); 
console.log(decodeURIComponent(localStorage.getItem('encodedData')));
alert(decodedData);
const list = document.querySelector('.card-grid');
var cardList;
var dataList = [];
var imgList = [];
var rateList = [];
var reasonList = [];


function showInfo() {
  forumsItem = ``;
  forumsItem += getForums(decodedData);
  list.innerHTML = forumsItem;
  
  cardList = document.querySelectorAll('.card');
  for(let i=0;i <cardList.length; i++) {
    cardList[i].onclick = () => {
      alert(dataList[i]+dataList.length);
    }
  }
}
function getForums(forumsList) {
	let forumsHtml = ``;
  let i = 0;
	for (let pet of forumsList) {
    alert(pet.레스토랑명 + i);
    dataList[i] = pet.Restaurant
		forumsHtml += `
      <a class="card" >
        <div class="card__background" style="background-image: url(${pet.image_link})"></div>
        <div class="card__content">
          <h3 class="card__heading">${pet.Restaurant}</h3>
        </div>
      </a>
		`;
    i++;
	}
	return forumsHtml;
}

showInfo();





$(function () {
  $("body div").fadeIn(500, function () {
      $(this).animate({
          "top": "00px"
      },1000);
  });
  
  $("a").click(function () {
      var url = $(this).attr("href");
      $("body div").animate({
          "opacity": "0",
          "top": "10px"
      },500, function () {
          // document.location.href = "../travel.html";
      });
      
      return false;
  });
});
var x;
var $cards = $(".card");
var $style = $(".hover");

$cards
  .on("mousemove touchmove", function(e) { 
    // normalise touch/mouse
    var pos = [e.offsetX,e.offsetY];
    e.preventDefault();
    if ( e.type === "touchmove" ) {
      pos = [ e.touches[0].clientX, e.touches[0].clientY ];
    }
    var $card = $(this);
    // math for mouse position
    var l = pos[0];
    var t = pos[1];
    var h = $card.height();
    var w = $card.width();
    var px = Math.abs(Math.floor(100 / w * l)-100);
    var py = Math.abs(Math.floor(100 / h * t)-100);
    var pa = (50-px)+(50-py);
    // math for gradient / background positions
    var lp = (50+(px - 50)/1.5);
    var tp = (50+(py - 50)/1.5);
    var px_spark = (50+(px - 50)/7);
    var py_spark = (50+(py - 50)/7);
    var p_opc = 20+(Math.abs(pa)*1.5);
    var ty = ((tp - 50)/2) * -1;
    var tx = ((lp - 50)/1.5) * .5;
    // css to apply for active card
    var grad_pos = `background-position: ${lp}% ${tp}%;`
    var sprk_pos = `background-position: ${px_spark}% ${py_spark}%;`
    var opc = `opacity: ${p_opc/100};`
    var tf = `transform: rotateX(${ty}deg) rotateY(${tx}deg)`
    // need to use a <style> tag for psuedo elements
    var style = `
      .card:hover:before { ${grad_pos} }  /* gradient */
      .card:hover:after { ${sprk_pos} ${opc} }   /* sparkles */ 
    `
    // set / apply css class and style
    $cards.removeClass("active");
    $card.removeClass("animated");
    $card.attr( "style", tf );
    $style.html(style);
    if ( e.type === "touchmove" ) {
      return false; 
    }
    clearTimeout(x);
  }).on("mouseout touchend touchcancel", function() {
    // remove css, apply custom animation on end
    var $card = $(this);
    $style.html("");
    $card.removeAttr("style");
    x = setTimeout(function() {
      $card.addClass("animated");
    },2500);
  });
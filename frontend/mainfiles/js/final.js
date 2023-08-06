
const dataList = localStorage.getItem("dataList");
const imgList = localStorage.getItem("imgList");
const reasonList = localStorage.getItem("reasonList");
const total = document.querySelector('.input-flex-container');
const locImg = document.querySelector('#input1 img');
const locText = document.querySelector('.text1');
const $spanElement = $('span[data-year]');
const main_title = document.querySelector('.main_title');
const textList = document.querySelector('.description-flex-container');
$spanElement.data('-year', dataList);
main_title.textContent = dataList;
var realKey = [];
var reasonshtml = `<p class="active text1">${reasonList}</p>`
var reasons = [];
var check = 1;
let forumsHtml = `<div class="input active" id="input1">
<img src="${imgList}" alt="">
<span data-year="${dataList}" ></span>
</div>`;
for (let i = 0; i < localStorage.length; i++) {
    let key = localStorage.key(i);
	
	if(key.charAt(0)=='#'){
		let item = JSON.parse(decodeURIComponent(localStorage.getItem(key)));
		reasons[check] = item.Description
		forumsHtml += `
		<div class="input" id="input${check}">
			<img src="${item.Image_Links}" alt="">
			<span data-year="${item.name}"></span>
		</div>
		`
		check++;
	}
  }

function inner() {
	total.innerHTML = forumsHtml;
}
inner()
for(let i=0; i<check-1; i++) {
	reasonshtml+= `<p class="active text2">${reasons[i]}</p>
	`
	
}
reasonshtml = reasonshtml.replace('undefined', "");
textList.innerHTML = reasonshtml;


$(function(){
	var inputs = $('.input');
	var paras = $('.description-flex-container').find('p');
	inputs.click(function(){
		var t = $(this),
				ind = t.index(),
				matchedPara = paras.eq(ind);
		
		t.add(matchedPara).addClass('active');
		inputs.not(t).add(paras.not(matchedPara)).removeClass('active');
	});
});

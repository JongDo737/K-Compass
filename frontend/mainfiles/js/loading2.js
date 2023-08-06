
const receivedData = location.href.split('?')[1];
var text = decodeURI(receivedData);

const url = `https://b80rsrw2rf.execute-api.us-east-1.amazonaws.com?user_id=111&user_request=${text}`;
$.ajax({
  type: "POST",
  url: `${url}`,
  crossDomain: true,
  dataType: 'text',
  contentType: 'plain',
  timeout: 200000,
  success: function (data) {
    var jdata = JSON.parse(data);
    var encodedData = encodeURIComponent(JSON.stringify(jdata));
    location.href = `../first.html?${encodedData}`;
    
  },
  error: function () {
    alert('비동기 처리 오류');
  } 
  });



var xmlns = "http://www.w3.org/2000/svg",
  xlinkns = "http://www.w3.org/1999/xlink",
  select = function(s) {
    return document.querySelector(s);
  },
  selectAll = function(s) {
    return document.querySelectorAll(s);
  },
  truckFlip = select('#truckFlip'),
  roadBlock = select('#roadBlock')

TweenMax.set('svg', {
  visibility: 'visible'
})
TweenMax.set('#truckSquash',{
  transformOrigin: '100% 130%'
})
var mainTl = new TimelineMax();

var roadSideTl = new TimelineMax({
  repeat: -1
});
roadSideTl.to('#roadMarkingSide', 0.5, {
  x: 0.5,
  y: -51,
  ease: Linear.easeNone
})

var roadTopTl = new TimelineMax({
  
});
roadTopTl.to('#roadMarkingTop', 0.5, {
  x: 68,
  y: -26,
  repeat: -1,
  ease: Linear.easeNone
})

var truckTl = new TimelineMax({
  repeat: -1
});
truckTl.to('#truck', 4, {
    x: '+=30',
    y: '+=25',
    ease: Power2.easeInOut
  })
  .to('#truck', 4, {
    x: '-=30',
    y: '-=25',
    delay: 1,
    ease: Power2.easeInOut
  })

var squashTl = new TimelineMax({
  repeat: -1
}).timeScale(3);
squashTl.to('#truckSquash', 1, {
    scaleY: 0.99,
    y: 1,
    scaleX: 1.01,
    
    ease: Sine.easeIn
  })
  .to('#truckSquash', 1, {
    scale: 1,
    y: 0,
    ease: Sine.easeOut
  })

mainTl.add(truckTl, 0)
mainTl.add(squashTl, 0)
mainTl.add(roadSideTl, 0.7)
mainTl.add(roadTopTl, 0)

mainTl.timeScale(2);

select('#hit').onclick = function(e) {
  //console.log(truckFlip._gsTransform)

  if (truckFlip._gsTransform.rotation != 0) {
    TweenMax.to([truckFlip, '#wholeThing'], 2, {
      //scale:1,
      rotation: 0,
      x: 0,
      y: 0,
      ease: Elastic.easeOut.config(0.6, 0.72)
    })
    TweenMax.fromTo(roadTopTl, 0.25, {
      time:0
    }, {
      time: 0.5,
      repeat: -1,
      ease: Linear.easeNone
    })    
   TweenMax.fromTo(roadSideTl, 0.25, {
      time:0
    }, {
      time: 0.5,
      repeat: -1,
      ease: Linear.easeNone
    })    

  } else {

    TweenMax.to(truckFlip, 2, {
      //scale:-1,
      rotation: 180,
      x: -20,
      y: -50,
      ease: Elastic.easeOut.config(0.6, 0.72)
    })
    TweenMax.to('#wholeThing', 2, {
      rotation: -180,
      transformOrigin: '50% 50%',
      ease: Elastic.easeOut.config(0.6, 0.72)
    })
    
    TweenMax.fromTo(roadTopTl, 0.25, {
      time:0.5
    }, {
      time: 0,
      repeat: -1,
      ease: Linear.easeNone
    })
  }
   TweenMax.fromTo(roadSideTl, 0.25, {
      time:0.5
    }, {
      time: 0,
      repeat: -1,
      ease: Linear.easeNone
    })
  

}

TweenMax.set(truckFlip, {
  rotation: 0,
  transformOrigin: '50% 50%',
  x: 0,
  y: 0
})

var isDevice = (/android|webos|iphone|ipad|ipod|blackberry/i.test(navigator.userAgent.toLowerCase()));
if (!isDevice) {
  select('#wholeRoad').setAttribute('filter', 'url(#edgeClean)');
  select('#truck').setAttribute('filter', 'url(#edgeClean)')
}
//ScrubGSAPTimeline(mainTl)

TweenMax.globalTimeScale(1);
mainTl.seek(100)

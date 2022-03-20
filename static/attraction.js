let id_number = location.href

//console.log(id_number.substring(33,100))
id_number = id_number.substring(33,100)



fetch(`http://3.87.217.170:3000/api/attractions/${id_number}`, {method: 'get'})
.then(response =>{
  return  response.json()
})

.then( data =>{
    let name = document.getElementById("name")
    name.innerHTML = data['data']['data']['name'] ; 
    let category = document.getElementById("category")
    category.innerHTML = data['data']['data']['category'] ;
    let mrt = document.getElementById("mrt")
    mrt.innerHTML = data['data']['data']['mrt'] ;
    let description = document.getElementById("description")
    description.innerHTML = data['data']['data']['description'] ;
    let address = document.getElementById("address")
    address.innerHTML = data['data']['data']['address'] ;
    let transport = document.getElementById("transport")
    transport.innerHTML = data['data']['data']['transport'] ;
    let j = 0 //抓取締一張圖片
    for(var i = 1 ; i<=3;i++){
        let push_img = document.getElementById("imgs"+[i])
        let show_img = document.createElement("img"); 
        show_img.src=data['data']['data']['images'][j];
        push_img.appendChild(show_img);
        j = j + 1 ;
    }


})


function morning(){
    let cost_h5 = document.getElementById("cost_h4");
    cost_h5.innerHTML = "新台幣2000"
}
function night(){
    let cost_h5 = document.getElementById("cost_h4");
    cost_h5.innerHTML = "新台幣2500"
}

document.addEventListener("DOMContentLoaded",function(){
    var dots = document.getElementsByClassName("dot");
    dots[slideIndex - 1].className += " active";
})
var slideIndex = 1;


// 展示上一张/下一
function plusSlides(n) {
  showSlides(slideIndex += n);
}
// 展示并记录指定位置的图片
function currentSlide(n) {
  showSlides(slideIndex = n);
}
// 展示指定位置的图片
function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {
    slideIndex = 1
  }
  if (n < 1) {
    slideIndex = slides.length
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}

window.onscroll=function(){

    let nav = document.getElementById("nav");//獲取到導航欄id
    nav.style.top = '0';
    nav.style.zIndex = '9999';
    nav.style.position = 'fixed';
    }
  
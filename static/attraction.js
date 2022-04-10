let id_number = location.href

//id_number.substring(33,100)//本機端
id_number = id_number.substring(36,100)//ec2

let booking_attractions = []


fetch(`http://3.87.217.170:3000/api/attractions/${id_number}`, {method: 'GET'})
.then(response =>{
  return  response.json()
})

.then( data =>{
    booking_attractions = data ;
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
function afternoon(){
    let cost_h5 = document.getElementById("cost_h4");
    cost_h5.innerHTML = "新台幣2500"
}

document.addEventListener("DOMContentLoaded",function(){
    let dots = document.getElementsByClassName("dot");
    dots[slideIndex - 1].className += " active";
    let choose_date = document.getElementById('date');
    new_date = new Date().toLocaleDateString();
    let output =[]
    if( new_date.length === 8){
      output=new_date.replace(/\//g, "-0");
    }
    if( new_date.length === 9){
        if(new_date.charAt(6) === '/'){
          output=new_date.replace(/\//, "-0");
        }
        else{
          output=new_date.replace(/\/{2}/, "-0");
        }
    }
    choose_date.min=output;
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


function start_booking_click(){
  let url = `http://3.87.217.170:3000/api/user`;
  fetch(url, {method:'GET'})
  .then(response =>{
    return  response.json()
  })
  .then( data =>{
    if(data['data']['id'] == null){
      login_click();
    }
    else{
      let coose_date = document.getElementById("date").value
      
      if(coose_date === ''){
          alert("請選擇日期")
          return
      }
      let radio_time = document.getElementsByTagName("INPUT");
      let choose_radio_time = []
      for (var i = 0; i < radio_time.length; i++) {
          if (radio_time[i].type == "radio") {
              if (radio_time[i].checked) {
                  choose_radio_time = radio_time[i].value
              }
          }
      }
      
      let pice = document.getElementById("cost_h4").textContent
      let booking_id = booking_attractions['data']['data']['id'];
      let booking_name = booking_attractions['data']['data']['name'];
      let booking_address = booking_attractions['data']['data']['address'];
      let booking_image = booking_attractions['data']['data']['images'][0];
      let url =`http://3.87.217.170:3000/api/booking`;
      let booking_data ={
        "attractionId": booking_id,
        "name":booking_name,
        "address":booking_address,
        "image":booking_image,
        "date": coose_date ,
        "time": choose_radio_time,
        "price": pice.substring(3,100)
      }
      fetch(url, 
      {
        method: 'POST',
        body:JSON.stringify(booking_data),  
        headers:{
        'Content-Type': 'application/json'
      }
      })
      .then(response =>{
        return  response.json()
      })
      .then( data =>{
        if(data['ok'] === true){
          document.location.href='http://3.87.217.170:3000/booking';
        }
     
      })
    }
  })
  
}

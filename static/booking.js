
document.addEventListener("DOMContentLoaded",function(){
  
    let url = ip_addres+`api/user`;
   
    fetch(url, {method:'GET'})
    .then(response =>{
      return  response.json()
    })
    .then( member_data =>{
      if(member_data['data']['id'] == null){
        document.location.href=ip_addres;
      }
      else{
        let url = ip_addres+`api/booking`;
        fetch(url, {method:'GET'})
        .then(response =>{
          return  response.json()
        })
        .then( data =>{
    
        if(data['data'] === null || data['data']['attraction']['id'] === '' ) {
     
          document.getElementById('member_name').innerHTML=member_data['data']['name'];
          document.getElementById('attraction_conten_layout').innerHTML="";
          document.getElementById('member_data').innerHTML="<h4>目前沒有任何待預訂的行程</h4>";
          document.getElementById('member_data').style.margin='0px';
          document.getElementById('pay').innerHTML="";
          document.getElementById('pay').style.margin='0px';
          document.getElementById('total').innerHTML="";
          document.getElementById('hr1').style.border="0px";
          document.getElementById('hr2').style.border="0px";
          document.getElementById('hr2').style.margin="0px";
          document.getElementById('hr3').style.border="0px";
          document.getElementById('hr3').style.margin="0px";
        }
        else{

          let member_name = document.getElementById('member_name');
          member_name.innerText= data['data']['member'];
          document.getElementById("attraction_show_img").src= data['data']['attraction']['image'];
          document.getElementById("input_name").value= data['data']['member'];
          document.getElementById("input_email").value = data['data']['email'];
          let booking_name = document.getElementById('booking_name');
          booking_name.innerText= data['data']['attraction']['name'];
          let booking_date = document.getElementById('booking_date');
          booking_date.innerHTML= data['data']['date'];
          let booking_time = document.getElementById('booking_time');
          booking_time.innerHTML= data['data']['time'];
          let booking_price = document.getElementById('booking_price');
          booking_price.innerHTML= data['data']['price'];
          let booking_address = document.getElementById('booking_address');
          booking_address.innerHTML= data['data']['attraction']['address'];
          let sum_booking_price = document.getElementById('sum_booking_price');
          sum_booking_price.innerHTML = "新台幣"+data['data']['price']+"元";
        }
        })
      }
    })
    
})


function delete_booking(){
  let url = ip_addres+`api/booking`;
  fetch(url, {method:'DELETE'})
  .then(response =>{
    return  response.json()
  })
  .then(data =>{

    if(data['ok'] === true){
      document.location.href=ip_addres+`booking`;
    }
  })
}

document.addEventListener("DOMContentLoaded",function(){
    let order_number = location.href;
    //order_number = order_number.substring(38,100);//本機端
    order_number = order_number.substring(41,100);//ec2
    if(order_number === ''){
        let in_size = document.getElementById('in_size')
        in_size.innerHTML="尚無訂單" ;
        in_size.style.fontSize = '19px';
        in_size.style.fontFamily = 'Noto Sans TC';
        in_size.style.color ='#666666';
        in_size.style.margin ='50px 0px'
    }
    let number = document.getElementById("number");
   
    number.innerText = order_number ;
   
   
})
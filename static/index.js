let start_data = [] ;
let page = [] ;
let start_time  = [] ;
let end_time = [] ;
let ip_addres = `http://3.87.217.170/`;
  document.addEventListener("DOMContentLoaded",function(){
    page = 0 ;
    fetch(ip_addres+`api/attractions?page=${page}`, {method: 'get'})
    .then(response =>{
      return  response.json()
    })
  
   .then( data =>{
    start_time = 0 ;
    end_time = 11 ;
    start_data = data ;
    show_img(start_time,end_time,data)
    
    setTimeout(function(){
      let spinner_size = document.getElementById("spinner_size")
      fadeOut(spinner_size,50);
      spinner_size.style.display='none'
      document.body.style.display = 'contents' ;
      
    },1000);

    window.addEventListener('scroll', function() {
        //文档内容实际高度（包括超出视窗的溢出部分）
        if(window.location.href !== ip_addres){
          return 
        }
        let scrollHeight =  document.documentElement.scrollHeight || document.body.scrollHeight;
        //console.log('scrollHeight',scrollHeight)
        //滚动条滚动距离
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
        //console.log('scrollTop',scrollTop)
        //窗口可视范围高度
        let clientHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
        //console.log('clientHeight',clientHeight)
        if(clientHeight + scrollTop+1 >= scrollHeight){
          let data_length = Object.values(start_data['data']).length
          if(data_length >= 13){
            page = page+1;
                if(keyword.value !=''){ 
  
                  fetch(ip_addres+`api/attractions?page=${page}&keyword=${keyword.value}`, {method: 'get'})
                  .then(response =>{
                    return  response.json()
                  })
                  .then( next_data =>{
                    
                    start_time = start_time + 12 ;
                    let next_data_length = Object.values(next_data['data']).length
                    start_data = next_data
                    if(next_data_length >= 13){
                      end_time  = end_time + 12;
                    }
                    else{
                      end_time = end_time+next_data_length
                    
                    }
                    show_img(start_time,end_time,next_data)
                    
                  })
           
                }
                else{
                fetch(ip_addres+`api/attractions?page=${page}`, {method: 'get'})
                .then(response =>{
                  return  response.json()
                })
                .then( next_data =>{
                  
                  start_time = start_time + 12 ;
                  let next_data_length = Object.values(next_data['data']).length
                  start_data = next_data
                  if(next_data_length >= 13){
                    end_time  = end_time + 12;
                  }
                  else{
                    end_time = end_time+next_data_length
                  
                  }
                  show_img(start_time,end_time,next_data)
                  
                })
         
              }
          }
          else{
            return ;
          }
        }
        
      })
        })
    fetch(ip_addres+`api/user`, {method: 'get'})
    .then(response =>{
      return  response.json()
    })
    .then( data =>{
      if(data['data']['email'] === null){
        let login = document.getElementById("login")
        let loginout = document.getElementById("loginout")
        login.style.display = "block";
        loginout.style.display = "none";
      }
      else{
        let dialog = document.getElementById("dialog")
        let login_dialog = document.getElementById("login_dialog")
        dialog.style.display="none";
        login_dialog.style.display="none";
        let login = document.getElementById("login")
        let loginout = document.getElementById("loginout")
        login.style.display = "none";
        loginout.style.display = "block";
        document.body.style.overflow = 'scroll' ;
  
      }
    })
  })
window.onscroll=function(){

  let header = document.getElementById("header");//獲取到導航欄id
  header.style.top = '0';
  header.style.zIndex = '10';
  header.style.position = 'fixed';
  let second = document.getElementById("second");
  second.style.margin = '63px 0px 0px';
  }


function select_click(){
  let keyword = document.getElementById("keyword");
  page = 0 
  if(keyword.value == '' ){
    no_data();
   
  }
  else{
        fetch(ip_addres+`api/attractions?page=${page}&keyword=${keyword.value}`, {method: 'get'})
        .then(response =>{
          return  response.json()
      })
      .then( select_click =>{
        start_data = select_click ;
        let keyword_length = Object.values(start_data['data']).length
        //console.log('keyword_length',keyword_length)
        let div_delet = document.getElementById("third");
        
        
        if(start_data['data']['error'] ==  true){
          no_data();
        }
        else{
          div_delet.innerHTML ="";
          if(keyword_length >=13){
            //console.log(keyword_length)
            start_time = 0 ;
            end_time = 11
            show_img(start_time,end_time,start_data)
           
          }
          else{
            show_img(1,keyword_length,start_data)
            
       
          }
        }
      })
      }
}


function show_img(start_time,end_time,data){

    let third = document.getElementById("third");
    let j = 0; //取單筆資料 根據回圈次數
    if(third === null){
      return ;
    }
    for(var i = start_time ; i<=end_time;i++){

      let all_data_div = document.createElement("div");
      all_data_div.class = "show_data";
      all_data_div.id = "show_data"+[i];
      third.appendChild(all_data_div);

      let a_herf = document.createElement("a");
      a_herf.href= ip_addres+`attraction/`+data['data'][j]['id'];
      a_herf.id = "a_herf"+[i];
            
      let show_data = document.getElementById("show_data"+[i])
      show_data.appendChild(a_herf);

      let a_herf_push = document.getElementById("a_herf"+[i])
      let show_img = document.createElement("img"); 
      show_img.src=data['data'][j]['images'][0];
      a_herf_push.appendChild(show_img);

      
      let third_p = document.createElement("p");
      third_p.className = "third_p";
      third_p.innerHTML = data['data'][j]['name'];
      a_herf_push.appendChild(third_p);

      let third_a_right = document.createElement("a");
      third_a_right.className = "third_a_right";
      third_a_right.innerHTML = data['data'][j]['category'];
      a_herf_push.appendChild(third_a_right);

      let third_a_left = document.createElement("a");
      third_a_left.className = "third_a_left";
      third_a_left.innerHTML = data['data'][j]['mrt'];
      a_herf_push.appendChild(third_a_left);
      j =j+1;
      }
}
 
function no_data(){
  let div_delet = document.getElementById("third");
  div_delet.innerHTML ="";
  let third_p = document.createElement("p");
  third_p.className = "third_p";
  third_p.innerHTML ="查無景點，請重新輸入"
  div_delet.appendChild(third_p);
}

function login_click(){
  let dialog = document.getElementById("dialog")
  dialog.style.display="flex";
  document.body.style.display ="block";
  document.body.style.overflow="hidden";
  document.body.style.margin="0px"
  let login_dialog_size = document.getElementById("login_dialog_size")

  fadeIn(login_dialog_size,50);
  login_dialog_size.style.height ="auto"
 

}
function close_login_dialog(){
  let login_dialog_size = document.getElementById("login_dialog_size")
  fadeOut(login_dialog_size,50);
  setTimeout(function(){
    let dialog = document.getElementById("dialog")
    dialog.style.display="none";
    document.body.style.display ="contents";
    document.body.style.overflow = 'scroll' ;
  },700);
  
}
//淡入淡出

function fadeIn(element,speed){
  if(element.style.opacity !=1){
      var speed = speed || 50 ;
      var num = 0;
      var st = setInterval(function(){
      num++;
      element.style.opacity = num/10;
      if(num>=10)  {  clearInterval(st);  }
      },speed);
  }
}

function fadeOut(element,speed){
  if(element.style.opacity !=0){
      var speed = speed || 50 ;
      var num = 10;
      var st = setInterval(function(){
      num--;
      element.style.opacity = num / 10 ;
      if(num<=0)  {   clearInterval(st);  }
      },speed);
  }

}



function new_member_click(){
  let login_dialog = document.getElementById("login_dialog")
  login_dialog.style.display="none";
  let new_member_dialog = document.getElementById("new_member_dialog")
  new_member_dialog.style.display="block";
  
}
function login_agin_click(){
  let login_dialog = document.getElementById("login_dialog")
  login_dialog.style.display="block";
  let new_member_dialog = document.getElementById("new_member_dialog")
  new_member_dialog.style.display="none";
}

function login_member_click(){
    let email = document.getElementById("member_email")
    let password = document.getElementById("member_password")
    let error_massage = document.getElementById("error_massage")

    if(IsEmail(email.value) === false){
      error_massage.style.display='block';
      error_massage.innerHTML = "信箱格式錯誤"
      
    }
    else if(email.value === "" || password.value === "" ){
      
      error_massage.style.display='block';
      error_massage.innerHTML = "信箱、密碼不能為空"
    }
    else{
      error_massage.style.display= "none" ;
      let member_data = {
        'email':email.value,
        'password':password.value,
      }
      let url = ip_addres+`api/user`;
      fetch(url, 
      {
        method: 'PATCH',
        body:JSON.stringify(member_data),  
        headers:{
        'Content-Type': 'application/json'
        }
      })
      .then(response =>{
            return  response.json()
      })
      .then( data =>{
        if(data['error'] === true){
          error_massage.style.display='block';
          error_massage.innerHTML = data['message']
        }
        else{
          fetch(url,{method: 'GET'})
          .then(response =>{
            return  response.json()
          })
          .then( data =>{
    
            if(data['data']['email'] === null){
              let login = document.getElementById("login")
              let loginout = document.getElementById("loginout")
              login.style.display = "block";
              loginout.style.display = "none";
            }
            else{
              let login = document.getElementById("login")
              let loginout = document.getElementById("loginout")
              login.style.display = "none";
              loginout.style.display = "block";
              close_login_dialog();

            }
          })
        }
      })

    }
}

function create_new_member_click(){
  let new_member_name = document.getElementById("new_member_name")
  let new_member_email = document.getElementById("new_member_email")
  let new_member_password = document.getElementById("new_member_password")
  let new_member_error_massage = document.getElementById("new_member_error_massage")
  if(new_member_name.value === "" || new_member_email.value === ""  || new_member_password.value ===""){
    new_member_error_massage.style.display='block';
    new_member_error_massage.innerHTML = "姓名、信箱、密碼不能為空"
  }
  else if(IsEmail(new_member_email.value) === false){
    new_member_error_massage.style.display='block';
    new_member_error_massage.innerHTML = "信箱格式錯誤";
  }
  else{
      let member_data = {
        'name':new_member_name.value,
        'email':new_member_email.value,
        'password':new_member_password.value,
      }
      let url =ip_addres+`api/user`;
      fetch(url, 
      {
        method: 'POST',
        body:JSON.stringify(member_data),  
        headers:{
        'Content-Type': 'application/json'
      }
      })
      .then(response =>{
        return  response.json()
      })
      .then( data =>{
        if(data['error'] === true){
          new_member_error_massage.style.display='block';
          new_member_error_massage.innerHTML = data['message']
        }
        else{
          new_member_error_massage.style.display='block';
          new_member_error_massage.innerHTML = '註冊成功'

        }
      })
  }

}

function loginout_click(){
  let login = document.getElementById("login")
  let loginout = document.getElementById("loginout")
  let login_dialog = document.getElementById("login_dialog")
  login_dialog.style.display ="block"
  login.style.display = "block";
  loginout.style.display = "none";
  let url = ip_addres+`api/user`;
  fetch(url, {method:'DELETE'})

}

function IsEmail(email) {
  let regex =  /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/; 
  if(!regex.test(email)) {
    return false;
  }else{
    return true;
  }
}

function booking_click(){
  let url = ip_addres+`api/user`;
  fetch(url, {method:'GET'})
  .then(response =>{
    return  response.json()
  })
  .then( data =>{
    
    if(data['data']['id'] == null){
      login_click();
    }
    else{
      window.location.href =ip_addres+"booking";
    }
  })  
}
let start_data = [] ;
let page = [] ;
let start_time  = [] ;
let end_time = [] ;
document.addEventListener("DOMContentLoaded",function(){
  page = 0 ;
  fetch(`http://3.87.217.170:3000/api/attractions?page=${page}`, {method: 'get'})
  .then(response =>{
    return  response.json()
  })
 .then( data =>{
  start_time = 0 ;
  end_time = 11 ;
  start_data = data ;
  show_img(start_time,end_time,data)


  window.addEventListener('scroll', function() {
      //文档内容实际高度（包括超出视窗的溢出部分）
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

                fetch(`http://3.87.217.170:3000/api/attractions?page=${page}&keyword=${keyword.value}`, {method: 'get'})
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
              fetch(`http://3.87.217.170:3000/api/attractions?page=${page}`, {method: 'get'})
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

        }
      }
      
    })
      })

})

window.onscroll=function(){

  let nav = document.getElementById("nav");//獲取到導航欄id
  nav.style.top = '0';
  nav.style.zIndex = '9999';
  nav.style.position = 'fixed';
  }


function select_click(){
  let keyword = document.getElementById("keyword");
  page = '';
  if(keyword.value == '' ){
    no_data();
   
  }
  else{
        fetch(`http://3.87.217.170:3000/api/attractions?keyword=${keyword.value}`, {method: 'get'})
        .then(response =>{
          return  response.json()
      })
      .then( select_click =>{
        start_data = select_click ;
        let keyword_length = Object.values(start_data['data']).length
        console.log('keyword_length',keyword_length)
        let div_delet = document.getElementById("third");
        
        
        if(start_data['data']['error'] ==  true){
          no_data();
        }
        else{
          div_delet.innerHTML ="";
          if(keyword_length >=13){
            console.log(keyword_length)
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
    for(var i = start_time ; i<=end_time;i++){

      let all_data_div = document.createElement("div");
      all_data_div.class = "show_data";
      all_data_div.id = "show_data"+[i];
      third.appendChild(all_data_div);
      let show_data = document.getElementById("show_data"+[i])
      let show_img = document.createElement("img"); 
      show_img.src=data['data'][j]['images'][0];
      show_data.appendChild(show_img);

      
      let third_p = document.createElement("p");
      third_p.className = "third_p";
      third_p.innerHTML = data['data'][j]['name'];
      show_data.appendChild(third_p);

      let third_a_right = document.createElement("a");
      third_a_right.className = "third_a_right";
      third_a_right.innerHTML = data['data'][j]['category'];
      show_data.appendChild(third_a_right);

      let third_a_left = document.createElement("a");
      third_a_left.className = "third_a_left";
      third_a_left.innerHTML = data['data'][j]['mrt'];
      show_data.appendChild(third_a_left);
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

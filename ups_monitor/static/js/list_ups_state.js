
document.addEventListener("DOMContentLoaded", function() {

	console.log("загружена страница");
  update();

});

function update(){
    $.ajax({
      url: '/api/state_ups/',
  
      dataType: 'json',
      success: function (data) {
        console.log(data);

        for (ups of data.data){
            
            const el = document.getElementById(ups.ups);
            //el.getElementsByClassName('ups_name')[0].textContent = ups.name;
            el.getElementsByClassName('ups_main_voltage')[0].textContent = ups.main_voltage;
            el.getElementsByClassName('ups_load')[0].textContent = ups.load;
            el.getElementsByClassName('ups_temperature')[0].textContent = ups.temperature;
            el.getElementsByClassName('ups_charge_battary')[0].textContent = ups.charge_battary;
            el.getElementsByClassName('ups_date_add')[0].textContent = ups.date_add;
            console.log(el.getElementsByClassName('ups_main_voltage')[0].textContent);
            if (el.getElementsByClassName('ups_main_voltage')[0].textContent < 10){
              $(document.getElementById(ups.ups)).css('background-color','red');
            }else {
              $(document.getElementById(ups.ups)).css('background-color','white');
            }
          }
        

            
        }
        
      }); 
    
      
    };
  

setInterval(update, 60000);
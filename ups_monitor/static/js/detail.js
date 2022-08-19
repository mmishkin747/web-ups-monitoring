$(document).ready(function () {

  $("#update_data").click(function (btn) {
    var input = $(this).val();
    console.log(btn.currentTarget.value);
 
    $.ajax({
        url: '/api/update_detail/' + btn.currentTarget.value,
  
        dataType: 'json',
        success: function (data) {
          console.log(data.data),
          document.getElementById('model').innerHTML = data.data.model,
          document.getElementById('voltage_battary').innerHTML = data.data.voltage_battary,
          document.getElementById('report_selftest').innerHTML = data.data.report_selftest,
          document.getElementById('made_data').innerHTML = data.data.made_date,
          document.getElementById('serial_number').innerHTML = data.data.serial_number;
          document.getElementById('battary_replacement').innerHTML = data.data.last_date_battary_replacement;
          document.getElementById('date_add').innerHTML = data.data.date_add;


        }, 
      });
    });

  
});





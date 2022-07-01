$("#sender").click(function () {
    var input = $(this).val();

    $.ajax({
        url: '/api_v1/update/',
        data: {
          'input_value': input
        },
        dataType: 'json',
        success: function () {
          document.getElementById('pText').innerHTML = value;
        }
      });
    });

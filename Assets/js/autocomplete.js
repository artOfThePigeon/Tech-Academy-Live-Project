jQuery(function() {
    $("#id_input").on('keyup', function(){
        var value = $(this).val();
        $.ajax({
            url: "{% url 'Forum:ajax_autocomplete' %}",
            data: {
              'search': value
            },
            dataType: 'json',
            success: function (data) {
                list = data.list;
                $("#id_input").autocomplete({
                source: user_list,
                minLength: 3
                });
            }
        });
    });
  });

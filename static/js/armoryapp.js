$(document).ready(function() {
    var $cart = $('#selected-seats'), //Table Area
    $counter = $('#counter'),
    $warning = $('#warning');
    var seats_to_reset = [];
    var day = "friday";
    var selected = null;


    var sc = $('#seat-map').seatCharts({
        map: [  //Seating chart
            '__aaaaaaaaaaaaaaaaa___',
            'a____________________a',
            'a__aaa___aaaa___aaa__a',
            'a_a___a_a____a_a___a_a',
            'a_a___a_a____a_a___a_a',
            'a_a___a_a____a_a___a_a',
            'a_a___a_a____a_a___a_a',
            'a__aaa___aaaa___aaa__a',
            'a____________________a',
            'a__aaa___aaaa___aaa__a',
            'a_a___a_a____a_a___a_a',
            'a_a___a_a____a_a___a_a',
            'a_a___a_a____a_a___a_a',
            'a_a___a_a____a_a___a_a',
            'a__aaa___aaaa___aaa__a',
            'a____________________a',
            'a__aaa___aaaa___aaa__a',
            'a_a___a_a____a_a___a_a',
            'a_a___a_a____a_a___a_a',
            'a_a___a_a____a_a___a_a',
            'a__aaa___aaaa___aaa__a',
            'a____________________a',
            '______aaaaaaaaaa______',
        ],
        naming : {
            top : false,
            getLabel : function (character, row, column) {
                return column;
            }
        },
        legend : { //It's confusing, yes but don't fucking touch it.
                   //by default, the colors are weird and unintiutive so
                   //I'm changing it up
            node : $('#legend'),
            items : [
                [ 'a', 'available',   'Company' ],
                [ 'a', 'unavailable', 'Unoccupied'],
                [ 'a', 'selected', 'Someone else']
            ]                   
        },
        
        click: function () { //Click event
            "{% if user.is_staff %}";
            $warning.text("");
            if (this.status() == 'available') {
                //Delete reservation
                $('#cart-item-'+this.settings.id).remove();
                return 'unavailable';
            } else if (sc.find('available').length === 3 ){
                $warning.text("Wtf no, you can't reserve more than three tables for one company.");
                return this.style();
            } else if (this.status() == 'unavailable') {
                $('<li>R'+(this.settings.row+1)+' S'+this.settings.label+'</li>')
                    .attr('id', 'cart-item-'+this.settings.id)
                    .data('seatId', this.settings.id)
                    .appendTo($cart);

                $counter.text(sc.find('available').length+1);
                            
                return 'available';
            } else if (this.status() == 'selected') { //unselect
                return 'unavailable';
            } else {
                return this.style();
            }

            "{% else %}"; //Don't let the unauthorized user do anything
            if (this.status() == 'selected') { 
                return 'selected';
            } else if (this.status() == 'available') {            
                return 'available';
            } else if (this.status() == 'unavailable') { 
                return 'unavailable';
            } else {
                return this.style();
            }
            "{% endif %}";
        }
    });

    sc.find('available').status('unavailable');


    $.ajax({
        type     : 'get',
        url      : '/bookings/get/'+day+'/',
        dataType : 'json',
        success  : function(response) {
            console.log(response.bookings)
            $.each(response.bookings, function(index, booking) {
                //find seat by id and set its status to unavailable
                sc.status(booking.seat_id, 'selected');
            });

        }
    });

    function getCookie(c_name)
        {
            if (document.cookie.length > 0)
            {
                c_start = document.cookie.indexOf(c_name + "=");
                if (c_start != -1)
                {
                    c_start = c_start + c_name.length + 1;
                    c_end = document.cookie.indexOf(";", c_start);
                    if (c_end == -1) c_end = document.cookie.length;
                    return unescape(document.cookie.substring(c_start,c_end));
                }
            }
         return "";
        }


    $("#friday-toggle").click(function(){
        day = "friday";
        refreshData(selected);
        sc.find('available').status('unavailable');
        sc.find('selected').status('unavailable');
    });

    $("#saturday-toggle").click(function(){
        day = "saturday";
        sc.find('available').status('unavailable');
        sc.find('selected').status('unavailable');
        refreshData(selected);

    });

    $(".row.selectable").click(function(){
        if (selected !== null){
            $(selected).css("background-color",'');
        }
        selected = this;
        $(selected).css("background-color","#B9DEA0");
        refreshData(selected);
        sc.find('available').status('unavailable');
    });

    function refreshData(div){
        console.log("ok");
            $.ajax({
            type     : 'get',
            url      : '/bookings/get_company/'+$(div).attr('id')+'/'+day+'/',
            dataType : 'json',
            success  : function(response) {
                //iterate through all bookings for our event 
                $.each(response.others, function(index, other) {
                    //find seats reserved by people other than the
                    // specified company by id and set its status to selected
                    sc.status(other.seat_id, 'selected');
                });

                $.each(response.bookings, function(index, booking) {
                    //find seat by id and set its status to unavailable
                    sc.status(booking.seat_id, 'available');
                });
                $("#companyname").text(response.companyname);
                if (response.logo){
                    $("#logo").html("<img class=\"img-border\" src=\""+response.logo+"\"/>");
                }
                else {
                    $("#logo").html();
                }
                if (response.bio){
                    $("#company_bio").html("<h2>Bio</h2>"+response.company_bio);
                }
                else {
                    $("#bio").html();
                }
                $("#days_attending").html("<h2>Days attending</h2>"+response.days_attending);
                $("#majors_wanted").html("<h2>Majors hiring</h2>"+response.majors_wanted);
                $("#grade_level_wanted").html("<h2>Grade levels hiring</h2>"+response.grade_level_wanted);
                old_seats = sc.find('available').seatIds;
            }
        });
    }

    $("#table-submit").click(function(){
        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken")},
            url: '/bookings/post_all/'+day+'/',
            type: 'POST',
            data: JSON.stringify({
                "company" : $(selected).attr('id'),
                "bookings" : sc.find('available').seatIds,
                "to_delete": sc.find('unavailable').seatIds,
            }),
            dataType: 'json',
            success: function() {
                old_seats = sc.find('available').seatIds;
                $warning.text("Changes submitted");
            },
            error: function() {
                $warning.text("Something went wrong with the database...");
            }
        });
    });  
});

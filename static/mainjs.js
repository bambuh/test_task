$(document).ready(function(){              
    $('#book_find').click(function(){      
        $('#books_list').load('/book-filter?bfilter='+$('#book_find_text').attr('value'));           
    }) 
    $('#book_find_text').keypress(function(e){
    	if (e.which == 13){
    		$('#book_find').trigger('click');
    		// $('#books_list').load('/book-filter?bfilter='+$('#book_find_text').attr('value'));
    	}
    }) 
    $('#author_find').click(function(){      
        $('#authors_list').load('/author-filter?afilter='+$('#author_find_text').attr('value'));           
    }) 
    $('#author_find_text').keypress(function(e){
    	if (e.which == 13){
    		$('#author_find').trigger('click')
        // $('#authors_list').load('/author-filter?afilter='+$('#author_find_text').attr('value'));           
    	}
    }) 
    // $('#book_find_text').keyup(function(){      
    //     $('#books_list').load('/book-filter?bfilter='+$('#book_find_text').attr('value'));           
    // }) 
    $('#editmode').click(function(){   
    	$(this).hide();
    	$('#book_add_div').show();
    	$('#viewmode').show();
        $('.books_tab').animate({ width: "59%" }, "slow");
        $('.authors_tab').show().animate({ opacity: "0"}, "slow").animate({ opacity: "1"}, "slow");
    }); 
    $('#viewmode').click(function(){   
    	$(this).hide();
    	$('#book_add_div').hide();
    	$('#editmode').show();
        $('.authors_tab').animate({ opacity: "0"}, "slow").end().hide();
        $('.books_tab').animate({ opacity: "1"}, "slow").animate({ width: "100%" }, "slow");
    }); 
    $('.author_edit_btn').click(function(){
    	$(this).hide();
    	alert($(this).attr("id").replace("author_edit_", ""));
    });

}); 
		// 	$(function(){
		// 		$('dl.tabs dt').click(function(){
		// 			$(this)
		// 				.siblings().removeClass('selected').end()
		// 				.next('dd').andSelf().addClass('selected');
		// 		});
		// 	});
		// 
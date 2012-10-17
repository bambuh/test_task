$(document).ready(function(){              
    $('#book_find').click(function(){   
    	$.get('/book-filter', {'bfilter':$('#book_find_text').attr('value')}, function(html){
    		$('#books_list').html(html)
    		if ($('#edit_mode > a:hidden').attr('id') == 'viewmode') {
    			$('.book_author_del_btn, .book_edit_btn, .book_del_btn').hide();
    		}
    	}, 'html')   
    }) 
    $('#book_find_text').keypress(function(e){
    	if (e.which == 13){
    		$('#book_find').trigger('click');
    	}
    }) 
    $('#author_find').click(function(){      
        $('#authors_list').load('/author-filter?afilter='+$('#author_find_text').attr('value'));           
    }) 
    $('#author_find_text').keypress(function(e){
    	if (e.which == 13){
    		$('#author_find').trigger('click')
    	}
    }) 
    $('#editmode').click(function(){   
    	$(this).hide();
    	$('#book_add_div').show();
    	$('#viewmode').show();
        $('.books_tab').animate({ width: "65%" }, "slow");
        $('.authors_tab').show().animate({ opacity: "0"}, "slow").animate({ opacity: "1"}, "slow");
        $('.book_author_del_btn, .book_edit_btn, .book_del_btn').show();
        $('#author_find').trigger('click')
    }); 
    $('#viewmode').click(function(){   
    	$(this).hide();
    	$('#book_add_div').hide();
    	$('#editmode').show();
        $('.authors_tab').animate({ opacity: "0"}, "slow").end().hide();
        $('.books_tab').animate({ opacity: "1"}, "slow").animate({ width: "100%" }, "slow");
        $('.book_author_del_btn, .book_edit_btn, .book_del_btn').hide();
    }); 
    $('.book_author_del_btn, .book_edit_btn, .book_del_btn').hide();
    $('#book_find').trigger('click')

}); 

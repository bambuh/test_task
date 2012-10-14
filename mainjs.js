			$(function(){
				$('dl.tabs dt').click(function(){
					$(this)
						.siblings().removeClass('selected').end()
						.next('dd').andSelf().addClass('selected');
				});
			});
		
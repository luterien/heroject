// Checkbox
$(document).ready(function(){
	
	$('.checkbox').click(function(){
		$(this).toggleClass('checked');
	});

	$('.show-user').hover(function(){
		$(this).find('.user-list').toggle();
	});
});
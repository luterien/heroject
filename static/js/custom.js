$(document).ready(function(){
	
	// Checkbox
	$('.checkbox').click(function(){
		$(this).addClass('checked');
	});

	$('.checked').click(function(){
		$(this).removeClass('checked');
	});

	// Dropdown
	$('.show-menu').hover(function(){
		$(this).find('.menu-list').toggle();
	});

	// Load Creater
	$('#ajax-crt').click(function(){
		$(this).parent().load('/project/create/');
	});

	// Ajax
	$('#project-active-tasks li input').on("change", function(){
	update_task_status(this);
	});

	$('#project-completed-tasks li input').on("change", function(){
	update_task_status(this);
	});

	function update_task_status(that){

		var task_id = $(that).val();

		if (that.checked){
		task_is_done = 1
		} else {
		task_is_done = 0
		}

		$.ajax({

		url : "/tasks/update_status/",
		data : {'is_done': task_is_done, 'task_id': task_id}

		}).success(function(r){

		$('#project-active-tasks').load(' #project-active-tasks', function(){$(this).children().unwrap()});
		$('#project-completed-tasks').load(' #project-completed-tasks', function(){$(this).children().unwrap()});
		//$('.progress').load('.progress', function(){$(this).children().unwrap()});

		})
	};
});
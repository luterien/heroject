// Checkbox
$(document).ready(function(){
	$('.checkbox').click(function(){
		$(this).toggleClass('checked');
	});
});

// Ajax

$('#project-active-tasks li input').live("change", function(){
	update_task_status(this);
});

$('#project-completed-tasks li input').live("change", function(){
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
		$('.progress').load(' .progress', function(){$(this).children().unwrap()});

	})
};
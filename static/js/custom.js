$(document).ready(function(){
	
	// Checkbox
	$('.checkbox').live("click", function(){
		if ($(this).hasClass('checked') == false) {
			$(this).addClass('checked');
			update_task_status($(this).next(), true);
		} else {
			$(this).removeClass('checked');
			update_task_status($(this).next(), false);
		}
	});

	// Dropdown
	$('.show-menu').hover(function(){
		$(this).find('.menu-list').toggle();
	});

	// Load Creater
	$('#ajax-crt').click(function(){
		$(this).parent().load('/project/create/', function() {
        
            $("#id_title").focus();
        });

	});	
	
	$('.crt-project a').click(function(){
		$("#ajax-crt").parent().load('/project/create/');
	});

	function update_task_status(that, checked){

		var task_id = $(that).val();
		var slug = $('#project_slug').val();

		var active_tasks_url = "/project/" + slug + "/active_tasks/";
		var completed_tasks_url = "/project/" + slug + "/completed_tasks/";

		if (checked==true){
		task_is_done = 1
		} else {
		task_is_done = 0
		}

		$.ajax({

		url : "/project/tasks/update_status/",
		data : {'is_done': task_is_done, 'task_id': task_id}

		}).success(function(r){
			$('#project-active-tasks').load(active_tasks_url);
			$('#project-completed-tasks').load(completed_tasks_url);
			//$('.progress').load('.progress', function(){$(this).children().unwrap()});
			//location.reload();
		})
	};


	$('select').addClass('select2');
	$('.select2').select2();

	$('.assign select').live('change', function(){

		var user_id = $(this).val();
		var task_id = $('#task_id').val();

		var assigned = "/task/" + task_id + "/people/";

		$.ajax({

			url : "/task/assign/",
			data : {'user_id': user_id, 'task_id':task_id }

		}).success(function(r){
			$('#assigned').load(assigned);
		})

	});

	$('#remove_from_task').live('click', function(){

		var user_id = $(this).find('input').val();
		var task_id = $('#task_id').val();

		var assigned = "/task/" + task_id + "/people/";

		$.ajax({

			url : "/task/remove/",
			data : {'user_id': user_id, 'task_id':task_id }

		}).success(function(r){
			$('#assigned').load(assigned);
		})

	});

	$('.add-todo-form').submit(function(){

		if ($('#id_title').val() == ""){
			$('#warning_text').css('display','block');
			return false;
		}
	})

});

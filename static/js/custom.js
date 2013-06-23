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


    var update_progress = function(width) {
        var prg_cnt = $(".prg-cnt strong"),
            bar = $(".progress .bar");

        bar.animate({ "width": width + "%"});
        prg_cnt.html("%" + width);

        if (!width) prg_cnt.empty();
    };
	
	function reload_task_list(slug){

		var active_tasks_url = "/project/" + slug + "/active_tasks/";
		var completed_tasks_url = "/project/" + slug + "/completed_tasks/";
	
		$('#project-active-tasks').load(active_tasks_url);
		$('#project-completed-tasks').load(completed_tasks_url, function(data) {
			var progress = jQuery("span.progress", data.prevObject).text() || 0;
			
			update_progress(progress);
		});
	
	}
	
	function update_task_status(that, checked){

		var task_id = $(that).val();
		var slug = $('#project_slug').val();

		if (checked==true){
			task_is_done = 1
		} else {
			task_is_done = 0
		}

		$.ajax({

			url : "/project/tasks/update_status/",
			data : {'is_done': task_is_done, 'task_id': task_id}

		}).success(function(r){
			reload_task_list(slug);
			//$('.progress').load('.progress', function(){$(this).children().unwrap()});
			//location.reload();
		})
	};

	$('select').addClass('select2');
	$('.select2').select2();

	function assign_user_to_task(user_id, task_id, callback){
		$.ajax({
			url : "/task/assign/",
			data : {'user_id': user_id, 'task_id':task_id }
		}).success(callback)
	}
	
	function remove_user_from_task(user_id, task_id, callback){
		$.ajax({
			url : "/task/remove/",
			data : {'user_id': user_id, 'task_id':task_id }
		}).success(callback)
	}
	
	$('.assign select').live('change', function(){

		var user_id = $(this).val();
		var task_id = $('#task_id').val();
		
		var assigned = "/task/" + task_id + "/people/";
		
		assign_user_to_task(user_id, task_id, function(r){$('#assigned').load(assigned)});

	});

	$('#remove_from_task').live('click', function(){

		var user_id = $(this).find('input').val();
		var task_id = $('#task_id').val();
		
		var assigned = "/task/" + task_id + "/people/";

		remove_user_from_task(user_id, task_id, function(r){$('#assigned').load(assigned)});

	});
	
	$('.todo-people').live('change', function(){

		var user_id = $(this).find('option:selected').val();
		var task_id = $(this).parent().attr('data-taskid');
		
		var assigned = "/task/" + task_id + "/people/";
		
		// TODO : refresh task detail
		
		assign_user_to_task(user_id, task_id, function(r){console.log(r);});

	});

	$('.add-todo-form').submit(function(){

		if ($('#id_title').val() == ""){
			$('#warning_text').css('display','block');
			return false;
		}
	})

});

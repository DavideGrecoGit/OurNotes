function manage_member(btn, view_name, remove_group=false){
    var page = window.location.pathname.split('/')[1]
    var group_slug = $(btn).attr('data-group_slug');

    $.get('/'+view_name+'/', {'group_slug': group_slug})
    .done( function(){
        
        if(page=="search"){
            // If Page does not exist anymore, redirect to search
            if(remove_group){
                alert("Group deleted with success.\nClick 'OK' to go to the search page");
                window.location.href = '/search/';
            }
            //Else reload
            else{
                location.reload();
            }
            
        }else{
            // No need to reload
            $("#"+group_slug).removeClass("flex");
            $("#"+group_slug).addClass("hidden");
        }
    })
    .fail(function(){alert("An error occured");})
}

$(document).ready(function() {
    $('#remove_btn').click(function() {
        if(confirm("Are you sure to delete this group and all its content?")){
            manage_member(this, 'remove_group', remove_group=true)
        }
    });

    $('#leave_btn').click(function() {
        manage_member(this, 'remove_group')
    });

    $('#join_btn').click(function() {
        manage_member(this, 'join_group')
    });
});

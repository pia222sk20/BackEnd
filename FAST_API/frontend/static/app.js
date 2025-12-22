$(document).ready(function(){
    $('#todoForm').on('submit',function(e){
        e.preventDefault()
        addTodo();
    });
});

function addTodo(){
    const title = $('#todoTitle').val().trim();
    const description = $('#todoDescription').val().trim();
    const todoData = {
        title:title,
        description : description || null
    }
    $.ajax({
        url : 'http://localhost:8000/api/todos',
        method:'POST',
        data:JSON.stringify(todoData),
        contentType:'application/json',
        success:function(newTodo){
            console.log('추가 성공', newTodo)
        },
        error:function(error){
            console.log('추가 실패', error)
        }
    });
}
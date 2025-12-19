$(document).ready(function(){
    loadUsers();
});

function loadUsers(){
    $.ajax({
        url:'/api/users', 
        method: 'GET',
        success:function(users){
            $('#userTable').empty();
            users.forEach(user => {
                $('#userTable').append(
                     $('#userTable').append(
                    `
                    <tr data-id="${user.id}">
                        <td><input type="checkbox" class="chk"></td>
                        <td>${user.id}</td>
                        <td>${user.name}</td>
                        <td>${user.email}</td>
                        <td>
                            <button class="edit">MODIFY</button>
                            <button class="remove">REMOVE</button>
                        </td>
                    </tr>
                    `
                    )
                )
            });
        },
        error:function(){
            alert('목록조회 실패');
        }
    });
}
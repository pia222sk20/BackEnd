// api를 테스트하기위해서 통신이 필요하고 Mock 서버인 json server로 실습
// npm install -g json-server
// json-server --watch db.json --port 3000

$(document).ready(function(){
    loadUsers();
});

function loadUsers(){
    $.ajax({
        url:'http://localhost:3000/users', 
        method: 'GET',
        success:function(users){
            $('#userTable').empty();
            users.forEach(user => {
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
            });
        },
        error:function(){
            alert('목록조회 실패');
        }
    });
}
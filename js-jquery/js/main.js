console.log('js 연결확인')

//  dom - html전체 구조를 객체화 한것
$(document).ready(
    function(){
        console.log('jquery 준비완료');

        $("#btn").click(function(){
            $('#text').text('버튼 클릭됨');        
        })

        // 전체선택
        $("#checkall").on('change',function(){
            $('.chk').prop('checked',this.checked);
            const checked = $('.chk:checked').length
            // 개수를 카운트
            $('#count').text(checked)

        });

        // 개별체크로 전체 컨트롤
        $('.chk').on('change',function(){
            const total = $('.chk').length
            const checked = $('.chk:checked').length
            $('#checkall').prop('checked',total==checked)
            // 개수를 카운트
            $('#count').text(checked)

        });

        // 선택 삭제
        $('#deleteBtn').click(function(){
            $('.tchk:checked').each(function(){
                $(this).closest('tr').remove()
            });
        });
        // 버튼 비활성화(중복 클릭 방지)  저장 결제 api 호출
        $('#saveBtn').click(function(){
            $(this).prop('diabled',true)

            setTimeout( ()=>{
                $(this).prop('disabled',false)
            },2000  );
        });

    }   
);
$(function(){
    $('div.form-group [id^=id_]').addClass('form-control');

    $('#category-modal-btn').click(function(){
        $('#modalCategoryForm').find('input[type="text"]').val('');
    });

    $('body').tooltip({
        selector: '[data-toggle="tooltip"]'
    });
});
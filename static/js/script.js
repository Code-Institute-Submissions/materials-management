var new_items = [[],[],[],[]]
var new_item_name = []
var new_item_qty = []
var new_item_cost = []
var new_item_id = []
var item_id = 0
    
    $(document).ready(function(){
    $('.sidenav').sidenav();
    $('.fixed-action-btn').floatingActionButton();
    $('.modal').modal();
    $('select').formSelect();
    $('.dropdown-trigger').dropdown();
    $('.tabs').tabs();
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    
    
    $('.navpanellayer').mouseenter(function(){
        $(this).css("width","0");
        $('.navpanel').css("width","200px","visibility","visible");
    })

    $('.navpanel').mouseleave(function(){
        $(this).css("width","0","visibility","hidden");
        $('.navpanellayer').css("width","10px");
    })

    $('#plus-inventory').click(function(){
        $('#mobilepanel-plus-inventory').toggle('slow');
        $('#mobilepanel-caret').hide();
        $('#mobilepanel-search-inventory').hide();
    })

    $('#search-inventory').click(function(){
        $('#mobilepanel-search-inventory').toggle('slow');
        $('#mobilepanel-caret').hide();
        $('#mobilepanel-plus-inventory').hide();
    })

    $('.caret-up').click(function(){
        $('#mobilepanel-caret').toggle('slow');
        $('#mobilepanel-plus-inventory').hide();
        $('#mobilepanel-search-inventory').hide();
    })

    $('.contentrow, .tabrow, nav, #search-inventory, .caret-up ,#mobilepanel-plus-inventory').click(function(){
        $('#mobilepanel-plus-inventory').css("display", "none");
    })

    $('.contentrow, .tabrow, nav, #plus-inventory, .caret-up,#mobilepanel-plus-inventory').click(function(){
        $('#mobilepanel-search-inventory').css("display", "none");
    })

    $('.contentrow, .tabrow, nav, #plus-inventory, #mobilepanel-search-inventory ,#mobilepanel-plus-inventory').click(function(){
        $('#mobilepanel-caret').css("display", "none");
    })

    
    $('#add_purchase_item').click(function(){
        new_items[0] = $(this).parent().parent().find("#puo_item_name").val().split(",");
        new_items[1] = $(this).parent().parent().find("#puo_item_qty").val();
        if (new_items[1] == ""){
            return
        };
        new_item_name.push(new_items[0][0]);
        new_item_cost.push(new_items[0][1]);
        new_item_qty.push(new_items[1]);
        new_item_id.push(item_id);
        $('#new_purchase_items').val(new_item_name);
        $('#new_purchase_cost').val(new_item_cost);
        $('#new_purchase_qty').val(new_item_qty);
        $('#new_purchase_id').val(new_item_id);
        $('#items_list').append(`
            <tbody>
                <tr id=${item_id}>
                    <td>${new_items[0][0]}</td>
                    <td>${new_items[1]}</td>
                    <td>$${new_items[0][1]}</td>
                    <td>$${new_items[0][1]*new_items[1]}</td>
                    <td><strong onclick="delete_item(this)"><i class="fas fa-times"></strong></i></div></td>
                </tr>
            </tbody>
        `);  
        item_id++;
    })

});

function delete_item(btn){
    index = new_item_id.indexOf(Number(btn.parentElement.id));
    new_item_name.splice(index, 1);
    new_item_cost.splice(index, 1);
    new_item_qty.splice(index, 1);
    new_item_id.splice(index, 1);
    btn.parentElement.parentElement.remove();
}